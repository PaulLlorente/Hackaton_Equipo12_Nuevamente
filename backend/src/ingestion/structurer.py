from collections import Counter
from .schema import FragmentoTexto, SeccionContenido


# función para detectar el tamaño de fuente más común en los fragmentos de texto, que se usará como referencia para determinar los niveles de encabezado
def _detectar_tamano_cuerpo(fragmentos: list[FragmentoTexto]) -> float:

    tamanos = [round(f.tamano_fuente, 1) for f in fragmentos]

    mas_comun = Counter(tamanos).most_common(1)[0][
        0
    ]  # Obtiene el tamaño de fuente más frecuente

    return mas_comun


# función para determinar el nivel de encabezado basado en el tamaño de fuente del fragmento y el tamaño de fuente del cuerpo
def _determinar_nivel_encabezado(tamano_fuente: float, tamano_cuerpo: float) -> int:
    """
    Devuelve 1 (H1), 2 (H2), o 0 (párrafo normal).
    """

    tamano_diferencia = tamano_fuente / tamano_cuerpo
    tolerancia_h1 = 1.7  # Diferencia de tamaño para considerar H1
    tolerancia_h2 = 1.15  # Diferencia de tamaño para considerar H2

    return (
        1
        if tamano_diferencia >= tolerancia_h1
        else 2 if tamano_diferencia >= tolerancia_h2 else 0
    )


# funcion principal para estructurar el documento en secciones basadas en los fragmentos de texto extraídos y entrega una lista de SeccionContenido
def estructurar_documento(fragmentos: list[FragmentoTexto]) -> list[SeccionContenido]:
    if not fragmentos:
        return []

    # 1. Calculamos el tamaño base una sola vez
    tamano_cuerpo = _detectar_tamano_cuerpo(fragmentos)

    secciones_finales: list[SeccionContenido] = []
    seccion_actual: SeccionContenido | None = None

    for frag in fragmentos:
        nivel = _determinar_nivel_encabezado(frag.tamano_fuente, tamano_cuerpo)

        if nivel > 0:  # ES UN TÍTULO

            if seccion_actual is not None:
                secciones_finales.append(seccion_actual)

            # creamos una sección nueva
            seccion_actual = SeccionContenido(
                nivel_encabezado=nivel,
                titulo_seccion=frag.texto,
                texto="",  # Empezamos con texto vacío, los siguientes fragmentos lo llenarán
                pagina_inicio=frag.pagina,
                pagina_fin=frag.pagina,
            )

        else:  # ES PÁRRAFO NORMAL (Cuerpo)
            # ¿Qué pasa si el PDF arranca con texto normal antes del primer título?
            if seccion_actual is None:
                seccion_actual = SeccionContenido(
                    nivel_encabezado=0,
                    titulo_seccion=None,
                    texto="",
                    pagina_inicio=frag.pagina,
                    pagina_fin=frag.pagina,
                )

            if seccion_actual.texto:
                seccion_actual.texto += "\n" + frag.texto
            else:
                seccion_actual.texto = frag.texto

            seccion_actual.pagina_fin = (
                frag.pagina
            )  # Actualizamos la última página de la sección

    # Al final del bucle, si todavía tenemos una sección en construcción, la agregamos a la lista final
    if seccion_actual is not None:
        secciones_finales.append(seccion_actual)

    return secciones_finales
