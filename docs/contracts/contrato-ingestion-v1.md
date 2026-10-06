# Decisiones del modulo de ingestion

- **Contrato:** v1.0
- **Ultima revision:** 2026-10-05
- **Responsable de mi modulo:** (Yo) Brayan Camilo Lopez (`Discord: @Brayan López`)
- **Consumidores de mi salida:** AI Engineer, RAG Data/Vector Store y API Core
- **Archivo actualizable:** uso este documento para registrar mis decisiones; no reemplaza el codigo.

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

| Extraccion PDF | Implementada y validada | `src/ingestion/extractors/extractorPDF.py` | Validar con mas PDFs tecnicos |
| Extraccion Markdown | Implementada y validada (D-013) | `src/ingestion/extractors/extractorMD.py` | Validar con documentos mixtos |
| Arquitectura Multi-parser | Implementada con Factory (D-012) | `extractor.py`, `factory.py` | Listo para incorporar futuros formatos |
| Entrada por bytes | Implementada (D-010) | `extractors/`, `main.py` | Listo para integracion con FastAPI |
| Parser PDF | PyMuPDF confirmado | `requirements.txt`, `extractors/extractorPDF.py` | Confirmar con PDFs escaneados |
| Hash del archivo | Refactorizado a bytes en memoria | `src/ingestion/hashing.py` | Funcional |
| Modelo de salida | Definido con Pydantic (puro y desacoplado) | `src/ingestion/schema.py` | Funcional |
| Advertencias | Implementadas | `extraction_warnings.py` detecta paginas sin texto | Agregar errores y casos OCR |
| Estructuracion por encabezados | Implementada y refinada | `src/ingestion/structurer.py` | Funcional con extraccion por bloques y Adapter MD |
| Orquestacion del flujo | Implementada y funcional | `src/ingestion/main.py` | Recibe `source: bytes` y `nombre_archivo: str` |
| Pruebas automaticas | Modularizadas por formato (D-014) | `tests/test_ingestion_PDF.py`, `tests/test_ingestion_MD.py` | Ejecutadas y 100% verdes contra JSON Schema |
| Contrato JSON formal | Implementado | `contracts/clean_document.schema.json` | Compartido con Vanessa y Pereira |

| Tipado moderno | Migrado a `list[]` nativo (D-011) | Todos los modulos | Funcional |

Este estado distingue entre el codigo que ya escribi y el comportamiento que ya
comprobe. El flujo principal puede construir el JSON por secciones, las pruebas
comprueban el contrato completo tanto para PDF como para Markdown, y el schema JSON
esta listo para que el consumidor de AI lo use como referencia.

## 3. Estructura actual del paquete

| Archivo | Responsabilidad | Analogia |
| --- | --- | --- |
| `schema.py` | Define las estructuras de datos y el documento final desacoplado de librerias externas | Los formularios oficiales que todos deben llenar sin importar que lapiz se use |
| `extractor.py` | Clase abstracta base (`DocumentExtractor`) que define el contrato comun | El molde estandar de enchufe al que cualquier aparato debe adaptarse |
| `factory.py` | Fabrica que resuelve y entrega el extractor correcto segun la extension del archivo | La recepcionista que canaliza cada documento a la ventanilla correcta |
| `extractors/extractorPDF.py` | Extrae contenido de PDFs por bloques fisicos usando PyMuPDF | El lector experto en libros impresos y diagramacion visual |
| `extractors/extractorMD.py` | Extrae contenido de Markdown adaptando encabezados (`#`) a tamaños de fuente | El interprete que traduce un dialecto para que el sistema lo entienda sin cambiar sus reglas |
| `hashing.py` | Calcula la huella SHA-256 directamente sobre los bytes en memoria | La huella digital del documento |
| `extraction_warnings.py` | Detecta paginas que no produjeron texto | El tablero que enciende una alerta |
| `structurer.py` | Agrupa fragmentos y estima niveles de encabezado jerarquicos | El archivista que separa el texto por temas segun el tamaño |
| `main.py` | Coordina el flujo global y serializa el resultado | El coordinador general que pasa el expediente por cada ventanilla |
| `__init__.py` | Marca el directorio como paquete Python | La etiqueta que permite importar el paquete |

