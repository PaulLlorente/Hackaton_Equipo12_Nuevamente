"""Exporta schemas de la interfaz interna v1.0. Sin proveedores ni API keys."""

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from backend.src.nuevamente_ai import AdaptationRequest
from backend.src.nuevamente_ai.prompts import response_model


def main():
    output = ROOT / "docs/contracts"
    output.mkdir(parents=True, exist_ok=True)
    models = {"adaptation_prompt.schema.json": AdaptationRequest}
    models.update({f"adaptation_response_{name}.schema.json": response_model(name)
                   for name in ("resumen", "flashcard", "quiz", "guion")})
    for filename, model in models.items():
        (output / filename).write_text(json.dumps(model.model_json_schema(),
            ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Exportados {len(models)} schemas a {output}")


if __name__ == "__main__":
    main()
