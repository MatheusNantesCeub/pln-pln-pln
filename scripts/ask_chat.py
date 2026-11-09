"""Faz perguntas ao chat RAG (/api/chat) e registra respostas e fontes.

Cada pergunta tem um gabarito tirado do resumo do artigo no arXiv, para
conferir se a resposta veio do nosso conteúdo. A última pergunta está fora
do corpus: o esperado é o modelo admitir que não encontrou a informação.

Uso (no host, com o app rodando):
    .venv/Scripts/python.exe scripts/ask_chat.py
"""

import argparse
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent

QUESTIONS = [
    {
        "pergunta": "Qual HOTA o ARC-SORT alcança no teste do SportsMOT e a quantos quadros por segundo ele roda?",
        "gabarito": "81,82 HOTA no SportsMOT; cerca de 50 FPS em uma RTX 3060 de notebook (artigo 2610.22306).",
    },
    {
        "pergunta": "No RAG-RST, quanto o F1 de nuclearidade e de relação melhora em relação ao LLM sem exemplos recuperados?",
        "gabarito": "Nuclearidade de 0,794 para 0,846 F1 e relação de 0,738 para 0,788 F1, sem treinamento (2610.22150).",
    },
    {
        "pergunta": "Como o artigo sobre RAG privado protege o banco de documentos contra ataques de extração?",
        "gabarito": "Aplica a mesma projeção aleatória aos embeddings do datastore e das consultas (2610.22297).",
    },
    {
        "pergunta": "Quanto tempo os agentes Gemini 4 Argon levaram para derrotar o Ender Dragon no Minecraft e quantas vezes morreram?",
        "gabarito": "27 horas e 14 minutos, 605 mortes e 2.783 programas escritos (2610.22319).",
    },
    {
        "pergunta": "Qual taxa de alcance o PSA-PPO obteve na colheita robótica de alface hidropônica e em que robô foi testado?",
        "gabarito": "94,7% de alcance em 150 alvos, braço UR10e; 86,1% de colheita completa (2610.22337).",
    },
    {
        "pergunta": "Quantas consultas com premissas falhas o benchmark PremiseSQL contém?",
        "gabarito": "1.800 consultas falhas em quatro categorias, mais as 1.800 originais (2610.22158).",
    },
    {
        "pergunta": "Que modelo foi especializado para a variante Masewalkopa do náuatle e qual chrF++ ele obteve?",
        "gabarito": "Um checkpoint mT5-large (modelo LoRA-v9c-b), 58,46 chrF++ no dev (2610.22110).",
    },
    {
        "pergunta": "Qual é a receita tradicional do pão de queijo mineiro?",
        "gabarito": "Fora do corpus: o modelo deve dizer que o contexto não traz essa informação.",
    },
]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default="http://localhost:5000")
    parser.add_argument("--collection", default="artigos_ia")
    parser.add_argument("--output", type=Path, default=ROOT / "visualizacoes" / "perguntas_chat.md")
    args = parser.parse_args()

    lines = [
        "# Perguntas ao chat RAG local",
        "",
        f"Collection `{args.collection}` · LLM e embeddings rodando localmente no Ollama · "
        "gabaritos extraídos dos resumos do arXiv.",
        "",
    ]
    for number, item in enumerate(QUESTIONS, start=1):
        started = time.time()
        # Sem session_id o app cria uma sessão nova: o histórico de uma pergunta não contamina a outra
        result = requests.post(
            f"{args.url}/api/chat",
            json={"message": item["pergunta"], "collection_names": [args.collection]},
            timeout=600,
        ).json()
        elapsed = time.time() - started
        answer = result.get("response") or result.get("error", "")
        sources = result.get("sources", [])
        print(f"\n[{number}] {item['pergunta']}\n→ {answer}\n({elapsed:.1f}s, {result.get('processed_by')})")

        lines += [
            f"## {number}. {item['pergunta']}",
            "",
            f"**Gabarito:** {item['gabarito']}",
            "",
            "**Resposta do chat:**",
            "",
            "> " + answer.strip().replace("\n", "\n> "),
            "",
            f"*Processado por `{result.get('processed_by')}` em {elapsed:.1f}s.* Trechos recuperados:",
            "",
        ]
        for source in sources:
            title = source.get("titulo") or source.get("file_name")
            lines.append(
                f"- {title} — `{source.get('file_name')}` · similaridade {source.get('score', 0):.3f}"
                + (f" · tópico *{source['topico']}*" if source.get("topico") else "")
            )
        lines.append("")

    args.output.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nRelatório: {args.output}")


if __name__ == "__main__":
    main()