| `tests/test_ingestion_PDF.py` | Prueba automatica para PDFs contra el JSON Schema | La auditoria formal de entrega para documentos PDF |
| `tests/test_ingestion_MD.py` | Prueba automatica para Markdown contra el JSON Schema | La auditoria formal de entrega para documentos Markdown |
| `contracts/clean_document.schema.json` | Contrato formal en JSON Schema que cualquier lenguaje puede validar | El reglamento publico escrito que todos los equipos pueden leer |

| `../../backend/tests` | Ejecuta la prueba con pytest y valida el JSON contra el schema formal | El simulacro de entrega del expediente ante un auditor |
| `clean_document.schema.json` | Contrato formal en JSON Schema que cualquier lenguaje puede validar | El reglamento publico escrito que todos los equipos pueden leer |


La separacion es correcta y escalable: la orquestacion no conoce detalles de ningun
formato y soportar un formato nuevo solo requiere crear un nuevo extractor en `extractors/`.

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

### D-005: SHA-256 para identidad del archivo *(actualizada)*

**Decision original:** calculo el hash leyendo el archivo en bloques de 1 MiB
desde disco.

**Decision actualizada (D-010 explica el motivo):** calculo el hash directamente
sobre los bytes que ya estan en memoria. Como el archivo llega completo desde
FastAPI (o desde el test con `.read_bytes()`), no necesito abrir ninguna ruta
ni leer en bloques.

**Motivo:** puedo identificar el contenido original y detectar posibles duplicados.

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

**Decision:** crear `clean_document.schema.json` como documento de
referencia formal que cualquier lenguaje puede validar.

**Motivo:** Pydantic valida el JSON mientras el codigo Python se ejecuta, pero
ese contrato es invisible para mis companeros. El JSON Schema es el reglamento
escrito que Vanessa puede usar en su codigo Python y que Pereira puede referenciar
desde el PR #8 sin depender de mi implementacion.

**Caracteristicas del schema:** usa `"additionalProperties": false` para rechazar
campos extra, `"const": "1.0"` para fijar la version del contrato, `"enum"` para
los idiomas validos, `"format": "date-time"` para las fechas, y
`"pattern": "^[a-fA-F0-9]{64}$"` para garantizar que el SHA-256 sea valido.

**Validacion en prueba:** `../../backend/tests` carga el schema y valida el
JSON real generado por el pipeline usando la libreria `jsonschema`. Si el JSON
no cumple el contrato, la prueba falla antes de que alguien lo descubra en
produccion.

**Analogia:** Pydantic es el inspector interno de la fabrica que revisa cada
pieza antes de que salga. El JSON Schema es el certificado de calidad que
acompana el paquete y que el cliente puede verificar por su cuenta sin conocer
el proceso interno.

### D-010: entrada por bytes en lugar de ruta de disco

**Problema encontrado:** en produccion el PDF llega desde el frontend a traves
de la API de FastAPI. FastAPI lo tiene en memoria como `bytes` (mediante
`await file.read()`). Si mi modulo solo acepta una ruta de disco, Erick tendria
que guardar el archivo en el servidor y luego pasarme la ruta — un viaje de ida
y vuelta al disco completamente innecesario.

**Decision:** refactorizar `DocumentExtractor` para recibir `source: bytes` y
`nombre_archivo: str` en lugar de `file_path: str | Path`. PyMuPDF soporta
apertura desde memoria con `pymupdf.open(stream=source, filetype="pdf")`.

**Archivos modificados:**
- `extractor.py`: constructor recibe `(source: bytes, nombre_archivo: str)`.
  Se guarda `self.source` para calcular el hash posteriormente.
- `hashing.py`: recibe `bytes` directamente y calcula el SHA-256 sin abrir
  ningun archivo ni leer en bloques.
- `main.py`: la funcion `procesar_documento` ahora recibe `source: bytes` y
  `nombre_archivo: str` en lugar de `ruta_archivo: str`.
- `test_ingestion.py`: lee el PDF de prueba con `.read_bytes()` y pasa los
  bytes al pipeline.

**Consecuencia en el contrato de salida:** ninguna. El JSON que entrego sigue
siendo identico. Este cambio es puramente interno: como entra el PDF a mi modulo,
no como sale la informacion.

