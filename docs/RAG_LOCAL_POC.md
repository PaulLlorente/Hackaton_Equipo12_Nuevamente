# Prueba local de chunking y embeddings

## Objetivo

Este módulo consume el contrato v1.0 producido por Ingestión, divide cada sección extensa en chunks medidos con el tokenizer del modelo y genera embeddings locales. La salida sirve como frontera estable para que RAG Data cargue los vectores y metadatos en ChromaDB.

## Flujo entre módulos

```text
PDF
  -> src/ingestion
  -> JSON v1.0 con contenido_estructurado
  -> src/nuevamente_rag
  -> chunks.jsonl + embeddings.npy + manifest.json
  -> ChromaDB
```

Responsabilidades:

- **Ingestión:** extrae el PDF, detecta secciones, calcula SHA-256 y reporta advertencias.
- **AI:** valida el contrato, aplica la política de chunking y comprueba la recuperación local.
- **RAG Data:** genera los embeddings definitivos y persiste chunks y metadatos en ChromaDB.

## Contrato de entrada

El contrato oficial está en `contracts/clean_document.schema.json`. El ejemplo mínimo reproducible está en `data/samples/clean_document.example.json`.

Campos utilizados por el chunker:

- `tenant_id` y `document_id` para aislamiento y trazabilidad.
- `titulo` e `idioma` para describir el documento.
- `metadata_origen.sha256` para identificar el PDF original.
- `extraccion.advertencias` para informar degradaciones u OCR pendiente.
- `contenido_estructurado[].nivel_encabezado` y `titulo_seccion` para contexto semántico.
- `pagina_inicio` y `pagina_fin` para citar la evidencia original.

El título de la sección se antepone al texto antes de generar embeddings. Las secciones vacías que solo contienen un título pueden producir un chunk de título; los elementos completamente vacíos se omiten.

## Política de chunking

- Modelo local: `intfloat/multilingual-e5-small`.
- Tamaño máximo inicial: 350 tokens.
- Solapamiento: 50 tokens.
- Cada sección se procesa por separado.
- El algoritmo prefiere terminar en un límite de párrafo u oración.
- Todos los chunks conservan `section_title`, `heading_level`, `page_start` y `page_end`.
- Los documentos usan el prefijo `passage: ` y las consultas `query: `.
- Los vectores se normalizan a norma L2 igual a 1.

Una sección puede producir uno o varios chunks. Un chunk nunca mezcla contenido de dos secciones distintas.

## Instalación

Requiere Python 3.11 o superior.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

La primera construcción descarga el modelo. Las consultas posteriores pueden ejecutarse sin red con `--offline`.

## Ejecutar todas las pruebas

```powershell
python -m pytest -q
```

Las pruebas comprueban tanto Ingestión como RAG e incluyen un recorrido real:

```text
PDF de prueba -> JSON v1.0 -> secciones -> chunks
```

## Construir el índice de ejemplo

```powershell
python scripts/rag_local.py build `
  --input data/samples/clean_document.example.json `
  --output artifacts/rag-local
```

Salida:

- `chunks.jsonl`: texto y metadatos listos para ChromaDB.
- `embeddings.npy`: matriz `float32`; la fila N corresponde a la línea N de `chunks.jsonl`.
- `manifest.json`: modelo, dimensión, configuración, forma y SHA-256 de los artefactos.

## Probar recuperación offline

```powershell
python scripts/rag_local.py query `
  --index artifacts/rag-local `
  --text "¿Qué debo hacer cuando la API devuelve 429?" `
  --tenant-id equipo-12-demo `
  --top-k 1 `
  --offline
```

El primer resultado esperado corresponde a `Límites y reintentos`, página 2.

## Integración con ChromaDB

La correspondencia de los artefactos es:

```python
collection.add(
    ids=[chunk["chunk_id"] for chunk in chunks],
    documents=[chunk["text"] for chunk in chunks],
    metadatas=[chunk["metadata"] for chunk in chunks],
    embeddings=embeddings.tolist(),
)
```

Cada `metadata` contiene como mínimo:

```json
{
  "tenant_id": "empresa_x",
  "document_id": "doc_001",
  "section_index": 4,
  "section_title": "Subredes públicas y privadas",
  "heading_level": 2,
  "page_start": 2,
  "page_end": 3,
  "chunk_index": 7
}
```

Toda consulta de producción debe filtrar por `tenant_id`. Cuando se conoce el documento, también debe filtrar por `document_id`.

## Criterios de aceptación

- El JSON se valida contra el contrato v1.0 antes del chunking.
- Una sección extensa se divide sin mezclarse con otra sección.
- El título, nivel y rango de páginas se conservan en cada chunk.
- La matriz contiene una fila por chunk y valores finitos normalizados.
- La consulta local devuelve evidencia con tenant, sección y páginas correctos.
- El JSON real generado desde el PDF de prueba atraviesa Ingestión y llega al chunker sin adaptaciones manuales.
