"""Agrupa os chunks da collection por conteúdo e gera as visualizações.

Todos os PDFs são tratados como um único corpus: o K-Means roda sobre os
embeddings dos chunks, sem usar arquivo de origem nem categoria do arXiv.
Cada grupo recebe um nome curto gerado pelo LLM local a partir dos termos
mais característicos (c-TF-IDF) e de trechos representativos.

Saídas:
  - payload no Qdrant: cluster_id, topico e amostra_viz (para a aba Visualize)
  - visualizacoes/*.png: UMAP, PCA e t-SNE coloridos por tópico
  - visualizacoes/topicos.json e visualizacoes/topicos.md
  - visualizacoes/qdrant_*.json: consultas para colar na aba Visualize

Uso (no host, com o venv do projeto):
    .venv/Scripts/python.exe scripts/cluster_topics.py
"""

import argparse
import json
import os
import re
from collections import Counter
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import requests
from qdrant_client import QdrantClient
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.manifold import TSNE
from sklearn.metrics import silhouette_score

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "visualizacoes"

# Paleta categórica validada (ordem fixa) + marcador por tópico como segunda codificação
COLORS = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]
MARKERS = ["o", "s", "^", "D", "v", "P", "X", "*"]
SURFACE = "#fcfcfb"
TEXT_PRIMARY = "#0b0b0b"
TEXT_SECONDARY = "#52514e"
MUTED = "#d6d5d0"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--url", default="http://localhost:6333")
    parser.add_argument("--api-key", default=os.getenv("QDRANT_API_KEY", "plnCEUB12025-SK2025"))
    parser.add_argument("--collection", default="artigos_ia")
    parser.add_argument("--k", type=int, default=0, help="0 = escolher entre 5 e 8 pela silhueta")
    parser.add_argument("--ollama", default="http://localhost:11434")
    parser.add_argument("--llm", default="qwen2.5:7b")
    parser.add_argument("--viz-sample", type=int, default=2000, help="pontos marcados para a aba Visualize")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--nomes", type=Path,
        help="JSON {cluster_id: nome} com nomes revisados; o nome sugerido pelo LLM fica em nome_llm",
    )
    return parser.parse_args()


def load_points(client: QdrantClient, collection: str):
    ids, vectors, payloads = [], [], []
    offset = None
    while True:
        points, offset = client.scroll(
            collection,
            limit=1000,
            offset=offset,
            with_vectors=True,
            with_payload=["content", "file_name_safe", "titulo", "chunk_index"],
        )
        for point in points:
            if point.id == 0:  # ponto de metadata da collection
                continue
            ids.append(point.id)
            vectors.append(point.vector)
            payloads.append(point.payload)
        if offset is None:
            break
    X = np.asarray(vectors, dtype=np.float32)
    X /= np.linalg.norm(X, axis=1, keepdims=True)
    return ids, X, payloads


def choose_k(X: np.ndarray, seed: int) -> tuple[int, dict[int, float]]:
    rng = np.random.default_rng(seed)
    sample = rng.choice(len(X), size=min(4000, len(X)), replace=False)
    scores = {}
    for k in range(5, 9):
        labels = KMeans(n_clusters=k, n_init=10, random_state=seed).fit_predict(X)
        scores[k] = float(silhouette_score(X[sample], labels[sample], metric="cosine"))
        print(f"  k={k}: silhueta={scores[k]:.4f}")
    return max(scores, key=scores.get), scores


def distinctive_terms(texts: list[str], labels: np.ndarray, k: int, top: int = 12) -> list[list[str]]:
    """Termos que distinguem cada grupo do resto do corpus (log-odds ponderado pela frequência).

    O c-TF-IDF clássico, com só k "documentos", deixa palavras genéricas como
    "model" e "training" no topo de todos os grupos; aqui cada termo é comparado
    com sua frequência nos demais grupos.
    """
    docs = [" ".join(texts[i] for i in np.where(labels == c)[0]) for c in range(k)]
    vectorizer = CountVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        min_df=1,
        max_features=60000,
        token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z\-]{2,}\b",
    )
    counts = vectorizer.fit_transform(docs).toarray().astype(float)
    vocab = vectorizer.get_feature_names_out()
    totals = counts.sum(axis=1, keepdims=True)
    rest = counts.sum(axis=0, keepdims=True) - counts
    p_in = (counts + 0.5) / (totals + 0.5 * counts.shape[1])
    p_out = (rest + 0.5) / (totals.sum() - totals + 0.5 * counts.shape[1])
    scores = p_in * np.log(p_in / p_out)
    scores[counts < 15] = -np.inf  # ignora termos raros dentro do grupo
    return [[vocab[j] for j in np.argsort(row)[::-1][:top]] for row in scores]


