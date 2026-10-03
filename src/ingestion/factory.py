from pathlib import Path

from .extractor import DocumentExtractor
from .extractors.extractorPDF import ExtractorPDF


class ExtractorFactory:
    @staticmethod
    def get_extractor(source: bytes, nombre_archivo: str) -> DocumentExtractor:

        extension = Path(
            nombre_archivo
        ).suffix.lower()  # Obtenemos la extensión del archivo

        match extension:
            case ".pdf":
                return ExtractorPDF(source, nombre_archivo)
