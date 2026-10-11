import json
import re
import streamlit as st

from services.api import consultar_rag

# ============================================================
# LIMPIEZA Y NORMALIZACIÓN DEL TEXTO
# ============================================================


def limpiar_texto(texto):
    """
    Limpia y normaliza el contenido recuperado del motor RAG.

    Características:
    - Maneja valores None y textos vacíos.
    - Extrae el campo 'texto' cuando el contenido es un JSON.
    - Convierte los saltos de línea literales (\\n) en saltos reales.
    - Normaliza saltos de línea de Windows, Linux y Mac.
    - Elimina espacios y tabulaciones innecesarios.
    - Conserva párrafos, listas, títulos y bloques de código.
    - Corrige espacios antes de los signos de puntuación.
    - Evita eliminar contenido textual legítimo.
    """

    # --------------------------------------------------------
    # 1. Validar y normalizar el tipo de entrada
    # --------------------------------------------------------
    if texto is None:
        return ""

    if not isinstance(texto, str):
        # Algunas fuentes pueden entregar estructuras JSON.
        try:
            texto = json.dumps(texto, ensure_ascii=False)
        except (TypeError, ValueError):
            texto = str(texto)

    texto = texto.strip()

    if not texto:
        return ""

    # --------------------------------------------------------
    # 2. Intentar interpretar un objeto JSON serializado
    # --------------------------------------------------------
    # Ejemplo:
    # {"texto": "Primera línea\\nSegunda línea"}
    #
    # Solo extraemos el campo "texto" cuando realmente existe.
    if texto.startswith("{") and texto.endswith("}"):
        try:
            datos = json.loads(texto)

            if isinstance(datos, dict):
                for clave in ("texto", "content", "page_content"):
                    if clave in datos:
                        texto = str(datos[clave] or "")
                        break

        except (json.JSONDecodeError, TypeError, ValueError):
            # Si no es JSON válido, se trata como texto normal.
            pass

    # --------------------------------------------------------
    # 3. Eliminar envolturas simples como "texto": "..."
    # --------------------------------------------------------
    texto = re.sub(r'^\s*"?texto"?\s*:\s*', "", texto, flags=re.IGNORECASE).strip()

    # Retirar las comillas exteriores solamente si forman
    # una envoltura completa y no son contenido legítimo.
    if len(texto) >= 2 and texto[0] == texto[-1] == '"':
        texto = texto[1:-1]

    # --------------------------------------------------------
    # 4. Normalizar saltos de línea
    # --------------------------------------------------------
    # Primero convertimos secuencias escapadas de CRLF.
    # Se contemplan una o más barras invertidas:
    # \n, \\n, \\\n, etc.
    texto = re.sub(r"\\+r\\+n", "\n", texto)
    texto = re.sub(r"\\+n", "\n", texto)
    texto = re.sub(r"\\+r(?![A-Za-z])", "\n", texto)

    # Normalizar saltos reales de distintos sistemas.
    texto = texto.replace("\r\n", "\n").replace("\r", "\n")

    # Eliminar caracteres nulos.
    texto = texto.replace("\x00", "")

    # --------------------------------------------------------
    # 5. Normalizar espacios sin destruir el formato
    # --------------------------------------------------------
    lineas = texto.split("\n")
    lineas_limpias = []

    for linea in lineas:
        # Convertir tabulaciones en espacios.
        linea = linea.replace("\t", " ")

        # Compactar espacios consecutivos.
        linea = re.sub(r" {2,}", " ", linea)

        # Eliminar espacios en los extremos.
        linea = linea.strip()

        lineas_limpias.append(linea)

    texto = "\n".join(lineas_limpias)

    # --------------------------------------------------------
    # 6. Reducir saltos de línea excesivos
    # --------------------------------------------------------
    # Máximo una línea vacía entre párrafos.
    texto = re.sub(r"\n[ \t]*\n(?:[ \t]*\n)+", "\n\n", texto)

    # --------------------------------------------------------
    # 7. Unir líneas partidas sin destruir listas ni bloques
    # --------------------------------------------------------
    # Los documentos Markdown pueden contener:
    # - Títulos: # Título
    # - Listas: - Elemento
    # - Numeración: 1. Elemento
    # - Citas: > Texto
    # - Tablas: | columna |
    # - Código: ```python
    #
    # No unimos automáticamente líneas estructurales.
    lineas = texto.split("\n")
    resultado = []

    en_bloque_codigo = False

    patron_estructura = re.compile(
        r"^(?:"
        r"#{1,6}\s|"  # Títulos Markdown
        r"[-*+]\s|"  # Listas
        r"\d+[.)]\s|"  # Listas numeradas
        r">\s?|"  # Citas
        r"\|.*\||"  # Filas de tablas
        r"```|"  # Bloques de código
        r"~~~|"  # Bloques de código alternativos
        r"<(?:div|p|br|ul|ol|li)\b|"  # HTML básico
        r")",
        flags=re.IGNORECASE,
    )

    for linea in lineas:
        # Detectar bloques de código para preservar su formato.
        if linea.startswith(("```", "~~~")):
            en_bloque_codigo = not en_bloque_codigo
            resultado.append(linea)
            continue

        # Dentro de un bloque de código no modificamos el texto.
        if en_bloque_codigo:
            resultado.append(linea)
            continue

        # Conservar párrafos vacíos.
        if not linea:
            if resultado and resultado[-1] != "":
                resultado.append("")
            continue

        es_estructura = bool(patron_estructura.match(linea))

        if not resultado or not resultado[-1]:
            resultado.append(linea)
            continue

        linea_anterior = resultado[-1]

        # No combinar con líneas que forman estructuras Markdown.
        anterior_es_estructura = bool(patron_estructura.match(linea_anterior))

        if es_estructura or anterior_es_estructura:
            resultado.append(linea)
        else:
            # Unir líneas normales que pertenecen a la misma frase.
            resultado[-1] = linea_anterior + " " + linea

    texto = "\n".join(resultado)

    # --------------------------------------------------------
    # 8. Corregir espacios antes de signos de puntuación
    # --------------------------------------------------------
    texto = re.sub(r"[ \t]+([,.;:!?])", r"\1", texto)

    # --------------------------------------------------------
    # 9. Eliminar líneas vacías en los extremos
    # --------------------------------------------------------
    texto = texto.strip()

    return texto


