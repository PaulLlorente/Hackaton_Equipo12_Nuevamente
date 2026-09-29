from pathlib import Path
from datetime import datetime, timezone

# Importamos todos los módulos que necesitamos
from .schema import DocumentoIngestado, ExtraccionInfo
from .extractor import DocumentExtractor
from .structurer import estructurar_documento
from .extraction_warnings import detectar_advertencias


def procesar_documento(
    source: bytes, nombre_archivo: str, tenant_id: str, document_id: str
) -> str:

    with DocumentExtractor(source, nombre_archivo) as extractor:
        metadata = extractor.get_metadata()
        fragmentos = extractor.extraer_fragmentos()

    advertencias = detectar_advertencias(fragmentos, metadata.total_paginas)
    info_extraccion = ExtraccionInfo(advertencias=advertencias)

    secciones_documento = estructurar_documento(fragmentos)

    documento_final = DocumentoIngestado(
        tenant_id=tenant_id,
        document_id=document_id,
        titulo=metadata.nombre_archivo,
        fecha_ingesta=datetime.now(timezone.utc),
        metadata_origen=metadata,
        extraccion=info_extraccion,
        contenido_estructurado=secciones_documento,
    )

    return documento_final.model_dump_json(indent=2)
