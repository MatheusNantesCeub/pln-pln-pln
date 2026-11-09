"""Remove da collection os chunks que atrapalham o RAG, a partir dos tópicos do cluster_topics.py.

- Referências Bibliográficas: listas "Autor et al. (2023). Título..." que casam com
  perguntas genéricas pelos títulos citados e ocupam o contexto sem trazer resposta.
- Casos Clínicos Pediátricos: o Apêndice C do artigo AI Consilium, que reproduz por
  extenso um laudo médico. O corpo do artigo (método e resultados) é mantido.

Antes de apagar, cria um snapshot da collection no Qdrant (backup).

Uso (no host, depois do cluster_topics.py):
    .venv/Scripts/python.exe scripts/limpar_corpus.py --dry-run
    .venv/Scripts/python.exe scripts/limpar_corpus.py
"""

import argparse
import os

from qdrant_client import QdrantClient
from qdrant_client.models import FieldCondition, Filter, FilterSelector, MatchAny, MatchValue

TOPICOS_REMOVIDOS = ["Referências Bibliográficas", "Casos Clínicos Pediátricos"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--url", default="http://localhost:6333")
    parser.add_argument("--api-key", default=os.getenv("QDRANT_API_KEY", "plnCEUB12025-SK2025"))
    parser.add_argument("--collection", default="artigos_ia")
    parser.add_argument("--topicos", nargs="+", default=TOPICOS_REMOVIDOS)
    parser.add_argument("--dry-run", action="store_true", help="só conta, não apaga")
    args = parser.parse_args()

    client = QdrantClient(url=args.url, api_key=args.api_key)
    alvo = Filter(must=[FieldCondition(key="topico", match=MatchAny(any=args.topicos))])
    sem_metadata = Filter(must_not=[FieldCondition(key="name", match=MatchValue(value=args.collection))])

    antes = client.count(args.collection, count_filter=sem_metadata).count
    for topico in args.topicos:
        n = client.count(
            args.collection,
            count_filter=Filter(must=[FieldCondition(key="topico", match=MatchValue(value=topico))]),
        ).count
        print(f"{topico}: {n} chunks")
    total = client.count(args.collection, count_filter=alvo).count
    print(f"Total a remover: {total} de {antes}")
    if args.dry_run or total == 0:
        return

    snapshot = client.create_snapshot(args.collection)
    print(f"Snapshot de backup: {snapshot.name}")

    client.delete(args.collection, points_selector=FilterSelector(filter=alvo), wait=True)
    depois = client.count(args.collection, count_filter=sem_metadata).count
    print(f"Chunks restantes: {depois}")

    # Mantém o document_count do ponto de metadata coerente com a collection
    client.set_payload(
        args.collection,
        payload={"document_count": str(depois)},
        points=Filter(must=[FieldCondition(key="name", match=MatchValue(value=args.collection))]),
    )


if __name__ == "__main__":
    main()