def name_topic(args, terms: list[str], snippets: list[str], titles: list[str], taken: set[str]) -> dict:
    prompt = (
        "Você vai nomear um grupo de trechos (chunks) extraídos de 100 artigos científicos de IA.\n"
        "Os trechos foram agrupados só pelo conteúdo. Um grupo pode reunir um TEMA "
        "(ex.: visão 3D, agentes de LLM, robótica) ou um TIPO DE TEXTO que aparece em "
        "todos os artigos (ex.: referências bibliográficas, tabelas de resultados, "
        "provas matemáticas, prompts de avaliação). Nomeie pelo que os trechos realmente "
        "contêm; os títulos dos artigos são só uma pista e podem enganar.\n\n"
        f"Termos que mais distinguem o grupo do resto do corpus: {', '.join(terms)}\n"
        f"Artigos com mais trechos no grupo: {'; '.join(titles)}\n"
        "Trechos mais próximos do centro do grupo:\n- " + "\n- ".join(snippets) + "\n\n"
        f"Nomes já usados por outros grupos (não repita): {', '.join(sorted(taken)) or 'nenhum'}\n"
        'Responda só com JSON: {"nome": "<2 a 4 palavras em português, específico>", '
        '"descricao": "<uma frase em português sobre o conteúdo do grupo>"}'
    )
    try:
        response = requests.post(
            f"{args.ollama}/api/chat",
            json={
                "model": args.llm,
                "messages": [{"role": "user", "content": prompt}],
                "format": "json",
                "stream": False,
                "options": {"temperature": 0.2},
            },
            timeout=300,
        )
        response.raise_for_status()
        result = json.loads(response.json()["message"]["content"])
        if result.get("nome") and result["nome"] not in taken:
            return {"nome": result["nome"].strip(), "descricao": result.get("descricao", "").strip()}
    except Exception as error:
        print(f"  LLM indisponível para nomear ({error}); usando os termos")
    return {"nome": " / ".join(terms[:3]), "descricao": ""}


def snippet(text: str, size: int = 280) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    return text[:size] + ("…" if len(text) > size else "")


def place_labels(centers, names, ax, iterations=200):
    """Afasta rótulos sobrepostos e os mantém dentro dos limites do eixo."""
    (x0, x1), (y0, y1) = ax.get_xlim(), ax.get_ylim()
    width, height = x1 - x0, y1 - y0
    # Tamanho aproximado de cada caixa em unidades de dados (fonte 9 numa figura de 13")
    sizes = np.array([[0.0085 * width * (len(n) + 2), 0.045 * height] for n in names])
    pos = np.array(centers, dtype=float)
    # Começa um pouco acima do centro para não cobrir grupos pequenos e densos
    pos[:, 1] += sizes[:, 1]
    for _ in range(iterations):
        moved = False
        for i in range(len(pos)):
            for j in range(i + 1, len(pos)):
                dx, dy = pos[j] - pos[i]
                overlap_x = (sizes[i, 0] + sizes[j, 0]) / 2 - abs(dx)
                overlap_y = (sizes[i, 1] + sizes[j, 1]) / 2 - abs(dy)
                if overlap_x > 0 and overlap_y > 0:
                    # Separa na direção vertical, que custa menos espaço
                    shift = (overlap_y / 2 + 0.002 * height) * (1 if dy >= 0 else -1)
                    pos[i, 1] -= shift
                    pos[j, 1] += shift
                    moved = True
        pos[:, 0] = np.clip(pos[:, 0], x0 + sizes[:, 0] / 2, x1 - sizes[:, 0] / 2)
        pos[:, 1] = np.clip(pos[:, 1], y0 + sizes[:, 1] / 2, y1 - sizes[:, 1] / 2)
        if not moved:
            break
    return [tuple(p) for p in pos]