**Analogia:** antes le dabamos al lector la direccion de la biblioteca y el
numero de estante para que fuera a buscar el libro. Ahora le entregamos el libro
directamente en las manos. No tiene que ir a ninguna parte — ya tiene el
contenido listo para leer.

### D-011: migracion a tipado moderno `list[]`

**Decision:** reemplazar `from typing import List` por el tipo nativo `list[]`
en todos los modulos: `extractor.py`, `structurer.py`, `extraction_warnings.py`,
`schema.py`.

**Motivo:** desde Python 3.9, los tipos genericos nativos (`list`, `dict`, `tuple`)
pueden usarse directamente en anotaciones de tipo sin importar nada de `typing`.
El proyecto usa Python 3.14, asi que el import de `List` era innecesario.

**Archivos modificados:** todos los que usaban `from typing import List`. Se
elimino el import y se reemplazo `List[X]` por `list[X]`.

**Analogia:** es como dejar de usar una extension del navegador que hacia algo
que el navegador ahora ya hace de fabrica. La extension sigue funcionando, pero
ya no tiene sentido cargarla.

### D-012: abstraccion con Patron Factory y desacople del DTO

**Decision:** crear la clase abstracta `DocumentExtractor(ABC)` y la fabrica
`ExtractorFactory.get_extractor`. Desacoplar `schema.py` eliminando el import
de `pymupdf` y los valores hardcodeados (`parser`, `version_parser`, `tipo_origen`).
Cualquier formato no soportado lanza explicitamente `ValueError`.

**Motivo:** el DTO no debe tener conocimiento de con que libreria se extrajeron
los datos. Al encapsular la extraccion detras de una clase base comun, el
orquestador (`main.py`) no conoce detalles del archivo y el sistema cumple el
Principio de Abierto/Cerrado (OCP).

**Analogia:** es como un centro comercial con una recepcion central. Si llegas con
un paquete, la recepcionista (Factory) sabe exactamente a que oficina mandarlo segun
la etiqueta (extension). Si traes un paquete que el centro comercial no procesa,
te avisa inmediatamente en la entrada (ValueError) en vez de dejarte perderte adentro.

**En NestJS:** equivale al Strategy Pattern combinado con Factory Providers
(`useFactory`) e inyeccion de dependencias por interfaz.

### D-013: extractor de Markdown con Patron Adapter nativo

**Decision:** implementar `ExtractorMarkdown` sin dependencias externas pesadas,
decodificando bytes a UTF-8 y recorriendo el texto linea por linea. Adaptar los
simbolos `#`, `##` y `###` asignando tamaños de fuente virtuales (`24.0`, `20.0`,
`16.0`) y texto normal (`12.0`).

**Motivo:** `structurer.py` ya sabe inferir jerarquias H1/H2 usando relaciones de
tamaño de fuente. Al adaptar Markdown a esa misma escala virtual, reutilizamos el
100% de la logica de estructuracion existente sin duplicar codigo ni alterar el
contrato JSON v1.0.

**Analogia:** es como un adaptador de viaje para enchufes internacionales. El
televisor (estructurador) sigue esperando una clavija redonda (tamaños de fuente).
En lugar de desarmar el televisor para que acepte clavijas planas (Markdown), le
conectamos un adaptador liviano en la punta que traduce la conexion de inmediato.

**En NestJS:** Patrón Adapter clasico (GoF), util para normalizar fuentes heterogeneas
hacia un formato de dominio unico.

### D-014: separacion de suites de prueba y fixtures

**Decision:** dividir la suite de pruebas en `test_ingestion_PDF.py` y
`test_ingestion_MD.py`, y unificar los archivos de prueba en la carpeta
`docs/test_ingestion_formats/`.

**Motivo:** aislar el diagnostico por formato. Si falla la decodificacion de
Markdown, no bloquea la verificacion del motor de PDF. Ambos tests validan
su salida de forma independiente contra el contrato estricto de `clean_document.schema.json`.

**Analogia:** tener dos inspectores de aduana especializados: uno audita libros
impresos (PDF) y el otro audita documentos digitales (MD). Ambos usan el mismo
reglamento (JSON Schema), pero si un inspector detecta un detalle en un libro, el
otro puede seguir revisando el resto de cargas sin detenerse.

