from typing import List
from .schema import Advertencia, FragmentoTexto


def detectar_advertencias(
    fragmentos: List[FragmentoTexto], total_paginas: int
) -> List[Advertencia]:

    advertencias = []

    # 1. Detectar páginas sin texto
    paginas_con_texto = {fragmento.pagina for fragmento in fragmentos}
    for pagina in range(1, total_paginas + 1):
        if pagina not in paginas_con_texto:
            advertencias.append(
                Advertencia(
                    codigo="PAGINA_SIN_TEXTO",
                    pagina=pagina,
                    mensaje=f"La página {pagina} no contiene texto extraído.",
                    requiere_ocr=True,
                )
            )

    return advertencias
