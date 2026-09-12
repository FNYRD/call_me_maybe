"""Adaptador standalone para invocar el proyecto del companero (project_example/)
directo por sus clases, tal como pidio el estudiante — ese proyecto no tiene un
`python -m src` invocable igual que el propio.

Se corre como script aparte (nunca importado) porque su paquete top-level
tambien se llama "src", igual que el de este proyecto: aislar el import via
sys.path evita que colisione con nuestro propio src/.

Uso: <python> _project_example_runner.py <functions.json> <prompts.json> <output.json>
"""
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROJECT_EXAMPLE_DIR = PROJECT_ROOT / "tests" / "project_example"
sys.path.insert(0, str(PROJECT_EXAMPLE_DIR))

from src.callme_files_loader import CallMeFilesLoader, CallMeFunction  # noqa: E402
from src.decoder import Decoder  # noqa: E402

# Misma funcion de escape que usa project_example/src/__main__.py cuando
# ningun prompt calza con el catalogo real.
FN_NONE = {
    "name": "fn_none",
    "description": (
        "Fallback function used when the prompt does not match any available "
        "function definition, or when the prompt is empty or ambiguous."
    ),
    "parameters": {},
    "returns": {"type": "null"},
}


def main() -> None:
    functions_path, prompts_path, output_path = sys.argv[1:4]

    loader = CallMeFilesLoader()
    loader.load_functions(json.loads(Path(functions_path).read_text()))
    loader.load_prompts(json.loads(Path(prompts_path).read_text()))
    loader.func_definitions["fn_none"] = CallMeFunction(**FN_NONE)
    loader.func_names.add("fn_none")

    decoder = Decoder()
    resultados = []
    for prompt in loader.prompts:
        try:
            name = decoder.decode_func_name(
                prompt.prompt, loader.func_names, loader.func_definitions
            )
            params = decoder.decode_func_params(
                prompt.prompt, loader.func_definitions[name]
            )
            resultados.append({"prompt": prompt.prompt, "name": name, "parameters": params})
        except Exception as error:
            resultados.append({"prompt": prompt.prompt, "_error": str(error)})

    Path(output_path).write_text(json.dumps(resultados))


if __name__ == "__main__":
    main()
