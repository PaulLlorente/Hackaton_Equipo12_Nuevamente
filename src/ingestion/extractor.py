from abc import ABC, abstractmethod
from .schema import ResultadoExtraccion, MetadataOrigen

# clase abstracta que define el contrato para cualquier extractor
class DocumentExtractor(ABC):
    """
    Clase abstracta que define el contrato para cualquier extractor de documentos.
    """

    # constructor que recibe el archivo en memoria y el nombre del archivo
    def __init__(self, source: bytes, nombre_archivo: str):
        self.source = source
        self.nombre_archivo = nombre_archivo

    # método abstracto que debe ser implementado por cada clase hija
    @abstractmethod
    def parse(self) -> ResultadoExtraccion:
        """
        Recibe un archivo en memoria y debe devolver la estructura.
        Cada clase hija (PyMuPDF, Docling) implementará esto a su manera.
        """
        pass

    # propiedades que deben ser implementadas por cada clase hija
    @property
    @abstractmethod
    def extension(self) -> str:
        """Devuelve la extensión o tipo de origen (ej. 'pdf', 'md')"""
        pass

    @property
    @abstractmethod
    def parser_name(self) -> str:
        pass

    @property
    @abstractmethod
    def parser_version(self) -> str:
        pass
