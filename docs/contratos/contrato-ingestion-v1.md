# Decisiones del modulo de ingestion

**Contrato:** v1.0
**Ultima revision:** 2026-09-20
**Responsable de mi modulo:** Brayan Camilo Lopez (`Discord: @arctica47`)
**Consumidores de mi salida:** AI Engineer, RAG Data/Vector Store y API Core
**Archivo actualizable:** uso este documento para registrar mis decisiones; no reemplaza el codigo.

## 1. Alcance y responsabilidad

Mi modulo recibe un archivo tecnico, extrae su contenido, calcula metadatos,
detecta problemas y prepara una salida estructurada para el siguiente modulo.

En el repositorio, mi rol aparece como **Full Stack Developer - Modulo de
Ingestion**. La asignacion me pide extraer PDF y Markdown y preparar el contenido
para AI. La issue #5 esta asignada en GitHub a Cristhian Pereira para chunking y
embeddings; mi modulo es una dependencia de esa issue y el PR #8 espera recibir
mi documento limpio.

Mi modulo **no** hace chunking, embeddings, consultas vectoriales, prompts,
ChromaDB, OCI ni endpoints FastAPI. Es como una oficina de recepcion: reviso,
organizo y etiqueto el documento; no decido aun como se almacena ni como se
consulta.

## 2. Estado actual

| Area | Estado | Evidencia local | Proximo paso |
| --- | --- | --- | --- |
| Extraccion PDF | Implementada y validada | `src/ingestion/extractor.py` | Validar con mas PDFs tecnicos |
| Parser PDF | PyMuPDF confirmado | `requirements.txt`, `schema.py` | Confirmar con PDFs escaneados |
| Hash del archivo | Implementado | `src/ingestion/hashing.py` | Verificado contra archivo conocido |
| Modelo de salida | Definido con Pydantic | `src/ingestion/schema.py` | Funcional |
| Advertencias | Implementadas | `extraction_warnings.py` detecta paginas sin texto | Agregar errores y casos OCR |
| Estructuracion por encabezados | Implementada y refinada | `src/ingestion/structurer.py` | Funcional con extraccion por bloques |
| Orquestacion del flujo | Implementada y funcional | `src/ingestion/main.py` | Funcional |
| Prueba automatica | Implementada con pytest y JSON Schema | `tests/test_ingestion.py` valida JSON, secciones, paginas y contrato | Ejecutada y verde |
| Contrato JSON formal | Implementado | `contracts/clean_document.schema.json` | Compartir con Vanessa y Pereira |
| Multi-parser | Diseñado, no implementado | Contrato comun documentado | Terminar PDF primero |

Este estado distingue entre el codigo que ya escribi y el comportamiento que ya
comprobe. El flujo principal puede construir el JSON por secciones, la prueba
comprueba el contrato completo y el schema JSON esta listo para que el consumidor
de AI lo use como referencia.

## 3. Estructura actual del paquete

| Archivo | Responsabilidad | Analogia |
| --- | --- | --- |
| `schema.py` | Define las estructuras de datos y el documento final | Los formularios oficiales que todos deben llenar |
| `extractor.py` | Abre el PDF y produce un fragmento por bloque con pagina, fuente y tamaño | El lector que transcribe lo que encuentra respetando los parrafos |
| `hashing.py` | Calcula la huella SHA-256 del archivo original | La huella digital del documento |
| `extraction_warnings.py` | Detecta paginas que no produjeron texto | El tablero que enciende una alerta |
| `structurer.py` | Agrupa fragmentos y estima niveles de encabezado | El archivista que separa el texto por temas |
| `main.py` | Coordina el flujo y serializa el resultado | El coordinador que pasa el expediente por cada ventanilla |
| `__init__.py` | Marca el directorio como paquete Python | La etiqueta que permite importar el paquete |
| `tests/test_ingestion.py` | Ejecuta la prueba con pytest y valida el JSON contra el schema formal | El simulacro de entrega del expediente ante un auditor |
| `contracts/clean_document.schema.json` | Contrato formal en JSON Schema que cualquier lenguaje puede validar | El reglamento publico escrito que todos los equipos pueden leer |

La separacion es correcta para el MVP: cada pieza tiene una responsabilidad
comprensible y `main.py` no contiene los detalles de lectura del PDF.

## 4. Contrato de salida acordado

Mi salida debe ser un JSON normalizado y organizado por secciones:

