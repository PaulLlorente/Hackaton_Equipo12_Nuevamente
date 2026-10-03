from abc import ABC, abstractmethod
from .schema import ResultadoExtraccion, MetadataOrigen


class DocumentExtractor(ABC):
    """
    Clase abstracta que define el contrato para cualquier extractor de documentos.
    """

    def __init__(self, source: bytes, nombre_archivo: str):
        self.source = source
        self.nombre_archivo = nombre_archivo

    @abstractmethod
    def parse(self) -> ResultadoExtraccion:
        """
        Recibe un archivo en memoria y debe devolver la estructura.
        Cada clase hija (PyMuPDF, Docling) implementará esto a su manera.
        """
        pass

    @property
    @abstractmethod
    def extension(self) -> str:
        """Devuelve la extensión o tipo de origen (ej. 'pdf', 'docx')"""
        pass

    @property
    @abstractmethod
    def parser_name(self) -> str:
        pass

    @property
    @abstractmethod
    def parser_version(self) -> str:
        pass
