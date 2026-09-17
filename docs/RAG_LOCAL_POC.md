# Prueba local de chunking y embeddings

## Objetivo

Esta prueba recibe el texto limpio de un PDF, conserva la referencia de página, crea chunks medidos con el tokenizer del modelo y genera embeddings locales. El resultado valida el contrato entre Ingestión, AI y Vector Store antes de conectar Gemini, LangChain o ChromaDB.

## Decisiones

- **Modelo local:** `intfloat/multilingual-e5-small`, multilingüe, 384 dimensiones y ejecución en CPU.
- **Chunking inicial:** 350 tokens con 50 tokens de solapamiento. Cada chunk permanece dentro de una página y el algoritmo prefiere terminar en un párrafo u oración.
- **Recuperación:** consulta con prefijo `query: ` y documento con `passage: `. Los vectores quedan normalizados, por lo que Chroma puede usar distancia coseno y la prueba local puede usar producto punto.
- **Aislamiento:** cada chunk contiene `tenant_id` y `document_id`. Esos campos deben convertirse en filtros obligatorios del retriever.
- **Trazabilidad:** `page_start` y `page_end` permiten mostrar evidencia verificable al usuario.

Estos valores son una línea base. Deben ajustarse con un conjunto de preguntas y métricas de recuperación, no por intuición.

## Contrato con el módulo de extracción

Brayan o Backend debe entregar JSON UTF-8 que cumpla `contracts/clean_document.schema.json`. El ejemplo completo está en `data/samples/clean_document.example.json`.

Reglas de limpieza:

1. Una entrada por documento y una lista ordenada de páginas.
2. Conservar títulos, listas, párrafos, bloques de código y saltos entre párrafos.
3. Quitar caracteres de control, espacios repetidos y cortes de palabra causados por fin de línea.
4. No resumir, traducir ni corregir el contenido técnico.
5. Registrar advertencias de OCR o páginas vacías en `extraction.warnings`.
6. Calcular `source.sha256` desde los bytes del PDF original.

El script también acepta `.txt` para una prueba rápida, aunque ese modo pierde la página original y usa `tenant_id=default`.

## Instalación

Requiere Python 3.11 o superior.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

La primera ejecución descarga el modelo. Las siguientes pueden ejecutarse sin red con `--offline`.

## Construir el índice local

```powershell
python scripts/rag_local.py build `
  --input data/samples/clean_document.example.json `
  --output artifacts/rag-local
```

Salida esperada:

- `chunks.jsonl`: texto y metadatos listos para `ids`, `documents` y `metadatas` de ChromaDB.
- `embeddings.npy`: matriz `float32`; la fila N corresponde a la línea N de `chunks.jsonl`.
- `manifest.json`: modelo, dimensión, forma, configuración y SHA-256 de cada artefacto.

## Probar recuperación

```powershell
python scripts/rag_local.py query `
  --index artifacts/rag-local `
  --text "¿Qué debo hacer cuando la API devuelve 429?" `
  --tenant-id equipo-12-demo `
  --top-k 3 `
  --offline
```

La respuesta JSON incluye puntaje, `chunk_id`, documento, tenant, página y texto recuperado. Para aprobar la prueba, el resultado principal debe corresponder a la página 2 del documento de ejemplo.

## Pruebas automatizadas

```powershell
python -m unittest discover -s tests -v
```

Las pruebas unitarias no descargan modelos. Verifican limpieza, solapamiento, límites de página, alineación entre JSONL y NPY, dimensión, normalización, filtro por tenant y una consulta de recuperación determinista.

## Integración posterior con ChromaDB

Vanessa puede cargar los archivos manteniendo esta correspondencia:

```python
collection.add(
    ids=[chunk["chunk_id"] for chunk in chunks],
    documents=[chunk["text"] for chunk in chunks],
    metadatas=[chunk["metadata"] for chunk in chunks],
    embeddings=embeddings.tolist(),
)
```

Toda consulta debe filtrar al menos por `tenant_id`. Cuando se conozca el documento, también debe filtrar por `document_id`.

## Criterios de aceptación

- El mismo texto y la misma configuración producen los mismos `chunk_id`.
- Ningún chunk supera 350 tokens ni cruza páginas.
- La matriz tiene una fila por chunk, 384 columnas con el modelo propuesto, tipo `float32`, valores finitos y norma L2 aproximada a 1.
- Una consulta devuelve evidencia con página y tenant correctos.
- Después de descargar el modelo una vez, `--offline` funciona sin acceder a servicios externos.

## Resultado de la validación inicial

Validación ejecutada el 17 de septiembre de 2026 con `sentence-transformers 5.7.0` y el ejemplo versionado:

- 3 chunks para 3 páginas, sin cruces de página.
- Matriz de forma `[3, 384]`, tipo `float32`, valores finitos y norma L2 igual a 1 en todas las filas.
- Consulta offline: `¿Qué debo hacer si la API responde con error 429?`.
- Primer resultado: página 2, puntaje `0.842809`, con la instrucción sobre `Retry-After`, espera exponencial y tres reintentos.
- Las 4 pruebas unitarias finalizaron correctamente.

El puntaje sirve para ordenar resultados dentro del mismo modelo; no se usa como probabilidad ni como umbral definitivo de calidad.