# ============================================================
# PRESENTACIÓN DE LA CONSULTA
# ============================================================


def mostrar_consulta():
    """Interfaz de Streamlit para consultar documentos mediante RAG."""

    st.title("Consultar documento")

    st.write("Haz una pregunta sobre la información que ha sido procesada.")

    # --------------------------------------------------------
    # 1. Datos de la consulta
    # --------------------------------------------------------
    tenant_id = st.text_input(
        "Espacio de consulta", value=st.session_state.get("tenant_id", "equipo12")
    )

    pregunta = st.text_area(
        "¿Qué quieres saber?",
        placeholder="Escribe tu pregunta sobre el documento...",
        height=100,
    )

    # --------------------------------------------------------
    # 2. Ejecutar consulta
    # --------------------------------------------------------
    if not st.button("Consultar", use_container_width=True):
        return

    if not pregunta.strip():
        st.warning("Escribe una pregunta para continuar.")
        return

    if not tenant_id.strip():
        st.warning("Ingresa un espacio de consulta.")
        return

    with st.spinner("Buscando información en los documentos..."):
        exito, respuesta = consultar_rag(pregunta.strip(), tenant_id.strip())

    # --------------------------------------------------------
    # 3. Gestionar errores de la API
    # --------------------------------------------------------
    if not exito:
        st.error("No fue posible completar la consulta.")
        st.caption(str(respuesta))
        return

    if not isinstance(respuesta, dict):
        st.error("El servidor devolvió una respuesta inesperada.")
        return

    resultados = respuesta.get("results", [])

    if not isinstance(resultados, list):
        st.error("El formato de los resultados no es válido.")
        return

    if not resultados:
        st.info("No se encontraron fragmentos relacionados " "con tu pregunta.")
        return

    # --------------------------------------------------------
    # 4. Resumen de resultados
    # --------------------------------------------------------
    st.success(
        f"Consulta realizada correctamente. "
        f"Se encontraron {len(resultados)} fragmentos."
    )

    st.subheader("Información encontrada")

    # --------------------------------------------------------
    # 5. Mostrar cada fragmento
    # --------------------------------------------------------
    for indice, resultado in enumerate(resultados, start=1):

        # Validar la estructura de cada resultado.
        if not isinstance(resultado, dict):
            continue

        # Limpiar el contenido textual.
        texto_original = resultado.get("page_content", "")
        texto = limpiar_texto(texto_original)

        # Obtener metadatos de forma segura.
        metadata = resultado.get("metadata") or {}

        if not isinstance(metadata, dict):
            metadata = {}

        origen = metadata.get("origen", "Documento sin nombre")

        document_id = metadata.get("document_id", "No disponible")

        tenant_resultado = metadata.get("tenant_id", tenant_id.strip())

        # ----------------------------------------------------
        # Tarjeta del fragmento
        # ----------------------------------------------------
        with st.container(border=True):

            st.markdown(f"### Fragmento {indice}")

            if texto:
                # Streamlit renderiza listas, títulos y párrafos
                # Markdown presentes en el contenido.
                st.markdown(texto)
            else:
                st.caption("Sin contenido disponible.")

            st.divider()

            st.caption(f"📄 Documento: {origen}")

            with st.expander("Ver detalles"):
                st.text(f"Document ID: {document_id}")
                st.text(f"Espacio de consulta: {tenant_resultado}")

    # --------------------------------------------------------
    # 6. Respuesta original de la API para depuración
    # --------------------------------------------------------
    with st.expander("Ver respuesta completa del servidor"):
        st.json(respuesta)