```json
{
  "schema_version": "1.0",
  "tenant_id": "empresa_x",
  "document_id": "doc_001",
  "titulo": "Arquitectura de Redes VCN en OCI",
  "idioma": "es",
  "tipo_origen": "pdf",
  "fecha_ingesta": "2026-09-17T17:20:00Z",
  "metadata_origen": {
    "nombre_archivo": "vcn_oracle.pdf",
    "total_paginas": 12,
    "sha256": "hash_sha256_real"
  },
  "extraccion": {
    "parser": "PyMuPDF",
    "version_parser": "version_instalada",
    "advertencias": []
  },
  "contenido_estructurado": [
    {
      "nivel_encabezado": 1,
      "titulo_seccion": "Introduccion a VCN",
      "texto": "Una Virtual Cloud Network es tu red privada...",
      "pagina_inicio": 1,
      "pagina_fin": 1
    }
  ]
}
```

Los nombres son el contrato. No debo copiar los valores del ejemplo como datos
reales. En particular, debo calcular `sha256` sobre el archivo original y debo
obtener `version_parser` de la libreria instalada.

### Decisiones de los campos

- `tenant_id` separa los datos de una empresa de otra.
- `document_id` permite rastrear un documento aunque cambie su nombre.
- `metadata_origen` describe el archivo antes de limpiarlo.
- `contenido_estructurado` conserva contexto para que AI pueda fragmentar sin
  volver a interpretar el PDF crudo.
- `pagina_inicio` y `pagina_fin` mantienen trazabilidad cuando una seccion cruza
  varias paginas.
- `advertencias` comunica degradaciones sin esconderlas.

**Analogia:** el JSON es una ficha de entrega. El parser puede cambiar el metodo
con el que lee la caja, pero la ficha debe tener siempre las mismas casillas para
que el siguiente equipo no tenga que adivinar que recibio.

## 5. Decisiones registradas

### D-001: contrato por secciones

**Decision:** entregar `contenido_estructurado` con encabezado, nivel, texto y
paginas, en lugar de entregar solo texto plano.

**Motivo:** el chunking del PR #8 necesita que yo conserve contexto y trazabilidad.

**Analogia:** texto plano es una pila de hojas sin separadores; las secciones
son esa misma pila con etiquetas y paginas. AI puede cortar una seccion grande,
pero no pierde de que tema venia.

**Consecuencia:** `structurer.py` es una pieza obligatoria antes de considerar
terminada mi salida. La heuristica esta implementada y validada.

### D-002: PyMuPDF como parser PDF

**Decision:** mi codigo usa `pymupdf` para abrir el PDF y recorrer sus
paginas, bloques, lineas y spans.

**Motivo:** me permite conservar pagina y tamano de fuente, datos utiles
para inferir encabezados. Tambien accedo a la estructura de bloques fisicos del
documento, lo que resulto ser clave para la decision D-008.

**Aclaracion del contrato:** en la propuesta del chat aparecia `pypdf` como
ejemplo de parser, pero la decision de implementacion que tome fue PyMuPDF. El
contrato no obliga al consumidor a una libreria concreta; `extraccion.parser`
debe informar la libreria que realmente use.

**Analogia:** PyMuPDF es un lector que puede decirte no solo que palabras vio,
sino en que pagina y con que tamano estaban impresas. Eso ayuda a sospechar que
un texto es titulo, pero la sospecha todavia debe convertirse en una regla.

### D-003: extraer por bloques y conservar metadatos visuales *(actualizada)*

**Decision original:** extraer por lineas, conservando tamaño, fuente y negrita
del primer span.

**Decision actualizada (D-008 explica el motivo):** extraer un fragmento por
bloque, concatenando el texto de todas sus lineas. Se conserva tamaño, fuente y
negrita del primer span del bloque.

**Trade-off:** usar el primer span como referencia simplifica el MVP, pero puede
perder cambios de fuente dentro de un bloque con varias lineas de estilos mixtos.
No se intenta reconstruir el diseño completo del PDF.

**Analogia:** en vez de entregar cada oracion de un parrafo en sobres separados,
se entrega el parrafo completo con una muestra de su formato. Es suficiente para
ordenar el documento, no para reproducirlo visualmente.

### D-004: Pydantic como modelo interno del contrato

**Decision:** representar metadatos, advertencias, fragmentos, secciones y el
documento con `BaseModel`.

**Motivo:** me permite validar la forma de los datos mientras construyo mi
documento y serializo una salida consistente.

**Analogia:** Pydantic es el formulario con casillas obligatorias en la puerta
de salida. Evita entregar una ficha incompleta, pero no decide si la informacion
extraida es correcta.

### D-005: SHA-256 para identidad del archivo

**Decision:** calculo el hash leyendo el archivo en bloques de 1 MiB.

**Motivo:** puedo identificar el contenido original sin cargarlo completo en
memoria y detectar posibles duplicados.

