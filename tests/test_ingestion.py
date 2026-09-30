import json
from pathlib import Path

import jsonschema

from src.ingestion.main import procesar_documento


def test_extraccion_documento():
    pdf_bytes = (
        Path(__file__).parent.parent
        / "docs"
        / "test_pdf"
        / "Guia de Usuario - Oracle AI Success Navigator.pdf"
    ).read_bytes()  # bytes (archivo cargado en memoria)

    ruta_schema = (
        Path(__file__).parent.parent / "contracts" / "clean_document.schema.json"
    )

    # 1. Ejecutamos la función principal
    json_resultado = procesar_documento(
        source=pdf_bytes,
        tenant_id="oracle_hackathon_test",
        document_id="doc_test_001",
        nombre_archivo="Guia de Usuario - Oracle AI Success Navigator.pdf",
    )

    # 2. Comprobamos que haya resultado
    assert json_resultado, "La función no devolvió ningún JSON"

    # 3. Convertimos JSON string → dict
    resultado_dict = json.loads(json_resultado)

    # 4. Validaciones básicas
    assert resultado_dict["tipo_origen"] == "pdf"
    assert "schema_version" in resultado_dict
    assert len(resultado_dict["contenido_estructurado"]) > 0
    assert resultado_dict["metadata_origen"]["total_paginas"] > 0

    # 5. Cargamos el contrato
    with open(ruta_schema, encoding="utf-8") as archivo:
        schema = json.load(archivo)

    # 6. Validamos contra JSON Schema
    jsonschema.validate(
        instance=resultado_dict,
        schema=schema,
    )

    # 7. Guardamos el resultado generado
    ruta_salida = Path(__file__).parent / "resultado_test_ingestion.json"

    ruta_salida.write_text(
        json_resultado,
        encoding="utf-8",
    )
