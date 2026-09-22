from __future__ import annotations

import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from nuevamente_rag.pipeline import (  # noqa: E402
    CleanDocument,
    DocumentSection,
    TokenAwareChunker,
    build_index,
    load_clean_document,
    normalize_extracted_text,
    search_index,
)
from src.ingestion.main import procesar_documento  # noqa: E402


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

    def test_contract_preserves_sections_source_and_extraction_metadata(self) -> None:
        document = load_clean_document(ROOT / "data/samples/clean_document.example.json")
        self.assertEqual(document.document_id, "manual-demo-nuevamente")
        self.assertEqual(document.tenant_id, "equipo-12-demo")
        self.assertEqual(document.source["total_pages"], 3)
        self.assertEqual(document.extraction["parser"], "PyMuPDF")
        self.assertEqual(len(document.sections), 3)
        self.assertEqual(document.sections[1].section_title, "Límites y reintentos")
        self.assertEqual(document.sections[1].page_start, 2)
        self.assertTrue(document.sections[1].text.startswith("Límites y reintentos"))

    def test_invalid_page_range_is_rejected(self) -> None:
        source = json.loads(
            (ROOT / "data/samples/clean_document.example.json").read_text(encoding="utf-8")
        )
        source["contenido_estructurado"][0]["pagina_inicio"] = 2
        source["contenido_estructurado"][0]["pagina_fin"] = 1
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "invalid.json"
            path.write_text(json.dumps(source), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "pagina_fin"):
                load_clean_document(path)

    def test_chunking_has_overlap_and_never_crosses_sections(self) -> None:
        text = " ".join(f"palabra{i}." for i in range(90))
        document = CleanDocument(
            document_id="doc-1",
            tenant_id="tenant-1",
            title="Prueba",
            language="es",
            sections=(
                DocumentSection(0, 1, "Sección extensa", 1, 2, text),
                DocumentSection(1, 2, "Otra sección", 3, 3, "otra evidencia"),
            ),
            source={"total_pages": 3},
            extraction={"advertencias": []},
        )
        chunks = TokenAwareChunker(
            RegexTokenizer(), chunk_tokens=32, overlap_tokens=8, boundary_window_ratio=0
        ).split(document)
        first_section = [chunk for chunk in chunks if chunk.section_index == 0]
        self.assertGreater(len(first_section), 1)
        self.assertEqual(
            first_section[1].token_start,
            first_section[0].token_end - 8,
        )
        self.assertTrue(all(chunk.page_start == 1 for chunk in first_section))
        self.assertTrue(all(chunk.page_end == 2 for chunk in first_section))
        self.assertTrue(all(chunk.token_count <= 32 for chunk in chunks))

    def test_artifacts_are_chroma_compatible_and_queryable(self) -> None:
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
            self.assertEqual(manifest["document"]["section_count"], 3)
            self.assertEqual(manifest["embeddings"]["dtype"], "float32")
            self.assertEqual(chunks[1]["metadata"]["section_title"], "Límites y reintentos")

            results = search_index(
                output,
                "¿Qué hago ante un error 429 y cómo reintento?",
                embedder,
                top_k=1,
                tenant_id="equipo-12-demo",
            )
            self.assertEqual(results[0]["page_start"], 2)
            self.assertEqual(results[0]["section_title"], "Límites y reintentos")
            self.assertIn("429", results[0]["text"])

    def test_real_ingestion_output_flows_into_rag_chunker(self) -> None:
        pdf = ROOT / "docs/test_pdf/Guia de Usuario - Oracle AI Success Navigator.pdf"
        result = procesar_documento(
            ruta_archivo=str(pdf),
            tenant_id="oracle_hackathon_test",
            document_id="doc_test_001",
        )
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "resultado_ingestion.json"
            path.write_text(result, encoding="utf-8")
            document = load_clean_document(path)
            chunks = TokenAwareChunker(
                RegexTokenizer(), chunk_tokens=64, overlap_tokens=8
            ).split(document)

        self.assertGreater(len(document.sections), 30)
        self.assertGreater(len(chunks), len(document.sections))
        self.assertTrue(all(chunk.tenant_id == "oracle_hackathon_test" for chunk in chunks))
        self.assertTrue(any(chunk.page_end > chunk.page_start for chunk in chunks))
        self.assertTrue(any(chunk.section_title for chunk in chunks))


if __name__ == "__main__":
    unittest.main()
