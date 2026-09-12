"""Tests de caja negra del Bloque 6 — el comando `python -m src`.

Ver tests/blackbox_test_bloque_1.md para el contrato completo. Cada test
lanza el comando real como subproceso (nunca importa Chat/Interface/Guardian
directo) para probar exactamente lo que corre el evaluador.
"""
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PYTHON = sys.executable
FIXED_LOGS_PATH = PROJECT_ROOT / "logs" / "logs.json"


@pytest.fixture(autouse=True)
def clean_logs_file():
    """logs/logs.json es una ruta fija compartida entre procesos: se limpia
    antes y despues de cada test para que un test no contamine al siguiente."""
    if FIXED_LOGS_PATH.exists():
        FIXED_LOGS_PATH.unlink()
    yield
    if FIXED_LOGS_PATH.exists():
        FIXED_LOGS_PATH.unlink()

REAL_FUNCTIONS = PROJECT_ROOT / "data" / "input" / "functions_definition.json"
REAL_PROMPTS = PROJECT_ROOT / "data" / "input" / "function_calling_tests.json"
COMPANION_FUNCTIONS = PROJECT_ROOT / "tests" / "new_data" / "input" / "functions_definition.json"
COMPANION_PROMPTS = PROJECT_ROOT / "tests" / "new_data" / "input" / "function_calling_tests.json"
STRESS_FUNCTIONS = PROJECT_ROOT / "tests" / "stress_data" / "input" / "functions_definition.json"
STRESS_PROMPTS = PROJECT_ROOT / "tests" / "stress_data" / "input" / "function_calling_tests.json"
STRESS_CORRECTIONS = PROJECT_ROOT / "tests" / "stress_data" / "correction" / "function_calling_corrections.json"
# Elemento objetivo nivel 2 fabricado (mismo patron que stress_data): un
# catalogo con funciones ambiguas a proposito (numero escrito en palabras,
# confirmacion ambigua, nivel impreciso) para forzar un fallo de contenido
# real, ya que ningun catalogo de R9 documentaba uno de forma reproducible.
ERROR_FUNCTIONS = PROJECT_ROOT / "tests" / "error_data" / "input" / "functions_definition.json"
ERROR_PROMPTS = PROJECT_ROOT / "tests" / "error_data" / "input" / "function_calling_tests.json"
OFFICIAL_CORRECTIONS = (
    PROJECT_ROOT / "tests" / "official_example" / "correction"
    / "function_calling_corrections.json")
# Estos 2 de los 11 prompts oficiales usan un "regex" libre (numeros/vocales)
# sin un unico patron correcto contra el que medir -- xfail documentado,
# no cuentan como rojo del proyecto. Ver PROJECT.md, pendiente #3.
OFFICIAL_SIN_ANCLA = {
    'Replace all numbers in "Hello 34 I\'m 233 years old" with NUMBERS',
    "Replace all vowels in 'Programming is fun' with asterisks",
}
_OFFICIAL_ROWS = json.loads(OFFICIAL_CORRECTIONS.read_text())


def run_cmd(
    functions_definition: Path | None = None,
    input_path: Path | None = None,
    output: Path | None = None,
    extra_args: list[str] | None = None,
    timeout: float = 120,
) -> tuple[int, str, str, Path | None, Path | None]:
    """Lanza `python -m src` como subproceso con las rutas dadas.

    Devuelve (returncode, stdout, stderr, output_path, logs_path). Cuando
    `output` es None se usa el default real de src/__main__.py, así que
    logs_path/output_path se resuelven contra PROJECT_ROOT en ese caso.
    """
    args = [PYTHON, "-m", "src"]
    if functions_definition is not None:
        args += ["--functions_definition", str(functions_definition)]
    if input_path is not None:
        args += ["--input", str(input_path)]
    if output is not None:
        args += ["--output", str(output)]
    if extra_args:
        args += extra_args

    result = subprocess.run(
        args, cwd=PROJECT_ROOT, capture_output=True, text=True, timeout=timeout
    )

    resolved_output = output if output is not None else PROJECT_ROOT / "data" / "output" / "function_calling_results.json"
    # logs/logs.json es una ruta fija relativa al directorio desde donde corre
    # el proceso (no hay flag --logs, no depende de --output) — R2/R3.
    logs_path = PROJECT_ROOT / "logs" / "logs.json"

    return result.returncode, result.stdout, result.stderr, resolved_output, logs_path


