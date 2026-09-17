from __future__ import annotations

import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from nuevamente_rag.pipeline import (  # noqa: E402
    CleanDocument,
    Page,
    TokenAwareChunker,
    build_index,
    load_clean_document,
    normalize_extracted_text,
    search_index,
)


class RegexTokenizer:
    def __call__(self, text: str, **_: object) -> dict[str, list[tuple[int, int]]]:
        return {"offset_mapping": [match.span() for match in re.finditer(r"\S+", text)]}


class DeterministicEmbedder:
    model_name = "test/deterministic"
    tokenizer = RegexTokenizer()
    dimension = 3

    def _vector(self, text: str) -> np.ndarray:
        lower = text.lower()
        vector = np.array(
            [
                lower.count("token") + lower.count("autentic"),
                lower.count("reintento") + lower.count("429"),
                lower.count("cifrado") + lower.count("datos"),
            ],
            dtype=np.float32,
        )
        if not vector.any():
            vector[0] = 1.0
        return vector / np.linalg.norm(vector)

    def embed_documents(self, texts: list[str]) -> np.ndarray:
        return np.vstack([self._vector(text) for text in texts])

    def embed_query(self, text: str) -> np.ndarray:
        return self._vector(text)


class PipelineTests(unittest.TestCase):
    def test_normalization_preserves_paragraphs_and_repairs_hyphenation(self) -> None:
        raw = "  Configura-\nción   inicial\r\n\r\n\r\nSegundo  párrafo.\x00 "
        self.assertEqual(
            normalize_extracted_text(raw),
            "Configuración inicial\n\nSegundo párrafo.",
        )

    def test_json_contract_and_page_metadata_are_preserved(self) -> None:
        document = load_clean_document(ROOT / "data/samples/clean_document.example.json")
        self.assertEqual(document.document_id, "manual-demo-nuevamente")
        self.assertEqual(document.tenant_id, "equipo-12-demo")
        self.assertEqual([page.page_number for page in document.pages], [1, 2, 3])

    def test_chunking_has_overlap_and_never_crosses_pages(self) -> None:
        text = " ".join(f"palabra{i}." for i in range(90))
        document = CleanDocument(
            document_id="doc-1",
            tenant_id="tenant-1",
            title="Prueba",
            language="es",
            pages=(Page(1, text), Page(2, "otra página con evidencia")),
            source={},
            extraction={},
        )
        chunks = TokenAwareChunker(
            RegexTokenizer(), chunk_tokens=32, overlap_tokens=8, boundary_window_ratio=0
        ).split(document)
        page_one = [chunk for chunk in chunks if chunk.page_start == 1]
        self.assertGreater(len(page_one), 1)
        self.assertEqual(page_one[1].token_start, page_one[0].token_end - 8)
        self.assertTrue(all(chunk.page_start == chunk.page_end for chunk in chunks))
        self.assertTrue(all(chunk.token_count <= 32 for chunk in chunks))

    def test_artifacts_are_compatible_and_queryable(self) -> None:
        document = load_clean_document(ROOT / "data/samples/clean_document.example.json")
        embedder = DeterministicEmbedder()
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            manifest = build_index(
                document,
                output,
                embedder,
                chunk_tokens=64,
                overlap_tokens=8,
            )
            vectors = np.load(output / "embeddings.npy", allow_pickle=False)
            chunks = [
                json.loads(line)
                for line in (output / "chunks.jsonl").read_text(encoding="utf-8").splitlines()
            ]
            self.assertEqual(vectors.shape, (len(chunks), 3))
            self.assertEqual(manifest["embeddings"]["dtype"], "float32")
            self.assertEqual(manifest["vector_store_mapping"]["ids"], "chunks.jsonl[].chunk_id")

            results = search_index(
                output,
                "¿Qué hago ante un error 429 y cómo reintento?",
                embedder,
                top_k=1,
                tenant_id="equipo-12-demo",
            )
            self.assertEqual(results[0]["page_start"], 2)
            self.assertIn("429", results[0]["text"])


if __name__ == "__main__":
    unittest.main()
