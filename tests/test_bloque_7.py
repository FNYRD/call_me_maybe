"""Suite comparativa: mi proyecto (python -m src) contra project_example/
(el companero), corriendo los mismos prompts y comparando name+parameters
contra la correccion real de cada catalogo.

No modifica tests/test_bloque_6.py — es un archivo aparte. Reusa el mismo
criterio de contenido (anidacion, prefijo compartido, tipos, comillas) pero
en version comparativa: mi proyecto acierta -> pasa; empate en fallo -> pasa;
yo fallo y el companero acierta -> unico caso que cuenta como rojo.

data/input (oficial del subject) queda fuera: no tiene correccion real.
"""
import json
import subprocess
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PYTHON = str(PROJECT_ROOT / "callme" / "bin" / "python")
FIXED_LOGS_PATH = PROJECT_ROOT / "logs" / "logs.json"
RUNNER_SCRIPT = Path(__file__).resolve().parent / "_project_example_runner.py"

STRESS_FUNCTIONS = PROJECT_ROOT / "tests" / "stress_data" / "input" / "functions_definition.json"
STRESS_PROMPTS = PROJECT_ROOT / "tests" / "stress_data" / "input" / "function_calling_tests.json"
STRESS_CORRECTIONS = PROJECT_ROOT / "tests" / "stress_data" / "correction" / "function_calling_corrections.json"

COMPANION_FUNCTIONS = PROJECT_ROOT / "tests" / "new_data" / "input" / "functions_definition.json"
COMPANION_PROMPTS = PROJECT_ROOT / "tests" / "new_data" / "input" / "function_calling_tests.json"
COMPANION_CORRECTIONS = PROJECT_ROOT / "tests" / "new_data" / "correction" / "function_calling_corrections.json"


def run_own_project(functions: Path, prompts: Path, output: Path, timeout: float = 180):
    """Corre mi comando real (python -m src) — mismo mecanismo que test_bloque_6."""
    if FIXED_LOGS_PATH.exists():
        FIXED_LOGS_PATH.unlink()
    args = [
        PYTHON, "-m", "src",
        "--functions_definition", str(functions),
        "--input", str(prompts),
        "--output", str(output),
    ]
    result = subprocess.run(args, cwd=PROJECT_ROOT, capture_output=True, text=True, timeout=timeout)
    return result.returncode, result.stderr


def run_project_example(functions: Path, prompts: Path, output: Path, timeout: float = 180):
    """Corre el proyecto del companero via el adaptador (sus clases directo)."""
    args = [PYTHON, str(RUNNER_SCRIPT), str(functions), str(prompts), str(output)]
    result = subprocess.run(args, cwd=PROJECT_ROOT, capture_output=True, text=True, timeout=timeout)
    return result.returncode, result.stderr


def _es_correcto(resultado: dict | None, esperado: dict) -> bool:
    """Acierta si trae exactamente el name+parameters de la correccion. Un
    objeto de fallo (ERROR/_error) o ausente nunca cuenta como acierto."""
    if resultado is None:
        return False
    if "ERROR" in resultado or "_error" in resultado:
        return False
    return resultado.get("name") == esperado["name"] and resultado.get("parameters") == esperado["parameters"]


def _armar_comparacion(mio_resultados: list, companero_resultados: list, esperados: list, resumen) -> dict:
    mio_por_prompt = {r["prompt"]: r for r in mio_resultados}
    companero_por_prompt = {r["prompt"]: r for r in companero_resultados}
    comparacion = {}
    for e in esperados:
        prompt = e["prompt"]
        mio = mio_por_prompt.get(prompt)
        companero = companero_por_prompt.get(prompt)
        mio_ok = _es_correcto(mio, e)
        companero_ok = _es_correcto(companero, e)
        comparacion[prompt] = {
            "mio": mio,
            "companero": companero,
            "esperado": e,
            "mio_ok": mio_ok,
            "companero_ok": companero_ok,
        }
        resumen.registrar(mio_ok, companero_ok)
    return comparacion


def assert_no_pierde_contra_companero(prompt: str, comparacion: dict) -> None:
    """Unico criterio de rojo: yo fallo y el companero acierta ese mismo prompt."""
    fila = comparacion[prompt]
    perdio_contra_companero = (not fila["mio_ok"]) and fila["companero_ok"]
    assert not perdio_contra_companero, (
        f"Mi proyecto fallo y el del companero acerto en: {prompt!r}\n"
        f"  esperado:   {fila['esperado']}\n"
        f"  mio:        {fila['mio']}\n"
        f"  companero:  {fila['companero']}"
    )