## 6. Flujo implementado y frontera con el equipo

1. `procesar_documento` recibe `source: bytes` y `nombre_archivo: str`.

2. `ExtractorFactory.get_extractor` inspecciona la extension (`.pdf`, `.md`) y
   devuelve la instancia correspondiente que implementa `DocumentExtractor`.
   Si la extension es desconocida, lanza `ValueError`.
3. El extractor ejecuta `.parse()` en memoria:
   - En PDF: recorre bloques y spans de PyMuPDF.
   - En Markdown: recorre lineas y adapta los `#` a tamaños de fuente virtuales.
4. Se devuelve `ResultadoExtraccion` con fragmentos y metadatos basicos.
5. `calcular_sha256` calcula la huella SHA-256 sobre los bytes en memoria.
6. `detectar_advertencias` evalua la calidad de la extraccion.
7. `estructurar_documento` clasifica y agrupa los fragmentos en secciones jerarquicas.
8. `DocumentoIngestado` reune metadata, info de extraccion (parser, version,
   advertencias) y contenido estructurado.
9. `model_dump_json` serializa el resultado validado para el modulo RAG.
10. `test_ingestion_PDF.py` y `test_ingestion_MD.py` aseguran que ambos formatos
    cumplan al 100% el JSON Schema formal acordado con Vanessa y Pereira.


## 7. Decisiones pendientes

- Spike de Docling: evaluado en branch experimental. Descartado para el MVP de
  PDFs por latencia y consumo de recursos en OCI Always Free (7-33s vs 0.4s de PyMuPDF).
  Queda reservado como candidato para archivos ofimaticos (DOCX/PPTX) en sprints posteriores.
- Conectar con el endpoint de FastAPI de Erick en Semana 2.
- Validar comportamiento ante archivos corruptos o vacios a nivel de API.

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
| 2026-09-19 | Validaciones basicas con pytest | `../../backend/tests` | Comprueba tipo de origen, version, secciones y paginas | Implementado |
| 2026-09-20 | Refactor: extraccion por bloques | `extractor.py`, `structurer.py` | PyMuPDF ya agrupa lineas en bloques logicos; extraer por bloque elimina la necesidad de fusion manual | Implementado (D-008) |
| 2026-09-20 | Contrato JSON Schema formal | `clean_document.schema.json` | El schema es el reglamento publico que cualquier lenguaje puede validar | Implementado (D-009) |
| 2026-09-20 | Prueba contra contrato formal | `../../backend/tests` | pytest valida el JSON generado contra el schema; la prueba pasa verde | Implementado |
| 2026-09-25 | Refactor: entrada por bytes | `extractor.py`, `hashing.py`, `main.py`, `test_ingestion.py` | El modulo recibe bytes en memoria en vez de ruta de disco; elimina I/O innecesario para integracion con FastAPI | Implementado (D-010) |
| 2026-09-25 | Migracion a `list[]` nativo | Todos los modulos | Se elimino `from typing import List` y se uso `list[]` nativo de Python 3.9+ | Implementado (D-011) |
| 2026-09-25 | Hash desde bytes en memoria | `hashing.py` | `calcular_sha256` recibe `bytes` directamente; ya no abre archivos ni lee en bloques | Implementado (actualiza D-005) |
| 2026-10-04 | Patron Factory y desacople del DTO | `extractor.py`, `factory.py`, `schema.py` | Se creo `DocumentExtractor(ABC)` y `ExtractorFactory`. Se elimino acoplamiento de PyMuPDF en DTOs | Implementado (D-012) |
| 2026-10-05 | Extractor Markdown con Adapter nativo | `extractors/extractorMD.py` | Se mapeo la semantica de `#` a tamaños de fuente virtuales sin dependencias pesadas | Implementado (D-013) |
| 2026-10-05 | Modularizacion de tests por formato | `tests/test_ingestion_PDF.py`, `tests/test_ingestion_MD.py` | Tests independientes para PDF y MD ejecutados y 100% verdes contra el JSON Schema | Implementado (D-014) |
| 2026-10-05 | Spike de Docling evaluado | `scripts/spike_docling.py` (desechable) | Se midio y descarto para PDF por costo computacional (33s vs 0.4s); se reserva para DOCX/PPTX | Evaluado y documentado |

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