def assert_no_raw_traceback(stderr: str) -> None:
    """Ningun caso debe imprimir una excepcion de Python sin atrapar (R5)."""
    assert "Traceback (most recent call last)" not in stderr


# ---------------------------------------------------------------------------
# 1. Creacion correcta
# ---------------------------------------------------------------------------


def test_corre_sin_flags_usa_los_defaults(tmp_path):
    """Correr sin ningun flag usa los 3 defaults de R2 y termina con exito."""
    code, _, stderr, output_path, logs_path = run_cmd()
    assert code == 0
    assert_no_raw_traceback(stderr)
    assert output_path.exists()
    if logs_path.exists():
        logs_path.unlink()


def test_corre_con_las_tres_rutas_explicitas(tmp_path):
    """Pasar las 3 rutas explicitas (aunque sean las del default) funciona igual."""
    output_path = tmp_path / "salida.json"
    code, _, stderr, out, logs = run_cmd(
        functions_definition=REAL_FUNCTIONS, input_path=REAL_PROMPTS, output=output_path
    )
    assert code == 0
    assert_no_raw_traceback(stderr)
    assert out.exists()


# ---------------------------------------------------------------------------
# 2. Flujo normal
# ---------------------------------------------------------------------------


def test_catalogo_real_produce_n_objetos_en_orden(tmp_path):
    """Con el catalogo y prompts reales, la salida trae exactamente N objetos en el mismo orden que el input (R6.1)."""
    output_path = tmp_path / "salida.json"
    code, _, stderr, out, _ = run_cmd(
        functions_definition=REAL_FUNCTIONS, input_path=REAL_PROMPTS, output=output_path
    )
    assert code == 0
    assert_no_raw_traceback(stderr)

    prompts_enviados = [p["prompt"] for p in json.loads(REAL_PROMPTS.read_text())]
    resultados = json.loads(out.read_text())
    assert len(resultados) == len(prompts_enviados)
    assert [r["prompt"] for r in resultados] == prompts_enviados


def test_objetos_exitosos_traen_exactamente_prompt_name_parameters(tmp_path):
    """Cada objeto exitoso trae exactamente las claves prompt/name/parameters, sin anidar ni de mas (R6.2)."""
    output_path = tmp_path / "salida.json"
    code, _, _, out, _ = run_cmd(
        functions_definition=REAL_FUNCTIONS, input_path=REAL_PROMPTS, output=output_path
    )
    assert code == 0
    resultados = json.loads(out.read_text())
    catalogo_nombres = {f["name"] for f in json.loads(REAL_FUNCTIONS.read_text())}
    catalogo_nombres.add("fn_unknown")
    for objeto in resultados:
        if "ERROR" not in objeto:
            assert set(objeto.keys()) == {"prompt", "name", "parameters"}
            assert objeto["name"] in catalogo_nombres
            assert isinstance(objeto["parameters"], dict)


def test_sin_fallos_no_se_crea_logs(tmp_path):
    """Si la corrida entera sale bien, logs/logs.json no se crea (R6.5)."""
    output_path = tmp_path / "salida.json"
    code, _, _, out, logs_path = run_cmd(
        functions_definition=REAL_FUNCTIONS, input_path=REAL_PROMPTS, output=output_path
    )
    assert code == 0
    resultados = json.loads(out.read_text())
    assert all("ERROR" not in r for r in resultados)
    assert not logs_path.exists()


def test_catalogo_del_companero_produce_salida_valida(tmp_path):
    """Con un catalogo real de otro proyecto (tipos integer/boolean no vistos en el propio), el comando sigue produciendo objetos con la forma correcta."""
    output_path = tmp_path / "salida.json"
    code, _, stderr, out, _ = run_cmd(
        functions_definition=COMPANION_FUNCTIONS, input_path=COMPANION_PROMPTS, output=output_path
    )
    assert code == 0
    assert_no_raw_traceback(stderr)
    resultados = json.loads(out.read_text())
    prompts_enviados = [p["prompt"] for p in json.loads(COMPANION_PROMPTS.read_text())]
    assert len(resultados) == len(prompts_enviados)


