"""Ingere em lote os PDFs do arXiv usando o mesmo pipeline do upload do app.

Cada PDF passa por MinIO -> DocumentProcessor (chunks) -> QdrantVectorStore.
Os embeddings vêm do modelo configurado na collection (padrão: 'local', Ollama).
O upload web limita arquivos a 16 MB; este script não tem esse limite.

Uso (dentro do contêiner do app):
    python scripts/ingest_arxiv_pdfs.py --collection artigos_ia
"""

import argparse
import contextlib
import io
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from qdrant_client.models import FieldCondition, Filter, MatchValue

from src.debug_utils import charset_debugger
from src.document_processor import DocumentProcessor
from src.storage import StorageManager
from src.vector_store import QdrantVectorStore


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf-dir", type=Path, default=Path("/data/pdfs"))
    parser.add_argument("--manifest", type=Path, default=Path("/data/manifest.json"))
    parser.add_argument("--collection", default="artigos_ia")
    parser.add_argument("--embedding-model", default="local")
    parser.add_argument("--limit", type=int, default=0, help="0 = todos os PDFs")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    # O debug de charset imprime várias linhas por chunk; em lote isso só atrasa
    charset_debugger.log_debug = lambda *a, **k: None

    manifest = {}
    if args.manifest.exists():
        rows = json.loads(args.manifest.read_text(encoding="utf-8"))
        manifest = {f"{row['arxiv_id']}.pdf": row for row in rows}

    vector_store = QdrantVectorStore()
    client = vector_store.client
    existing = {c.name for c in client.get_collections().collections}
    if args.collection not in existing:
        vector_store.create_collection(
            args.collection,
            args.embedding_model,
            description="100 artigos recentes de IA do arXiv (cs.AI, cs.LG, cs.CL, cs.CV, cs.RO)",
        )

    processor = DocumentProcessor()
    storage = StorageManager()

    pdfs = sorted(args.pdf_dir.glob("*.pdf"))
    if args.limit:
        pdfs = pdfs[: args.limit]

    started = time.time()
    total_chunks = 0
    for index, pdf in enumerate(pdfs, start=1):
        by_file = Filter(must=[FieldCondition(key="file_name_safe", match=MatchValue(value=pdf.name))])
        if client.count(args.collection, count_filter=by_file, exact=True).count:
            print(f"[{index}/{len(pdfs)}] {pdf.name}: já ingerido, pulando", flush=True)
            continue

        file_started = time.time()
        # O pipeline do app imprime cada chunk; guardamos a saída e só mostramos em caso de erro
        captured = io.StringIO()
        try:
            with contextlib.redirect_stdout(captured):
                upload = storage.upload_document(str(pdf), topic=args.collection)
                result = processor.process_document(str(pdf), enhance=False)
                for chunk in result["chunks"]:
                    chunk.metadata["minio_path"] = upload["original_path"]
                    chunk.metadata["minio_object"] = upload["object_name"]
                vector_store.insert_documents(args.collection, result["chunks"])
        except Exception as error:
            print(captured.getvalue()[-2000:], file=sys.stderr)
            print(f"[{index}/{len(pdfs)}] {pdf.name}: ERRO {error}", flush=True)
            continue

        row = manifest.get(pdf.name)
        if row:
            client.set_payload(
                args.collection,
                payload={"titulo": row["title"], "arxiv_id": row["arxiv_id"]},
                points=by_file,
            )

        chunks = len(result["chunks"])
        total_chunks += chunks
        print(
            f"[{index}/{len(pdfs)}] {pdf.name}: {chunks} chunks em {time.time() - file_started:.1f}s",
            flush=True,
        )

    print(f"Concluído: {total_chunks} chunks novos em {time.time() - started:.0f}s", flush=True)


if __name__ == "__main__":
    main()