def plot_projection(coords, labels, topics, title, subtitle, path):
    fig, ax = plt.subplots(figsize=(13, 9), dpi=150)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)
    for c, topic in enumerate(topics):
        mask = labels == c
        ax.scatter(
            coords[mask, 0], coords[mask, 1],
            s=9, marker=MARKERS[c], c=COLORS[c], alpha=0.55, linewidths=0,
            label=f"{topic['nome']} ({mask.sum()})",
        )
    # Rótulo direto no centro de cada grupo: a identidade não depende só da cor
    (x0, y0), (x1, y1) = coords.min(axis=0), coords.max(axis=0)
    pad_x, pad_y = (x1 - x0) * 0.06, (y1 - y0) * 0.06
    ax.set_xlim(x0 - pad_x, x1 + pad_x)
    ax.set_ylim(y0 - pad_y, y1 + pad_y)
    positions = place_labels(
        [np.median(coords[labels == c], axis=0) for c in range(len(topics))],
        [t["nome"] for t in topics],
        ax,
    )
    for c, topic in enumerate(topics):
        ax.annotate(
            topic["nome"], positions[c], ha="center", va="center", fontsize=9, fontweight="bold",
            color=TEXT_PRIMARY, annotation_clip=False,
            bbox=dict(boxstyle="round,pad=0.3", fc=SURFACE, ec=COLORS[c], lw=1.5, alpha=0.92),
        )
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.text(0.02, 0.965, title, fontsize=15, fontweight="bold", color=TEXT_PRIMARY)
    fig.text(0.02, 0.935, subtitle, fontsize=10, color=TEXT_SECONDARY)
    legend = ax.legend(
        loc="upper left", bbox_to_anchor=(1.0, 1.0), frameon=False, fontsize=9,
        markerscale=2.2, title="Tópico (nº de chunks)", title_fontsize=9,
    )
    for text in legend.get_texts():
        text.set_color(TEXT_PRIMARY)
    for handle in legend.legend_handles:
        handle.set_alpha(1)
    fig.subplots_adjust(left=0.02, right=0.74, top=0.91, bottom=0.03)
    fig.savefig(path, facecolor=SURFACE)
    plt.close(fig)


def plot_small_multiples(coords, labels, topics, path):
    """Um painel por tópico, destacado sobre os demais em cinza (leitura sem depender de cor)."""
    k = len(topics)
    cols = 4
    rows = int(np.ceil(k / cols))
    fig, axes = plt.subplots(rows, cols, figsize=(16, 4.2 * rows), dpi=130)
    fig.patch.set_facecolor(SURFACE)
    for c, ax in enumerate(np.ravel(axes)):
        ax.set_facecolor(SURFACE)
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)
        if c >= k:
            continue
        ax.scatter(coords[:, 0], coords[:, 1], s=3, c=MUTED, linewidths=0)
        mask = labels == c
        ax.scatter(coords[mask, 0], coords[mask, 1], s=5, c=COLORS[c], marker=MARKERS[c], linewidths=0)
        ax.set_title(f"{topics[c]['nome']}  ·  {mask.sum()} chunks", fontsize=10, color=TEXT_PRIMARY, loc="left")
    fig.suptitle("UMAP por tópico: cada painel destaca um grupo", fontsize=14, fontweight="bold",
                 color=TEXT_PRIMARY, x=0.01, ha="left")
    fig.tight_layout()
    fig.savefig(path, facecolor=SURFACE)
    plt.close(fig)