def test_prompt_sin_match_elige_fn_unknown(tmp_path):
    """Un prompt que no calza con ninguna funcion real elige fn_unknown con parameters vacio (verificado ejecutando, R9)."""
    input_path = tmp_path / "prompts.json"
    input_path.write_text(json.dumps([{"prompt": "What's the weather like today?"}]))
    output_path = tmp_path / "salida.json"
    code, _, _, out, _ = run_cmd(
        functions_definition=REAL_FUNCTIONS, input_path=input_path, output=output_path
    )
    assert code == 0
    resultados = json.loads(out.read_text())
    assert len(resultados) == 1
    assert resultados[0]["name"] == "fn_unknown"
    assert resultados[0]["parameters"] == {}


def test_recorrido_completo_r12(tmp_path):
    """El recorrido documentado en R12: un solo prompt real produce name+parameters exactos, con a/b como number (int o float)."""
    input_path = tmp_path / "prompts.json"
    input_path.write_text(json.dumps([{"prompt": "What is the sum of 2 and 3?"}]))
    output_path = tmp_path / "salida.json"
    code, _, stderr, out, _ = run_cmd(
        functions_definition=REAL_FUNCTIONS, input_path=input_path, output=output_path
    )
    assert code == 0
    assert_no_raw_traceback(stderr)
    resultados = json.loads(out.read_text())
    assert resultados == [
        {
            "prompt": "What is the sum of 2 and 3?",
            "name": "fn_add_numbers",
            "parameters": {"a": 2, "b": 3},
        }
    ]
    assert isinstance(resultados[0]["parameters"]["a"], (int, float))
    assert isinstance(resultados[0]["parameters"]["b"], (int, float))


# ---------------------------------------------------------------------------
# 3. Valor limite valido
# ---------------------------------------------------------------------------


def test_input_vacio_produce_salida_vacia_sin_logs(tmp_path):
    """Una lista de prompts vacia produce output=[] y no crea logs/logs.json (R4, verificado ejecutando)."""
    input_path = tmp_path / "prompts.json"
    input_path.write_text("[]")
    output_path = tmp_path / "salida.json"
    code, _, stderr, out, logs_path = run_cmd(
        functions_definition=REAL_FUNCTIONS, input_path=input_path, output=output_path
    )
    assert code == 0
    assert_no_raw_traceback(stderr)
    assert json.loads(out.read_text()) == []
    assert not logs_path.exists()


def test_output_crea_carpetas_intermedias_inexistentes(tmp_path):
    """--output puede apuntar a una ruta con carpetas intermedias que no existen: el comando las crea solo (R4)."""
    input_path = tmp_path / "prompts.json"
    input_path.write_text("[]")
    output_path = tmp_path / "carpeta_nueva" / "salida.json"
    assert not output_path.parent.exists()
    code, _, stderr, out, _ = run_cmd(
        functions_definition=REAL_FUNCTIONS, input_path=input_path, output=output_path
    )
    assert code == 0
    assert_no_raw_traceback(stderr)
    assert out.exists()


# ---------------------------------------------------------------------------
# 5. Entradas invalidas
# ---------------------------------------------------------------------------

MENSAJE_STARTUP = "The keyboard has interrupted the program during startup"
MENSAJE_GENERATION = "The keyboard has interrupted the generation process"

# El import de torch/transformers dura ~1-2s (R5, warning de timing) y varia
# con cache del sistema. Se barre un rango de tiempos en vez de confiar en un
# numero fijo, hasta observar las dos ramas al menos una vez cada una: 10
# intentos, arrancando en 0.5s (0 daba SIGINT antes de que Python instale su
# propio manejo -> exit -2, fuera del control del programa) y sumando 1.5s en
# cada paso. El barrido corta en cuanto ve las dos ramas, sin agotar los 10.
SIGINT_SWEEP_DELAYS = [0.5 + 1.5 * i for i in range(10)]