**Analogia:** el hash es una huella digital del PDF. Dos archivos con el mismo
nombre pueden ser distintos; la huella permite diferenciarlos.

### D-006: advertencias en lugar de ocultar problemas

**Decision:** cuando una pagina no produce fragmentos, genero
`PAGINA_SIN_TEXTO` y marco `requiere_ocr=True`.

**Implementado:** mi funcion `detectar_advertencias` compara las paginas
esperadas con las paginas presentes en mis fragmentos usando un set de Python,
lo que permite la busqueda en tiempo constante O(1).

**Pendiente:** distinguir `POSIBLE_OCR` de `PAGINA_SIN_TEXTO`, registrar
`ERROR_EXTRACCION` y decidir como propagar un archivo completamente ilegible.

**Analogia:** una luz de advertencia en el tablero no repara el motor; informa al
conductor para que no crea que el viaje fue perfecto.

### D-007: multi-parser detras de una salida comun

**Decision:** cada formato tendra un parser especializado, pero todos entregaran
las mismas estructuras normalizadas antes de que yo cree `DocumentoIngestado`.

```text
archivo -> parser del formato -> fragmentos/secciones -> documento v1.0
```

**Orden que decidi:** PDF primero; Markdown, HTML y Word despues de validar mi
flujo PDF.

**Analogia:** son traductores distintos que llenan el mismo formulario. El
chunker no necesita saber si el texto vino de PDF o Markdown.

### D-008: extraer por bloque, no por linea

**Problema encontrado:** la heuristica de structurer.py intentaba fusionar
fragmentos consecutivos con el mismo nivel de encabezado para reconstruir
titulos largos que se partian en dos lineas. Pero esa misma regla fusionaba
incorrectamente titulos genuinamente distintos como "2. Primeros Pasos" y
"2.1 Acerca de...", que simplemente estaban juntos en el PDF sin texto de cuerpo
entre ellos.

**Causa raiz:** la logica de fusion era necesaria porque el extractor creaba
un fragmento por linea. Al desarmarse la agrupacion natural de PyMuPDF (el bloque),
structurer.py intentaba reconstruirla a ciegas con heuristicas fragiles.

**Investigacion:** al imprimir `block.get("bbox")` en el PDF real se comprobe que:
- "2. Primeros Pasos" y "2.1 Acerca de..." viven en **bloques distintos** (incluso
  en paginas distintas). Son objetos independientes en el PDF.
- Un titulo largo que ocupa dos lineas vive en **un solo bloque** de PyMuPDF.
  La libreria ya resolvio la agrupacion.

**Decision:** cambiar `extraer_fragmentos()` para crear un `FragmentoTexto` por
**bloque** en lugar de por linea. El texto de todas las lineas y spans del bloque
se concatena en un solo fragmento. Con esto, PyMuPDF entrega la unidad logica
completa y structurer.py solo necesita clasificar, no reconstruir.

**Consecuencia en structurer.py:** se elimino por completo la logica de fusion de
titulos (la condicion `seccion_actual.texto == ""` que intentaba unir fragmentos
consecutivos del mismo nivel). El codigo quedo mas simple y mas correcto.

**Analogia:** imagina que recibes una novela ya encuadernada por capitulos, pero
alguien la desarmo hoja por hoja. Tu codigo anterior intentaba rearmar los capitulos
a ojo, comparando si dos hojas consecutivas podrian ser del mismo capitulo.
La correccion fue no desarmarla: leer el PDF a nivel de "capitulo" (bloque) desde
el principio, y dejar que PyMuPDF te diga donde empieza y termina cada unidad logica.

### D-009: JSON Schema formal como contrato publico del equipo

**Decision:** crear `contracts/clean_document.schema.json` como documento de
referencia formal que cualquier lenguaje puede validar.

**Motivo:** Pydantic valida el JSON mientras el codigo Python se ejecuta, pero
ese contrato es invisible para mis companeros. El JSON Schema es el reglamento
escrito que Vanessa puede usar en su codigo Python y que Pereira puede referenciar
desde el PR #8 sin depender de mi implementacion.

**Caracteristicas del schema:** usa `"additionalProperties": false` para rechazar
campos extra, `"const": "1.0"` para fijar la version del contrato, `"enum"` para
los idiomas validos, `"format": "date-time"` para las fechas, y
`"pattern": "^[a-fA-F0-9]{64}$"` para garantizar que el SHA-256 sea valido.

**Validacion en prueba:** `tests/test_ingestion.py` carga el schema y valida el
JSON real generado por el pipeline usando la libreria `jsonschema`. Si el JSON
no cumple el contrato, la prueba falla antes de que alguien lo descubra en
produccion.