# ---------------------------------------------------------------------------
# Comparativa contra tests/stress_data
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def stress_comparativo(tmp_path_factory, resumen_comparativo):
    """Corre ambos proyectos una sola vez contra el catalogo de estres y
    cachea la comparacion, para no repetir la carga cara del modelo."""
    workdir = tmp_path_factory.mktemp("stress_cmp")
    mio_output = workdir / "mio.json"
    companero_output = workdir / "companero.json"

    run_own_project(STRESS_FUNCTIONS, STRESS_PROMPTS, mio_output)
    run_project_example(STRESS_FUNCTIONS, STRESS_PROMPTS, companero_output)

    mio_resultados = json.loads(mio_output.read_text()) if mio_output.exists() else []
    companero_resultados = json.loads(companero_output.read_text())
    esperados = json.loads(STRESS_CORRECTIONS.read_text())

    return _armar_comparacion(mio_resultados, companero_resultados, esperados, resumen_comparativo)


def test_cmp_stress_anidacion_de_un_nivel(stress_comparativo):
    """fn_schedule_meeting (slot anidado, 1 nivel): si yo fallo y el companero acierta, es rojo."""
    assert_no_pierde_contra_companero("Schedule a meeting called Planning on Monday at 9", stress_comparativo)


def test_cmp_stress_anidacion_de_dos_niveles(stress_comparativo):
    """fn_create_order (customer.address, 2 niveles): si yo fallo y el companero acierta, es rojo."""
    assert_no_pierde_contra_companero("Create an order for Maria living in Austin, zip 73301", stress_comparativo)


def test_cmp_stress_prefijo_largo_compartido(stress_comparativo):
    """fn_get_user vs fn_get_user_details: si yo fallo y el companero acierta, es rojo."""
    assert_no_pierde_contra_companero("Get the full details for user 42", stress_comparativo)


def test_cmp_stress_tipo_float(stress_comparativo):
    """fn_convert_currency (amount/rate float): si yo fallo y el companero acierta, es rojo."""
    assert_no_pierde_contra_companero("Convert 250.75 dollars at a rate of 0.92", stress_comparativo)


def test_cmp_stress_tipo_boolean(stress_comparativo):
    """fn_toggle_notifications (enabled boolean): si yo fallo y el companero acierta, es rojo."""
    assert_no_pierde_contra_companero("Turn off notifications for user 7", stress_comparativo)


def test_cmp_stress_dos_parametros_del_mismo_tipo(stress_comparativo):
    """fn_calculate_difference (minuend/subtrahend, mismo tipo): si yo fallo y el companero acierta, es rojo."""
    assert_no_pierde_contra_companero("Subtract 15 from 50", stress_comparativo)


def test_cmp_stress_comillas_embebidas(stress_comparativo):
    """Comillas embebidas sin backslash: si yo fallo y el companero acierta, es rojo."""
    assert_no_pierde_contra_companero('Log the message: He said "welcome" today', stress_comparativo)


def test_cmp_stress_comillas_y_backslash_combinados(stress_comparativo):
    """Comillas + backslash combinados: si yo fallo y el companero acierta, es rojo."""
    assert_no_pierde_contra_companero('Log the message: He said "hi" from C:\\tmp', stress_comparativo)


def test_cmp_stress_corrida_completa(stress_comparativo):
    """Sobre el lote completo de estres, ningun prompt debe quedar en el unico caso de rojo: yo fallo y el companero acierta."""
    for prompt in stress_comparativo:
        assert_no_pierde_contra_companero(prompt, stress_comparativo)


# ---------------------------------------------------------------------------
# Comparativa contra tests/new_data (examen del companero)
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def companion_comparativo(tmp_path_factory, resumen_comparativo):
    """Corre ambos proyectos una sola vez contra el catalogo del 'examen' del
    companero y cachea la comparacion."""
    workdir = tmp_path_factory.mktemp("companion_cmp")
    mio_output = workdir / "mio.json"
    companero_output = workdir / "companero.json"

    run_own_project(COMPANION_FUNCTIONS, COMPANION_PROMPTS, mio_output)
    run_project_example(COMPANION_FUNCTIONS, COMPANION_PROMPTS, companero_output)

    mio_resultados = json.loads(mio_output.read_text()) if mio_output.exists() else []
    companero_resultados = json.loads(companero_output.read_text())
    esperados = json.loads(COMPANION_CORRECTIONS.read_text())

    return _armar_comparacion(mio_resultados, companero_resultados, esperados, resumen_comparativo)


def test_cmp_catalogo_del_companero(companion_comparativo):
    """Sobre los 11 prompts del examen del companero, ningun prompt debe quedar en el unico caso de rojo: yo fallo y el companero acierta."""
    for prompt in companion_comparativo:
        assert_no_pierde_contra_companero(prompt, companion_comparativo)
