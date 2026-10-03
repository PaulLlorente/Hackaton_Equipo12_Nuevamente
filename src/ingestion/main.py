from datetime import datetime, timezone

# Importamos todos los módulos que necesitamos
from .schema import DocumentoIngestado, ExtraccionInfo
from .structurer import estructurar_documento
from .extraction_warnings import detectar_advertencias
from .factory import ExtractorFactory


def procesar_documento(
    source: bytes, nombre_archivo: str, tenant_id: str, document_id: str
) -> str:

    # recibimos una instancia de un extractor concreto
    documento = ExtractorFactory.get_extractor(source, nombre_archivo)

    extraccion_completa = documento.parse()
    fragmentos = extraccion_completa.fragmentos
    metadata = extraccion_completa.metadata

    advertencias = detectar_advertencias(fragmentos, metadata.total_paginas)
    info_extraccion = ExtraccionInfo(
        advertencias=advertencias,
        parser=documento.parser_version,
        version_parser=documento.parser_name,
    )

    secciones_documento = estructurar_documento(fragmentos)

    documento_final = DocumentoIngestado(
        tenant_id=tenant_id,
        document_id=document_id,
        titulo=metadata.nombre_archivo,
        fecha_ingesta=datetime.now(timezone.utc),
        metadata_origen=metadata,
        extraccion=info_extraccion,
        contenido_estructurado=secciones_documento,
        tipo_origen=documento.extension,
    )

    return documento_final.model_dump_json(indent=2)
