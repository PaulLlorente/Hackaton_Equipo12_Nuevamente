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

    # utilizamos el extractor para extraer los datos del archivo
    extraccion_completa = documento.parse()
    # extraemos los fragmentos y la metadata
    fragmentos = extraccion_completa.fragmentos
    metadata = extraccion_completa.metadata

    # detectamos las advertencias que puedan haber ocurrido durante la extracción
    advertencias = detectar_advertencias(fragmentos, metadata.total_paginas)
    info_extraccion = ExtraccionInfo(
        advertencias=advertencias,
        parser=documento.parser_version,
        version_parser=documento.parser_name,
    )

    # utilizamos la estructuración para organizar los fragmentos en secciones
    secciones_documento = estructurar_documento(fragmentos)

    # creamos DTO principal que contiene todos los datos necesarios con los datos extraídos y estructurados
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

    # convertimos el documento final a formato JSON y lo devolemos para su procesamiento
    return documento_final.model_dump_json(indent=2)
