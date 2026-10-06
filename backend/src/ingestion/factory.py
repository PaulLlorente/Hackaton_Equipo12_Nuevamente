from pathlib import Path

from .extractor import DocumentExtractor
from .extractors.extractorPDF import ExtractorPDF
from .extractors.extractorMD import ExtractorMarkdown


class ExtractorFactory:
    """
    Módulo que se encarga de crear instancias de
    DocumentExtractor según la extensión del archivo
    """

    # Método estático que crea una instancia de DocumentExtractor según la extensión del archivo
    @staticmethod
    def get_extractor(source: bytes, nombre_archivo: str) -> DocumentExtractor:

        extension = Path(
            nombre_archivo
        ).suffix.lower()  # Obtenemos la extensión del archivo

        match extension:
            case ".pdf":
                return ExtractorPDF(source, nombre_archivo)
            case ".md":  # Si es un archivo Markdown
                return ExtractorMarkdown(source, nombre_archivo)
            case _:
                raise ValueError(f"Formato no soportado: {extension}")