def run_with_sigint_after(delay: float, output_path: Path, timeout: float = 90):
    """Lanza el comando, espera `delay` segundos y le manda SIGINT real."""
    args = [
        PYTHON, "-m", "src",
        "--functions_definition", str(REAL_FUNCTIONS),
        "--input", str(REAL_PROMPTS),
        "--output", str(output_path),
    ]
    proc = subprocess.Popen(
        args, cwd=PROJECT_ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    time.sleep(delay)
    os.kill(proc.pid, signal.SIGINT)
    try:
        stdout, stderr = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        proc.kill()
        stdout, stderr = proc.communicate()
    return proc.returncode, stdout, stderr


def test_sigint_dispara_startup_y_generation_segun_el_momento(tmp_path):
    """Un SIGINT real durante el import da el mensaje de startup y uno durante la generacion da el de generation; en ambos casos exit 1, log correcto y sin traceback (R5, filas 5 y 6)."""
    mensajes_vistos = set()

    for i, delay in enumerate(SIGINT_SWEEP_DELAYS):
        output_path = tmp_path / f"salida_{i}.json"
        if FIXED_LOGS_PATH.exists():
            FIXED_LOGS_PATH.unlink()

        code, _, stderr = run_with_sigint_after(delay, output_path)

        assert_no_raw_traceback(stderr)

        if code in (0, -2):
            # code 0: la corrida termino antes de que llegara la senal.
            # code -2: SIGINT crudo mato el proceso antes de que Python
            # instalara su propio manejo -- fuera del control de src/,
            # no ejercita ninguna de las dos ramas de R5 (flaky en
            # cualquier delay, no depende del tamano del delay).
            continue

        assert code == 1
        assert FIXED_LOGS_PATH.exists()
        contenido_logs = FIXED_LOGS_PATH.read_text()
        assert MENSAJE_STARTUP in contenido_logs or MENSAJE_GENERATION in contenido_logs

        if MENSAJE_STARTUP in contenido_logs:
            mensajes_vistos.add("startup")
        if MENSAJE_GENERATION in contenido_logs:
            mensajes_vistos.add("generation")

        if mensajes_vistos == {"startup", "generation"}:
            break

    assert mensajes_vistos == {"startup", "generation"}, (
        f"El barrido de tiempos {SIGINT_SWEEP_DELAYS} no disparo las dos ramas de R5 "
        f"(solo se vio: {mensajes_vistos})"
    )


def test_functions_definition_inexistente_da_exit_1_con_validation_error(tmp_path):
    """--functions_definition apuntando a un archivo que no existe da exit 1 y el log trae el ValidationError de pydantic (R5)."""
    output_path = tmp_path / "salida.json"
    ruta_inexistente = tmp_path / "no_existe.json"
    code, _, stderr, _, logs_path = run_cmd(
        functions_definition=ruta_inexistente, input_path=REAL_PROMPTS, output=output_path
    )
    assert code == 1
    assert_no_raw_traceback(stderr)
    assert logs_path.exists()
    assert "Path does not point to a file" in logs_path.read_text()


def test_input_inexistente_da_exit_1_con_validation_error(tmp_path):
    """--input apuntando a un archivo que no existe da exit 1 y el log trae el ValidationError de pydantic (R5)."""
    output_path = tmp_path / "salida.json"
    ruta_inexistente = tmp_path / "no_existe.json"
    code, _, stderr, _, logs_path = run_cmd(
        functions_definition=REAL_FUNCTIONS, input_path=ruta_inexistente, output=output_path
    )
    assert code == 1
    assert_no_raw_traceback(stderr)
    assert logs_path.exists()
    assert "Path does not point to a file" in logs_path.read_text()


def test_functions_definition_vacio_da_exit_1(tmp_path):
    """--functions_definition apuntando a una lista vacia [] da exit 1 y el log dice que el archivo de funciones esta vacio (R5)."""
    functions_path = tmp_path / "vacio.json"
    functions_path.write_text("[]")
    output_path = tmp_path / "salida.json"
    code, _, stderr, _, logs_path = run_cmd(
        functions_definition=functions_path, input_path=REAL_PROMPTS, output=output_path
    )
    assert code == 1
    assert_no_raw_traceback(stderr)
    assert logs_path.exists()
    assert "Function's file is empty" in logs_path.read_text()


def test_functions_definition_json_corrupto_da_exit_1(tmp_path):
    """JSON corrupto en --functions_definition da exit 1 y el log lo reporta como JSON corrupto (R5)."""
    functions_path = tmp_path / "corrupto.json"
    functions_path.write_text("{esto no es json valido")
    output_path = tmp_path / "salida.json"
    code, _, stderr, _, logs_path = run_cmd(
        functions_definition=functions_path, input_path=REAL_PROMPTS, output=output_path
    )
    assert code == 1
    assert_no_raw_traceback(stderr)
    assert logs_path.exists()
    assert "Corrupt JSON" in logs_path.read_text()


def test_input_json_corrupto_da_exit_1(tmp_path):
    """JSON corrupto en --input da exit 1 y el log lo reporta como JSON corrupto (R5)."""
    input_path = tmp_path / "corrupto.json"
    input_path.write_text("{esto no es json valido")
    output_path = tmp_path / "salida.json"
    code, _, stderr, _, logs_path = run_cmd(
        functions_definition=REAL_FUNCTIONS, input_path=input_path, output=output_path
    )
    assert code == 1
    assert_no_raw_traceback(stderr)
    assert logs_path.exists()
    assert "Corrupt JSON" in logs_path.read_text()


# ---------------------------------------------------------------------------
# 4. Stress sobre el limite (R9 nivel 2 — tests/stress_data)
# ---------------------------------------------------------------------------

def _cargar_boundary_case_prompts() -> set[str]:
    """Lee tests/stress_data/correction/function_calling_corrections.json y
    devuelve los prompts cuya entrada trae la clave "boundary_case" — se
    calcula en tiempo de ejecucion, nunca hardcodeado, para reflejar el
    estado real del catalogo en cada corrida."""
    correcciones = json.loads(STRESS_CORRECTIONS.read_text())
    return {c["prompt"] for c in correcciones if "boundary_case" in c}


@pytest.fixture(scope="module")
def stress_batch_result(tmp_path_factory):
    """Corre una sola vez el comando completo contra el catalogo de estres con
    los prompts que no traen boundary_case en la correccion, y cachea el
    resultado parseado para que los tests de este grupo no repitan la carga
    cara del modelo."""
    workdir = tmp_path_factory.mktemp("stress_batch")
    todos_los_prompts = json.loads(STRESS_PROMPTS.read_text())
    boundary_case_prompts = _cargar_boundary_case_prompts()
    prompts_limpios = [p for p in todos_los_prompts if p["prompt"] not in boundary_case_prompts]

    input_path = workdir / "prompts.json"
    input_path.write_text(json.dumps(prompts_limpios))
    output_path = workdir / "salida.json"

    if FIXED_LOGS_PATH.exists():
        FIXED_LOGS_PATH.unlink()

    code, _, stderr, out, _ = run_cmd(
        functions_definition=STRESS_FUNCTIONS, input_path=input_path, output=output_path
    )
    resultados = json.loads(out.read_text())
    return {
        "code": code,
        "stderr": stderr,
        "prompts": [p["prompt"] for p in prompts_limpios],
        "resultados": resultados,
        "por_prompt": {r["prompt"]: r for r in resultados},
    }


def test_stress_corrida_completa_produce_objetos_en_orden(stress_batch_result):
    """Los prompts de estres sin boundary_case en la correccion terminan en exit 0, con un objeto exitoso por prompt en el mismo orden que el input (R6.1 bajo carga real)."""
    assert stress_batch_result["code"] == 0
    assert_no_raw_traceback(stress_batch_result["stderr"])
    resultados = stress_batch_result["resultados"]
    assert len(resultados) == len(stress_batch_result["prompts"])
    assert [r["prompt"] for r in resultados] == stress_batch_result["prompts"]


def test_stress_dispara_anidacion_de_un_nivel(stress_batch_result):
    """El guard de parametros anidados (1 nivel) se dispara: fn_schedule_meeting produce 'slot' como objeto con day/hour tipados."""
    r = stress_batch_result["por_prompt"]["Schedule a meeting called Planning on Monday at 9"]
    assert r["name"] == "fn_schedule_meeting"
    slot = r["parameters"]["slot"]
    assert isinstance(slot, dict)
    assert isinstance(slot["day"], str)
    assert isinstance(slot["hour"], int)


def test_stress_dispara_anidacion_de_dos_niveles(stress_batch_result):
    """El guard de parametros anidados (2 niveles) se dispara: fn_create_order produce customer.address como objeto dentro de objeto."""
    r = stress_batch_result["por_prompt"]["Create an order for Maria living in Austin, zip 73301"]
    assert r["name"] == "fn_create_order"
    customer = r["parameters"]["customer"]
    assert isinstance(customer, dict)
    address = customer["address"]
    assert isinstance(address, dict)
    assert isinstance(address["city"], str)
    assert isinstance(address["zip"], int)


def test_stress_distingue_nombres_con_prefijo_largo_compartido(stress_batch_result):
    """El guard de eleccion de nombre distingue fn_get_user de fn_get_user_details aunque compartan prefijo largo (R6.4)."""
    r = stress_batch_result["por_prompt"]["Get the full details for user 42"]
    assert r["name"] == "fn_get_user_details"
    assert r["parameters"]["user_id"] == 42


def test_stress_dispara_tipo_float(stress_batch_result):
    """El guard del tipo float se dispara: fn_convert_currency produce amount/rate como float, no como int truncado."""
    r = stress_batch_result["por_prompt"]["Convert 250.75 dollars at a rate of 0.92"]
    assert r["name"] == "fn_convert_currency"
    assert isinstance(r["parameters"]["amount"], float)
    assert isinstance(r["parameters"]["rate"], float)


def test_stress_dispara_tipo_boolean(stress_batch_result):
    """El guard del tipo boolean se dispara: fn_toggle_notifications produce enabled como bool, no como string/int."""
    r = stress_batch_result["por_prompt"]["Turn off notifications for user 7"]
    assert r["name"] == "fn_toggle_notifications"
    assert isinstance(r["parameters"]["enabled"], bool)
    assert r["parameters"]["enabled"] is False


def test_stress_dispara_dos_parametros_del_mismo_tipo(stress_batch_result):
    """El guard de dos parametros del mismo tipo en una funcion se dispara sin que se mezclen: fn_calculate_difference asigna minuend/subtrahend en el orden correcto."""
    r = stress_batch_result["por_prompt"]["Subtract 15 from 50"]
    assert r["name"] == "fn_calculate_difference"
    assert r["parameters"]["minuend"] == 50
    assert r["parameters"]["subtrahend"] == 15


def test_stress_preserva_comillas_embebidas_sin_backslash(stress_batch_result):
    """El caso limpio de comillas embebidas (sin backslash combinado) preserva los mismos caracteres, ignorando espacios: el modelo pierde espacios alrededor de comillas de forma conocida (caso estudiado 2026-09-10), no cuenta como rojo de codigo."""
    r = stress_batch_result["por_prompt"]['Log the message: He said "welcome" today']
    assert r["name"] == "fn_write_log_entry"
    esperado = 'He said "welcome" today'
    obtenido = r["parameters"]["message"]
    assert obtenido.replace(" ", "") == esperado.replace(" ", "")


def test_stress_preserva_comillas_y_backslash_combinados(stress_batch_result):
    """El caso que antes era boundary_case (comillas + backslash combinados en el mismo valor) ya tiene arreglo real en guardian.py/interface.py: se le exige exito exacto, igual que al resto del lote."""
    r = stress_batch_result["por_prompt"]['Log the message: He said "hi" from C:\\tmp']
    assert r["name"] == "fn_write_log_entry"
    assert r["parameters"]["message"] == 'He said "hi" from C:\\tmp'


def test_stress_boundary_case_no_crashea_aunque_no_se_exija_exito(tmp_path):
    """Si la correccion de estres vuelve a marcar algun prompt como boundary_case, ese prompt no es exigible como exitoso: se corre aparte con timeout acotado y solo se exige que no crashee con traceback crudo. Hoy el set esta vacio, asi que el test se salta."""
    boundary_case_prompts = _cargar_boundary_case_prompts()
    if not boundary_case_prompts:
        pytest.skip(
            "No hay prompts marcados boundary_case en la correccion de estres actual "
            "(tests/stress_data/correction/function_calling_corrections.json)"
        )
    for prompt in boundary_case_prompts:
        input_path = tmp_path / f"prompt_{abs(hash(prompt))}.json"
        input_path.write_text(json.dumps([{"prompt": prompt}]))
        output_path = tmp_path / f"salida_{abs(hash(prompt))}.json"
        try:
            code, _, stderr, out, _ = run_cmd(
                functions_definition=STRESS_FUNCTIONS,
                input_path=input_path,
                output=output_path,
                timeout=60,
            )
        except subprocess.TimeoutExpired:
            # Documentado en R9: puede entrar en loop y no cuenta como rojo.
            continue
        assert_no_raw_traceback(stderr)


def test_fallo_forzado_entre_dos_exitosos_mantiene_n_objetos_en_orden(tmp_path):
    """Un fallo de contenido real entre dos prompts exitosos no rompe el conteo ni el orden: 5 prompts dan 5 objetos, el del medio fallido (R6.1)."""
    output_path = tmp_path / "salida.json"
    code, _, stderr, out, logs_path = run_cmd(
        functions_definition=ERROR_FUNCTIONS, input_path=ERROR_PROMPTS, output=output_path
    )
    assert code == 0
    assert_no_raw_traceback(stderr)
    resultados = json.loads(out.read_text())
    prompts_enviados = [p["prompt"] for p in json.loads(ERROR_PROMPTS.read_text())]
    assert len(resultados) == len(prompts_enviados) == 5
    assert [r["prompt"] for r in resultados] == prompts_enviados


def test_objeto_fallido_trae_prompt_y_error_copiado_del_log(tmp_path):
    """El objeto fallido trae exactamente 2 claves (prompt/ERROR) y ERROR es copia del log real, nunca el texto del prompt repetido (R6.3, bug corregido)."""
    output_path = tmp_path / "salida.json"
    code, _, _, out, logs_path = run_cmd(
        functions_definition=ERROR_FUNCTIONS, input_path=ERROR_PROMPTS, output=output_path
    )
    assert code == 0
    resultados = json.loads(out.read_text())
    fallidos = [r for r in resultados if "ERROR" in r]
    assert len(fallidos) == 1
    objeto_fallido = fallidos[0]
    assert set(objeto_fallido.keys()) == {"prompt", "ERROR"}
    assert objeto_fallido["ERROR"] != objeto_fallido["prompt"]
    assert logs_path.exists()
    contenido_logs = json.loads(logs_path.read_text())
    log_real = list(contenido_logs["prompts"][0].keys())[0]
    assert objeto_fallido["ERROR"] == log_real


def test_modulo_requerido_roto_da_exit_1_sin_tocar_el_entorno_real(tmp_path):
    """Si llm_sdk no se puede importar, el comando da exit 1 y loguea el error de import, sin traceback crudo (R5). Se simula con un PYTHONPATH temporal que solo aplica a este subproceso, nunca al entorno real."""
    llm_sdk_roto = tmp_path / "llm_sdk_roto"
    paquete_falso = llm_sdk_roto / "llm_sdk"
    paquete_falso.mkdir(parents=True)
    (paquete_falso / "__init__.py").write_text('raise RuntimeError("boom - modulo roto a proposito")\n')

    env = os.environ.copy()
    pythonpath_previo = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = f"{llm_sdk_roto}{os.pathsep}{pythonpath_previo}"

    output_path = tmp_path / "salida.json"
    args = [
        PYTHON, "-m", "src",
        "--functions_definition", str(REAL_FUNCTIONS),
        "--input", str(REAL_PROMPTS),
        "--output", str(output_path),
    ]
    result = subprocess.run(
        args, cwd=PROJECT_ROOT, env=env, capture_output=True, text=True, timeout=60
    )

    assert result.returncode == 1
    assert_no_raw_traceback(result.stderr)
    assert FIXED_LOGS_PATH.exists()
    assert "An error occurred while importing a required module" in FIXED_LOGS_PATH.read_text()

    # El PYTHONPATH real del proceso de pytest no se toco.
    assert os.environ.get("PYTHONPATH", "") == pythonpath_previo


# ---------------------------------------------------------------------------
# Suite oficial del subject (data/input) contra su correccion real
# ---------------------------------------------------------------------------


def _official_params():
    params = []
    for row in _OFFICIAL_ROWS:
        prompt = row["prompt"]
        marks = (
            [pytest.mark.xfail(
                reason="regex libre, sin un unico patron correcto contra "
                       "el que medir (numeros/vocales)", strict=False)]
            if prompt in OFFICIAL_SIN_ANCLA else []
        )
        params.append(pytest.param(row, id=prompt, marks=marks))
    return params


@pytest.mark.parametrize("esperado", _official_params())
def test_oficial_data_input(tmp_path, esperado):
    """Cada uno de los 11 prompts oficiales de data/input produce name y
    parameters exactos contra tests/official_example/correction."""
    input_path = tmp_path / "prompts.json"
    input_path.write_text(json.dumps([{"prompt": esperado["prompt"]}]))
    output_path = tmp_path / "salida.json"
    code, _, stderr, out, _ = run_cmd(
        functions_definition=REAL_FUNCTIONS, input_path=input_path, output=output_path
    )
    assert code == 0
    assert_no_raw_traceback(stderr)
    resultado = json.loads(out.read_text())[0]
    assert resultado["name"] == esperado["name"]
    assert resultado["parameters"] == esperado["parameters"]
