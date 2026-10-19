from pathlib import Path
import re

_PATRON_UUID_LARGO = re.compile(
    r"^[0-9a-fA-F]{8}-?[0-9a-fA-F]{4}-?[0-9a-fA-F]{4}-?[0-9a-fA-F]{4}-?[0-9a-fA-F]{12}$"
)


def formatear_document_id(document_id, nombre_archivo=None) -> str:
    """Garantiza el formato legible `<nombre_archivo>_<8chars>` en toda la UI.

    Si recibe un UUID crudo de 32/36 caracteres (de cargas antiguas en ChromaDB),
    lo recorta a 8 caracteres y le antepone el nombre del archivo si existe.
    """
    doc_str = str(document_id or "").strip()
    if not doc_str or doc_str == "No disponible":
        return "No disponible"

    if _PATRON_UUID_LARGO.match(doc_str):
        sufijo = doc_str.replace("-", "")[:8]
        if nombre_archivo and nombre_archivo != "Documento sin nombre":
            stem = Path(str(nombre_archivo)).stem
            return f"{stem}_{sufijo}"
        return f"doc_{sufijo}"

    return doc_str


def obtener_metadata(resultado, tenant_id) -> tuple[str, str, str]:
    metadata = resultado.get("metadata") or {}

    if not isinstance(metadata, dict):
        metadata = {}

    origen = metadata.get("origen") or "Documento sin nombre"
    raw_doc_id = metadata.get("document_id") or "No disponible"
    document_id = formatear_document_id(raw_doc_id, origen)
    tenant_resultado = metadata.get("tenant_id") or tenant_id.strip()

    return origen, document_id, tenant_resultado
