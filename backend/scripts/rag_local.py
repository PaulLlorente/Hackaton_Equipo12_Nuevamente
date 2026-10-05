#!/usr/bin/env python3
"""CLI preliminar para construir y consultar un índice RAG local."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = REPOSITORY_ROOT / "src"
if str(SOURCE_DIR) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIR))

from nuevamente_rag.pipeline import (  # noqa: E402
    DEFAULT_MODEL,
    SentenceTransformerEmbedder,
    build_index,
    load_clean_document,
    search_index,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Chunking por tokens y embeddings locales para NuevaMente"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    build = subparsers.add_parser("build", help="Construye los artefactos del índice local")
    build.add_argument("--input", required=True, type=Path, help="Texto limpio .json o .txt")
    build.add_argument("--output", required=True, type=Path, help="Directorio de salida")
    build.add_argument("--model", default=DEFAULT_MODEL)
    build.add_argument("--chunk-tokens", type=int, default=350)
    build.add_argument("--overlap-tokens", type=int, default=50)
    build.add_argument("--batch-size", type=int, default=16)
    build.add_argument("--device", default="cpu")
    build.add_argument(
        "--offline",
        action="store_true",
        help="Prohíbe descargas y exige que el modelo ya esté en caché",
    )

    query = subparsers.add_parser("query", help="Ejecuta recuperación semántica de prueba")
    query.add_argument("--index", required=True, type=Path)
    query.add_argument("--text", required=True)
    query.add_argument("--model", default=DEFAULT_MODEL)
    query.add_argument("--top-k", type=int, default=3)
    query.add_argument("--tenant-id")
    query.add_argument("--batch-size", type=int, default=16)
    query.add_argument("--device", default="cpu")
    query.add_argument("--offline", action="store_true")

    return parser


def main() -> int:
    args = _parser().parse_args()
    embedder = SentenceTransformerEmbedder(
        args.model,
        device=args.device,
        local_files_only=args.offline,
        batch_size=args.batch_size,
    )

    if args.command == "build":
        document = load_clean_document(args.input)
        manifest = build_index(
            document,
            args.output,
            embedder,
            chunk_tokens=args.chunk_tokens,
            overlap_tokens=args.overlap_tokens,
        )
        print(json.dumps(manifest, ensure_ascii=False, indent=2))
        return 0

    results = search_index(
        args.index,
        args.text,
        embedder,
        top_k=args.top_k,
        tenant_id=args.tenant_id,
    )
    print(json.dumps({"query": args.text, "results": results}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
