from typing import List
from pydantic import BaseModel, Field
from datetime import datetime, timezone
import pymupdf


# 1. Metadatos del archivo original
class MetadataOrigen(BaseModel):
    nombre_archivo: str
    total_paginas: int
    sha256: str


# 2. Las advertencias de extracción (Páginas sin texto, etc.)
class Advertencia(BaseModel):
    codigo: str
    pagina: int
    mensaje: str
    requiere_ocr: bool


# 3. Información del proceso de extracción
class ExtraccionInfo(BaseModel):
    parser: str = "PyMuPDF"  # Por defecto, usamos PyMuPDF
    version_parser: str = pymupdf.__version__
    # Versión de PyMuPDF
    advertencias: List[Advertencia] = Field(
        default_factory=list
    )  # Array vacío por defecto


# 4. El contenido de cada sección (nivel_encabezado, titulo_seccion, texto, pagina_inicio, pagina_fin)
class SeccionContenido(BaseModel):
    """
    Representa una sección estructurada del documento.

    nivel_encabezado:
        0 = contenido sin encabezado
        1 = H1
        2 = H2
        3 = H3
        etc.
    """

    nivel_encabezado: int = Field(
        ge=0
    )  # Nivel de encabezado, 0 significa sin encabezado
    titulo_seccion: str | None = (
        None  # Permite que el título de la sección sea opcional
    )
    texto: str
    pagina_inicio: int
    pagina_fin: int


# 5. Fragmento de texto individual (texto, tamaño_fuente, pagina)
class FragmentoTexto(BaseModel):
    texto: str
    tamano_fuente: float
    pagina: int
    negrita: bool = False  # Por defecto, asumimos que el texto no está en negrita
    fuente: str | None = None  # Permite que el atributo sea opcional
    bbox: tuple[float, float, float, float] | None = (
        None  # Posición del fragmento dentro de la página: (x0, y0, x1, y1)
    )


# 6. El DTO principal (El JSON completo que le entregarre a mi compañera Vanessa)
class DocumentoIngestado(BaseModel):
    schema_version: str = "1.0"  # Versión del esquema
    tenant_id: str
    document_id: str
    titulo: str
    idioma: str = "es"  # Por defecto, asumimos español
    tipo_origen: str = "pdf"  # Por defecto, asumimos pdf
    fecha_ingesta: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata_origen: MetadataOrigen
    extraccion: ExtraccionInfo = Field(default_factory=ExtraccionInfo)
    contenido_estructurado: List[SeccionContenido] = Field(default_factory=list)
