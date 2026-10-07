"""Prepara prompts desde evidencia seleccionada, sin llamar a ningún LLM."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from backend.src.nuevamente_ai import PromptRequest, build_from_contract, build_prompt, evidence_from_record


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="Contrato v1.0 JSON o chunks JSON/JSONL")
    parser.add_argument("--tenant-id")
    parser.add_argument("--document-id")
    parser.add_argument("--documento-titulo")
    parser.add_argument("--perfil", choices=["principiante", "avanzado"])
    parser.add_argument("--formato", choices=["resumen", "flashcard", "quiz", "guion"])
    parser.add_argument("--objetivo")
    parser.add_argument("--sector")
    parser.add_argument("--detalle", choices=["breve", "detallado"])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        raw = args.input.read_text(encoding="utf-8-sig")
        data = (
            [json.loads(line) for line in raw.splitlines() if line.strip()]
            if args.input.suffix.lower() == ".jsonl"
            else json.loads(raw)
        )
        if args.input.resolve() == args.output.resolve():
            raise ValueError("La salida no puede sobrescribir la entrada")
        if isinstance(data, dict) and "evidencia" in data:
            if any(value is not None for value in (args.tenant_id, args.document_id,
                    args.documento_titulo, args.perfil, args.formato, args.objetivo, args.sector, args.detalle)):
                raise ValueError("Un contrato completo no admite sobreescrituras por flags")
            bundle = build_from_contract(data)
        else:
            required = (args.tenant_id, args.document_id, args.documento_titulo, args.perfil, args.objetivo)
            if any(value is None for value in required):
                raise ValueError("Con chunks sueltos se requieren tenant, documento, título, perfil y objetivo")
            records = data["chunks"] if isinstance(data, dict) else data
            if not isinstance(records, list):
                raise ValueError("Los chunks deben ser una lista")
            # Se valida TODO el lote: un tenant extraño es un error, no se oculta.
            bundle = build_prompt(PromptRequest(
                perfil_destinatario=args.perfil, formato_salida=args.formato or "resumen",
                documento_titulo=args.documento_titulo, objetivo=args.objetivo,
                tenant_id=args.tenant_id, document_id=args.document_id,
                nicho_sector=args.sector, nivel_detalle=args.detalle or "breve",
            ), [evidence_from_record(record) for record in records])
        output = {
            "version_prompt": "1.0",
            "system_prompt": bundle.system_prompt,
            "user_prompt": bundle.user_prompt,
            "sources": bundle.sources,
            "response_schema": bundle.output_model.model_json_schema(),
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    except (ValueError, KeyError, TypeError, OSError) as exc:
        parser.exit(1, f"No se pudo preparar el prompt: {exc}\n")
    print(f"Prompt preparado sin inferencia: {args.output}")


if __name__ == "__main__":
    main()