def main() -> None:
    args = parse_args()
    OUT.mkdir(exist_ok=True)
    client = QdrantClient(url=args.url, api_key=args.api_key, timeout=120, check_compatibility=False)

    print("Lendo vetores do Qdrant…")
    ids, X, payloads = load_points(client, args.collection)
    texts = [p.get("content", "") for p in payloads]
    print(f"{len(ids)} chunks, {X.shape[1]} dimensões, {len({p.get('file_name_safe') for p in payloads})} PDFs")

    scores = {}
    if args.k:
        k = args.k
    else:
        print("Escolhendo k pela silhueta (cosseno):")
        k, scores = choose_k(X, args.seed)
    print(f"k = {k}")
    kmeans = KMeans(n_clusters=k, n_init=20, random_state=args.seed).fit(X)

    # Ordena os grupos do maior para o menor: o slot de cor segue o tamanho do grupo
    order = [c for c, _ in Counter(kmeans.labels_).most_common()]
    remap = {old: new for new, old in enumerate(order)}
    labels = np.array([remap[c] for c in kmeans.labels_])
    centroids = kmeans.cluster_centers_[order]

    print("Termos característicos e nomes:")
    terms = distinctive_terms(texts, labels, k)
    reviewed = json.loads(args.nomes.read_text(encoding="utf-8")) if args.nomes else {}
    topics, taken = [], set()
    for c in range(k):
        members = np.where(labels == c)[0]
        central = members[np.argsort(-(X[members] @ centroids[c]))[:6]]
        papers = Counter(payloads[i].get("titulo") or payloads[i].get("file_name_safe") for i in members)
        name = name_topic(args, terms[c], [snippet(texts[i]) for i in central], [t for t, _ in papers.most_common(4)], taken)
        taken.add(name["nome"])
        topics.append({
            "cluster_id": c,
            "nome": reviewed.get(str(c), name["nome"]),
            "nome_llm": name["nome"],
            "descricao": name["descricao"],
            "chunks": int(len(members)),
            "pdfs": int(len(papers)),
            "termos": terms[c],
            "artigos_principais": [{"titulo": t, "chunks": n} for t, n in papers.most_common(5)],
            "trechos_centrais": [snippet(texts[i], 400) for i in central[:3]],
        })
        print(f"  [{c}] {topics[c]['nome']} (LLM: {name['nome']}) — {len(members)} chunks — {', '.join(terms[c][:6])}")

    print("Gravando tópicos no payload do Qdrant…")
    rng = np.random.default_rng(args.seed)
    viz = set()
    for c in range(k):
        members = np.where(labels == c)[0]
        quota = max(1, round(args.viz_sample * len(members) / len(ids)))
        viz.update(rng.choice(members, size=min(quota, len(members)), replace=False).tolist())
        for start in range(0, len(members), 1000):
            batch = members[start:start + 1000]
            client.set_payload(
                args.collection,
                payload={"cluster_id": c, "topico": topics[c]["nome"]},
                points=[ids[i] for i in batch],
            )
    viz_ids = [ids[i] for i in sorted(viz)]
    client.set_payload(args.collection, payload={"amostra_viz": False}, points=ids)
    for start in range(0, len(viz_ids), 1000):
        client.set_payload(args.collection, payload={"amostra_viz": True}, points=viz_ids[start:start + 1000])

    print("Projeções 2D…")
    reduced = PCA(n_components=50, random_state=args.seed).fit_transform(X)
    import umap

    projections = {
        "umap": umap.UMAP(n_neighbors=30, min_dist=0.1, metric="cosine", random_state=args.seed).fit_transform(X),
        "pca": PCA(n_components=2, random_state=args.seed).fit_transform(X),
        "tsne": TSNE(n_components=2, perplexity=40, init="pca", random_state=args.seed).fit_transform(reduced),
    }
    names = {"umap": "UMAP", "pca": "PCA", "tsne": "t-SNE"}
    subtitle = (f"{len(ids)} chunks de {len({p.get('file_name_safe') for p in payloads})} PDFs tratados como um único corpus · "
                f"embeddings bge-m3 (1024 dim) · cor = tópico encontrado pelo K-Means (k={k})")
    for key, coords in projections.items():
        plot_projection(coords, labels, topics, f"{names[key]} dos chunks, coloridos por tópico de conteúdo",
                        subtitle, OUT / f"topicos_{key}.png")
        (OUT / f"qdrant_{key}.json").write_text(json.dumps({
            "limit": len(viz_ids),
            "filter": {"must": [{"key": "amostra_viz", "match": {"value": True}}]},
            "color_by": {"payload": "topico"},
            "algorithm": names[key].replace("-", "").upper(),
        }, indent=2), encoding="utf-8")
    plot_small_multiples(projections["umap"], labels, topics, OUT / "topicos_umap_paineis.png")

    # Tópico dominante por PDF
    by_pdf = {}
    for label, payload in zip(labels, payloads):
        key = payload.get("titulo") or payload.get("file_name_safe")
        by_pdf.setdefault(key, Counter())[int(label)] += 1
    dominant = Counter(counts.most_common(1)[0][0] for counts in by_pdf.values())

    summary = {"collection": args.collection, "chunks": len(ids), "k": k, "silhueta": scores, "topicos": topics}
    (OUT / "topicos.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Tópicos encontrados nos chunks",
        "",
        f"Collection `{args.collection}`: **{len(ids)} chunks** de **{len(by_pdf)} PDFs**, tratados como um único corpus. "
        f"O K-Means agrupou os embeddings (bge-m3, 1024 dimensões) em **{k} tópicos**"
        + (f", escolhido entre 5 e 8 pela maior silhueta ({scores[k]:.3f})." if scores else "."),
        "Nenhuma informação de arquivo ou categoria do arXiv entra no agrupamento.",
        "",
        "Os nomes foram sugeridos pelo LLM local a partir dos termos e trechos de cada grupo"
        + (" e depois revisados à mão (coluna *Sugestão do LLM*)." if reviewed else "."),
        "",
        "| # | Tópico | Sugestão do LLM | Chunks | PDFs com trechos | PDFs onde é dominante | Termos característicos |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for t in topics:
        lines.append(
            f"| {t['cluster_id']} | **{t['nome']}** | {t['nome_llm']} | {t['chunks']} | {t['pdfs']} | {dominant.get(t['cluster_id'], 0)} | "
            f"{', '.join(t['termos'][:8])} |"
        )
    lines += ["", "## Detalhes", ""]
    for t in topics:
        lines += [f"### {t['cluster_id']}. {t['nome']}", "", t["descricao"], "", "Artigos com mais trechos no tópico:", ""]
        lines += [f"- {a['titulo']} ({a['chunks']} chunks)" for a in t["artigos_principais"]]
        lines += [""]
    (OUT / "topicos.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Pronto: arquivos em {OUT}")


if __name__ == "__main__":
    main()