**Analogia:** Pydantic es el inspector interno de la fabrica que revisa cada
pieza antes de que salga. El JSON Schema es el certificado de calidad que
acompana el paquete y que el cliente puede verificar por su cuenta sin conocer
el proceso interno.

## 6. Flujo implementado y frontera con el equipo

1. `DocumentExtractor` valida la ruta y abre el PDF.
2. Recorro paginas, bloques y spans; por cada bloque de texto genero un
   `FragmentoTexto` con el texto completo, el tamaño de fuente del primer span,
   la bandera de negrita, la fuente y el `bbox` del bloque.
3. `calcular_sha256` calcula la huella del archivo original en bloques de 1 MiB.
4. `detectar_advertencias` detecta paginas que no produjeron ningun fragmento.
5. `estructurar_documento` clasifica cada fragmento como H1, H2 o parrafo usando
   ratios respecto al tamaño de fuente mas frecuente del documento.
6. `DocumentoIngestado` reune metadatos, advertencias y secciones.
7. `model_dump_json` serializa el documento para el consumidor de AI.
8. `tests/test_ingestion.py` valida el JSON generado contra el schema formal.

El PR #8 actualmente describe una entrada por paginas (`page_number`, `text`).
Al integrarlo, debo conservar `tenant_id`, `document_id`, seccion,
encabezado, paginas, idioma, hash, parser y advertencias. El chunker puede
dividir el texto, pero no debe borrar la trazabilidad de origen.

## 7. Decisiones pendientes

- Validar el flujo con PDFs tecnicos de otros formatos (tablas, columnas, imagenes).
- Completar advertencias para OCR y errores de extraccion.
- Comparar PyMuPDF con otra alternativa solo si un PDF de prueba revela una limitacion relevante.
- Agregar soporte para Markdown como segundo formato de entrada.

## 8. Registro actualizable de avances

En cada avance agrego una fila. No marco una decision como implementada solo
porque existe una clase: necesito una prueba o un ejemplo que demuestre el flujo.

| Fecha | Avance | Evidencia | Decision o aprendizaje | Estado |
| --- | --- | --- | --- | --- |
| 2026-09-17 | Extraccion de lineas PDF | `extractor.py` | Se combinan spans y se conserva pagina, fuente y tamaño | Reemplazado por D-008 |
| 2026-09-17 | Hash del original | `hashing.py` | Se identifica contenido por SHA-256 | Implementado |
| 2026-09-18 | Advertencias de paginas vacias | `extraction_warnings.py` | Una pagina ausente puede requerir OCR | Parcial |
| 2026-09-19 | Estructuracion heuristica por ratios | `structurer.py` | El ratio tamaño/cuerpo estima H1, H2 o cuerpo sin depender de valores absolutos | Implementado |
| 2026-09-19 | Orquestacion del pipeline | `main.py` | Coordina extraccion, advertencias, estructura y JSON | Implementado |
| 2026-09-19 | Validaciones basicas con pytest | `tests/test_ingestion.py` | Comprueba tipo de origen, version, secciones y paginas | Implementado |
| 2026-09-20 | Refactor: extraccion por bloques | `extractor.py`, `structurer.py` | PyMuPDF ya agrupa lineas en bloques logicos; extraer por bloque elimina la necesidad de fusion manual | Implementado (D-008) |
| 2026-09-20 | Contrato JSON Schema formal | `contracts/clean_document.schema.json` | El schema es el reglamento publico que cualquier lenguaje puede validar | Implementado (D-009) |
| 2026-09-20 | Prueba contra contrato formal | `tests/test_ingestion.py` | pytest valida el JSON generado contra el schema; la prueba pasa verde | Implementado |

## 9. Como actualizo esta documentacion

En cada avance agrego cuatro cosas: fecha, decision, razon y evidencia. Si cambio
una decision, no borro la anterior: marco su estado como reemplazada y explico
que prueba provoco el cambio. Uso analogias para explicar mi razonamiento, no
para decorar el documento.

Para mi daily, resumo mi avance asi:

- **Que hice:** describo mi avance concreto en extractor, advertencias o estructurador.
- **Resultado:** indico el archivo, ejemplo o prueba que funciona.
- **Problema:** explico la limitacion que encontre, como PDF escaneado o encabezado ambiguo.
- **Solucion:** registro la decision que tome o la ayuda que necesito del equipo.

**Mi aprendizaje de backend:** estoy construyendo una frontera entre modulos y
un contrato compartido. Cada parser que agregue debe respetar la misma salida
aunque internamente use una libreria diferente; asi el consumidor de chunking no
queda acoplado a mi parser concreto.

