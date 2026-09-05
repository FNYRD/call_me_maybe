"""Tests de caja negra del Bloque 5 - clase Interface.

Contrato: tests/blackbox_test_bloque_5.md
Nada de src/ se lee: solo se importa y se ejecuta.

Regla de cifras (correccion del contrato del 2026-09-03):
  - un numero que MIDE un artefacto real (cuantos prompts hay, cuanto mide el
    mas largo, cuantas posiciones tiene el vocabulario) se saca del artefacto
    dentro del test, nunca se clava a mano;
  - un valor que es una PROMESA del contrato (las cuatro cadenas de log, las
    tres claves prompt/name/parameters) se clava literal: eso es lo que se
    esta comprobando.
"""

import json
from pathlib import Path
from typing import Callable, List

import pytest
from pydantic import ValidationError

from llm_sdk import Small_LLM_Model
from src.filemanager import FileManager, Function, Prompt, TypeSpec
from src.interface import Interface, Output


RAIZ = Path(__file__).resolve().parent.parent
FUNCIONES = RAIZ / "data" / "input" / "functions_definition.json"
PROMPTS = RAIZ / "data" / "input" / "function_calling_tests.json"

# Promesas del contrato: valores literales, no medidos.
LOGS_VALIDOS = {
    'The prompt was empty',
    'Model failed while replying',
    'Model entered an loop',
    'The prompt was replied correctly',
}
LOG_VACIO = 'The prompt was empty'
LOG_FALLO = 'Model failed while replying'
LOG_BUCLE = 'Model entered an loop'
LOG_CORRECTO = 'The prompt was replied correctly'
CLAVES_DEL_JSON = {"prompt", "name", "parameters"}


# --------------------------------------------------------------------------
# E1..E4 - los elementos objetivos reales, cargados una sola vez por sesion
# --------------------------------------------------------------------------

@pytest.fixture(scope="session")
def salida_temporal(tmp_path_factory) -> Path:
    """Ruta de salida que pide FileManager. Nunca se escribe dentro de data/."""
    ruta = tmp_path_factory.mktemp("salida") / "salida.json"
    ruta.write_text("[]")
    return ruta


@pytest.fixture(scope="session")
def gestor(salida_temporal: Path) -> FileManager:
    return FileManager(FUNCIONES, PROMPTS, salida_temporal)


@pytest.fixture(scope="session")
def funciones(gestor: FileManager) -> List[Function]:
    """E1 - el catalogo real entero, tal como este hoy en el archivo."""
    return gestor.get_functions()


@pytest.fixture(scope="session")
def prompts(gestor: FileManager) -> List[str]:
    """E2 - los prompts reales, tal como esten hoy en el archivo."""
    lista: List[Prompt] = gestor.get_prompts()
    return [p.prompt for p in lista]


@pytest.fixture(scope="session")
def prompt_mas_largo(prompts: List[str]) -> str:
    """El mayor del archivo real, medido; no una cadena escrita a mano."""
    return max(prompts, key=len)


@pytest.fixture(scope="session")
def prompt_mas_corto(prompts: List[str]) -> str:
    """El menor del archivo real, medido."""
    return min(prompts, key=len)


@pytest.fixture(scope="session")
def modelo() -> Small_LLM_Model:
    """E3 y E4 - el modelo real. Carga cara: una sola vez para toda la suite."""
    return Small_LLM_Model()


@pytest.fixture(scope="session")
def tamano_vocabulario(modelo: Small_LLM_Model) -> int:
    """Cuantas posiciones tiene la lista de logits del modelo real. Medido una vez."""
    return len(modelo.get_logits_from_input_ids([9707]))


@pytest.fixture(scope="session")
def cara(funciones: List[Function], modelo: Small_LLM_Model) -> Interface:
    """La instancia real, la misma para todos los prompts (R3)."""
    return Interface(
        funciones,
        modelo.get_path_to_vocab_file(),
        modelo.get_path_to_merges_file(),
        modelo.get_path_to_tokenizer_file(),
        modelo.get_logits_from_input_ids,
    )


@pytest.fixture(scope="session")
def resultados_reales(cara: Interface, prompts: List[str]) -> dict:
    """Todos los prompts reales pasados por reply una sola vez.

    El universo completo de R6 se recorre aqui; los tests de invariante leen
    de este diccionario en vez de volver a generar.
    """
    return {texto: cara.reply(texto) for texto in prompts}


@pytest.fixture(scope="session")
def correctos(resultados_reales: dict) -> dict:
    """Solo los prompts que salieron en estado correcto (R4 admite el corte)."""
    return {t: r for t, r in resultados_reales.items() if r.log == LOG_CORRECTO}


# --------------------------------------------------------------------------
# E5 - las funciones de logits simuladas
#
# El tamano de la lista se recibe medido del modelo real: la simulada
# reproduce la caracteristica, no una cifra copiada.
# --------------------------------------------------------------------------

def hacer_logits_planos(tamano: int) -> Callable[[List[int]], List[float]]:
    """E5 plana: misma puntuacion para todos los ids. Dispara el tope (R6.4)."""
    def logits_planos(ids: List[int]) -> List[float]:
        assert isinstance(ids, list) and all(isinstance(i, int) for i in ids)
        return [0.0] * tamano
    return logits_planos


def hacer_logits_que_lanzan(tamano: int, vuelta: int = 1) -> Callable[[List[int]], List[float]]:
    """E5 que lanza: RuntimeError en la vuelta pedida. Dispara el fallo (R6.3)."""
    estado = {"llamadas": 0}

    def logits_que_lanzan(ids: List[int]) -> List[float]:
        estado["llamadas"] += 1
        if estado["llamadas"] >= vuelta:
            raise RuntimeError("el modelo simulado ha fallado")
        return [0.0] * tamano

    logits_que_lanzan.estado = estado  # type: ignore[attr-defined]
    return logits_que_lanzan


def hacer_logits_contadores(tamano: int) -> Callable[[List[int]], List[float]]:
    """E5 que cuenta cuantas veces se la llama y con que entradas."""
    estado = {"llamadas": 0, "entradas": []}

    def logits_contadores(ids: List[int]) -> List[float]:
        estado["llamadas"] += 1
        estado["entradas"].append(list(ids))
        return [0.0] * tamano

    logits_contadores.estado = estado  # type: ignore[attr-defined]
    return logits_contadores


def cara_simulada(funciones: List[Function], modelo: Small_LLM_Model,
                  logits: Callable[[List[int]], List[float]]) -> Interface:
    """Misma clase, mismas rutas reales, con la funcion de logits del test (R7)."""
    return Interface(
        funciones,
        modelo.get_path_to_vocab_file(),
        modelo.get_path_to_merges_file(),
        modelo.get_path_to_tokenizer_file(),
        logits,
    )


# ==========================================================================
# 0 - LOS ELEMENTOS OBJETIVOS ESTAN AHI Y NO ESTAN VACIOS
# ==========================================================================

def test_los_elementos_objetivos_reales_no_estan_vacios(funciones, prompts, tamano_vocabulario):
    """Garantiza que el universo contra el que se contrastan las invariantes existe: catalogo, prompts y vocabulario medidos, no supuestos."""
    assert len(funciones) > 0
    assert len(prompts) > 0
    assert tamano_vocabulario > 0
    assert len({f.name for f in funciones}) == len(funciones)


# ==========================================================================
# 1 - CREACION CORRECTA (R4 · __init__)
# ==========================================================================

def test_init_construye_con_el_catalogo_real_completo(funciones, modelo):
    """Garantiza que Interface se construye con el catalogo real entero y las rutas del SDK."""
    face = Interface(
        funciones,
        modelo.get_path_to_vocab_file(),
        modelo.get_path_to_merges_file(),
        modelo.get_path_to_tokenizer_file(),
        modelo.get_logits_from_input_ids,
    )
    assert isinstance(face, Interface)


def test_init_construye_con_una_sola_funcion(funciones, modelo):
    """Garantiza que un catalogo de una sola Function tambien es aceptado, sea cual sea la funcion."""
    for funcion in funciones:
        face = Interface(
            [funcion],
            modelo.get_path_to_vocab_file(),
            modelo.get_path_to_merges_file(),
            modelo.get_path_to_tokenizer_file(),
            modelo.get_logits_from_input_ids,
        )
        assert isinstance(face, Interface)


def test_init_acepta_las_rutas_como_str_y_como_path(funciones, modelo):
    """Garantiza que FilePath admite las tres rutas tanto en str como en Path."""
    rutas = [
        modelo.get_path_to_vocab_file(),
        modelo.get_path_to_merges_file(),
        modelo.get_path_to_tokenizer_file(),
    ]
    como_str = Interface(funciones, str(rutas[0]), str(rutas[1]), str(rutas[2]),
                         modelo.get_logits_from_input_ids)
    como_path = Interface(funciones, Path(rutas[0]), Path(rutas[1]), Path(rutas[2]),
                          modelo.get_logits_from_input_ids)
    assert isinstance(como_str, Interface) and isinstance(como_path, Interface)


def test_init_no_llama_a_la_funcion_de_logits(funciones, modelo, tamano_vocabulario):
    """Garantiza que construir no pide ni un logit: el Callable se guarda, no se usa."""
    logits = hacer_logits_contadores(tamano_vocabulario)
    cara_simulada(funciones, modelo, logits)
    assert logits.estado["llamadas"] == 0


# ==========================================================================
# 2 - FLUJO NORMAL (R4 · reply, con E4 el modelo real)
# ==========================================================================

def test_reply_devuelve_un_output_para_todos_los_prompts_reales(resultados_reales, prompts):
    """R6.1: reply devuelve siempre un Output, nunca None ni otra cosa, en todos los prompts del archivo."""
    assert len(resultados_reales) == len(prompts)
    for texto, resultado in resultados_reales.items():
        assert isinstance(resultado, Output), texto


def test_reply_solo_devuelve_uno_de_los_cuatro_logs(resultados_reales):
    """R6.2: log es siempre una de las cuatro cadenas exactas del contrato."""
    for texto, resultado in resultados_reales.items():
        assert resultado.log in LOGS_VALIDOS, (texto, resultado.log)


def test_reply_deja_algun_prompt_real_en_estado_correcto(correctos, resultados_reales):
    """Garantiza que el flujo real llega a completarse: si ninguno sale correcto, las invariantes de estructura no prueban nada."""
    assert correctos, {t: r.log for t, r in resultados_reales.items()}


def test_reply_devuelve_json_parseable_de_tres_claves(correctos):
    """R6.6: en estado correcto output es un dict con exactamente prompt, name y parameters."""
    for texto, resultado in correctos.items():
        objeto = resultado.output
        assert set(objeto) == CLAVES_DEL_JSON, (texto, objeto)


def test_reply_conserva_el_prompt_crudo_en_la_clave_prompt(correctos):
    """Garantiza que la clave prompt del dict es el mismo texto que se le paso a reply."""
    for texto, resultado in correctos.items():
        assert resultado.output["prompt"] == texto


# ==========================================================================
# 3 - INVARIANTES CONTRA EL CATALOGO ENTERO (R6.8, R6.9, R6.10)
# ==========================================================================

def test_reply_elige_siempre_un_nombre_del_catalogo(correctos, funciones):
    """R6.8: name es uno de los nombres del catalogo que recibio el constructor."""
    nombres = {f.name for f in funciones}
    for texto, resultado in correctos.items():
        assert resultado.output["name"] in nombres, texto


def test_reply_escribe_exactamente_los_parametros_del_schema(correctos, funciones):
    """R6.9: las claves de parameters son las del schema de esa funcion, todas y sin sobrantes."""
    schema = {f.name: set(f.parameters) for f in funciones}
    for texto, resultado in correctos.items():
        objeto = resultado.output
        assert set(objeto["parameters"]) == schema[objeto["name"]], (texto, objeto)


def test_reply_respeta_el_tipo_declarado_de_cada_parametro(correctos, funciones):
    """R6.10: un parametro number sale como numero JSON y uno string sale como cadena."""
    tipos = {f.name: {n: p.type for n, p in f.parameters.items()} for f in funciones}
    for texto, resultado in correctos.items():
        objeto = resultado.output
        for nombre, valor in objeto["parameters"].items():
            declarado = tipos[objeto["name"]][nombre]
            if declarado == "number":
                assert isinstance(valor, (int, float)) and not isinstance(valor, bool), (texto, nombre, valor)
            elif declarado == "string":
                assert isinstance(valor, str), (texto, nombre, valor)
            else:
                pytest.fail(f"tipo no contemplado en el contrato: {declarado}")


def test_reply_no_deja_vacia_una_hoja_string(correctos, funciones):
    """R8.1: no se exige texto legible, pero si que el valor de una hoja string no este vacio."""
    tipos = {f.name: {n: p.type for n, p in f.parameters.items()} for f in funciones}
    for texto, resultado in correctos.items():
        objeto = resultado.output
        for nombre, valor in objeto["parameters"].items():
            if tipos[objeto["name"]][nombre] == "string":
                assert valor != "", (texto, nombre)


def test_reply_recorre_el_catalogo_entero_sin_inventar_nombres(correctos, funciones):
    """R6.8 por el otro lado: ningun nombre devuelto queda fuera del catalogo, ni siquiera por mayusculas o espacios."""
    nombres = {f.name for f in funciones}
    devueltos = {r.output["name"] for r in correctos.values()}
    assert devueltos <= nombres, devueltos - nombres


# ==========================================================================
# 4 - INDEPENDENCIA ENTRE LLAMADAS (R6.7)
# ==========================================================================

def test_reply_no_depende_de_las_llamadas_anteriores(funciones, modelo, cara, prompt_mas_corto):
    """R6.7: el mismo prompt da el mismo Output en la misma instancia y en una recien creada."""
    primera = cara.reply(prompt_mas_corto)
    segunda = cara.reply(prompt_mas_corto)
    otra = Interface(
        funciones,
        modelo.get_path_to_vocab_file(),
        modelo.get_path_to_merges_file(),
        modelo.get_path_to_tokenizer_file(),
        modelo.get_logits_from_input_ids,
    ).reply(prompt_mas_corto)
    assert primera.log == segunda.log == otra.log
    assert primera.output == segunda.output == otra.output


def test_reply_no_se_contamina_con_el_prompt_vacio_en_medio(cara, prompt_mas_corto):
    """R6.7: intercalar un prompt vacio no cambia el resultado del siguiente prompt real."""
    antes = cara.reply(prompt_mas_corto)
    vacio = cara.reply("")
    despues = cara.reply(prompt_mas_corto)
    assert vacio.log == LOG_VACIO
    assert antes.output == despues.output and antes.log == despues.log


# ==========================================================================
# 5 - VALOR LIMITE VALIDO (R4, E2: el prompt mas corto y el mas largo, medidos)
# ==========================================================================

def test_reply_con_el_prompt_real_mas_largo(resultados_reales, prompts, prompt_mas_largo):
    """Garantiza que el prompt mayor del archivo real sale por un log valido y sin excepcion."""
    assert len(prompt_mas_largo) == max(len(t) for t in prompts)
    resultado = resultados_reales[prompt_mas_largo]
    assert isinstance(resultado, Output)
    assert resultado.log in LOGS_VALIDOS


def test_reply_con_el_prompt_real_mas_corto(resultados_reales, prompts, prompt_mas_corto):
    """Garantiza que el prompt menor del archivo real sale por un log valido y sin excepcion."""
    assert len(prompt_mas_corto) == min(len(t) for t in prompts)
    resultado = resultados_reales[prompt_mas_corto]
    assert isinstance(resultado, Output)
    assert resultado.log in LOGS_VALIDOS


def test_reply_con_prompt_vacio_devuelve_el_estado_vacio(cara):
    """R4 y R6.2: la cadena vacia devuelve log 'The prompt was empty' y output {"prompt": ""}."""
    resultado = cara.reply("")
    assert resultado.log == LOG_VACIO
    assert resultado.output == {"prompt": ""}


def test_reply_con_prompt_vacio_no_pide_ni_un_logit(funciones, modelo, tamano_vocabulario):
    """R6.5: con user_prompt vacio el Callable no se llama ninguna vez."""
    logits = hacer_logits_contadores(tamano_vocabulario)
    resultado = cara_simulada(funciones, modelo, logits).reply("")
    assert logits.estado["llamadas"] == 0
    assert resultado.log == LOG_VACIO and resultado.output == {"prompt": ""}


# ==========================================================================
# 6 - STRESS SOBRE EL LIMITE: cada guard declarado se dispara al menos una vez
# ==========================================================================

def test_reply_atrapa_el_fallo_de_los_logits_en_la_primera_vuelta(funciones, modelo, tamano_vocabulario, prompt_mas_corto):
    """R6.3: si la funcion de logits lanza, reply no propaga: devuelve 'Model failed while replying'."""
    face = cara_simulada(funciones, modelo, hacer_logits_que_lanzan(tamano_vocabulario, vuelta=1))
    resultado = face.reply(prompt_mas_corto)
    assert resultado.log == LOG_FALLO
    assert resultado.output == {"prompt": prompt_mas_corto}


def test_reply_atrapa_el_fallo_de_los_logits_en_una_vuelta_posterior(funciones, modelo, tamano_vocabulario, prompt_mas_corto):
    """R6.3: el fallo tardio tambien se atrapa y devuelve el mismo estado {"prompt": user_prompt}."""
    face = cara_simulada(funciones, modelo, hacer_logits_que_lanzan(tamano_vocabulario, vuelta=5))
    resultado = face.reply(prompt_mas_corto)
    assert resultado.log == LOG_FALLO
    assert resultado.output == {"prompt": prompt_mas_corto}


def test_reply_atrapa_el_fallo_con_todos_los_prompts_reales(funciones, modelo, tamano_vocabulario, prompts):
    """R6.3 contra el universo entero: ningun prompt real hace escapar la excepcion."""
    for texto in prompts:
        face = cara_simulada(funciones, modelo, hacer_logits_que_lanzan(tamano_vocabulario, vuelta=1))
        resultado = face.reply(texto)
        assert resultado.log == LOG_FALLO, texto
        assert isinstance(resultado, Output)
        assert resultado.output == {"prompt": texto}, texto


def test_reply_corta_por_el_tope_de_hoja_con_logits_planos(funciones, modelo, tamano_vocabulario, prompt_mas_largo):
    """R6.4: con logits planos la hoja se desborda y el bucle corta con 'Model entered an loop'."""
    face = cara_simulada(funciones, modelo, hacer_logits_planos(tamano_vocabulario))
    resultado = face.reply(prompt_mas_largo)
    assert resultado.log == LOG_BUCLE
    assert resultado.output == {"prompt": prompt_mas_largo}


def test_reply_corta_por_el_tope_con_el_prompt_real_mas_corto(funciones, modelo, tamano_vocabulario, prompt_mas_corto):
    """R6.4 en su borde mas estrecho: el prompt mas corto del archivo da el tope mas pequeno del universo real."""
    face = cara_simulada(funciones, modelo, hacer_logits_planos(tamano_vocabulario))
    resultado = face.reply(prompt_mas_corto)
    assert resultado.log == LOG_BUCLE, resultado.log


def test_reply_corta_por_el_tope_con_todos_los_prompts_reales(funciones, modelo, tamano_vocabulario, prompts):
    """R6.4 contra el universo entero: con logits planos ningun prompt real se cuelga."""
    for texto in prompts:
        face = cara_simulada(funciones, modelo, hacer_logits_planos(tamano_vocabulario))
        resultado = face.reply(texto)
        assert resultado.log == LOG_BUCLE, (texto, resultado.log)


def test_reply_nunca_escapa_una_excepcion_con_un_str(funciones, modelo, tamano_vocabulario, prompt_mas_largo):
    """R5: con un user_prompt str, salga bien o mal, reply devuelve estado y no lanza."""
    simuladas = (
        hacer_logits_planos(tamano_vocabulario),
        hacer_logits_que_lanzan(tamano_vocabulario, vuelta=1),
        hacer_logits_que_lanzan(tamano_vocabulario, vuelta=3),
    )
    for logits in simuladas:
        face = cara_simulada(funciones, modelo, logits)
        for texto in (prompt_mas_largo, "", "aaaa"):
            resultado = face.reply(texto)
            assert isinstance(resultado, Output)
            assert resultado.log in LOGS_VALIDOS


# ==========================================================================
# 7 - ENTRADAS INVALIDAS (R5 - un test por caso, no es zona de stress)
# ==========================================================================

def test_init_rechaza_una_ruta_que_no_existe(funciones, modelo, tmp_path):
    """R5: una ruta inexistente sale por ValidationError con path_not_file, no por un error de dentro."""
    fantasma = tmp_path / "no_existe.json"
    reales = [
        modelo.get_path_to_vocab_file(),
        modelo.get_path_to_merges_file(),
        modelo.get_path_to_tokenizer_file(),
    ]
    for posicion in range(len(reales)):
        rutas = list(reales)
        rutas[posicion] = fantasma
        with pytest.raises(ValidationError) as fallo:
            Interface(funciones, rutas[0], rutas[1], rutas[2],
                      modelo.get_logits_from_input_ids)
        assert any(e["type"] == "path_not_file" for e in fallo.value.errors())


def test_init_rechaza_functions_que_no_es_lista_de_function(modelo):
    """R5: un dict, un str o un int en lugar de List[Function] salen por ValidationError."""
    for invalido in ({"a": 1}, "fn_greet", 5, None):
        with pytest.raises(ValidationError):
            Interface(
                invalido,
                modelo.get_path_to_vocab_file(),
                modelo.get_path_to_merges_file(),
                modelo.get_path_to_tokenizer_file(),
                modelo.get_logits_from_input_ids,
            )


def test_init_rechaza_un_logits_method_no_invocable(funciones, modelo):
    """R5: un logits_method no invocable sale por ValidationError con callable_type."""
    for invalido in (5, None, "no soy callable", [1, 2]):
        with pytest.raises(ValidationError) as fallo:
            Interface(
                funciones,
                modelo.get_path_to_vocab_file(),
                modelo.get_path_to_merges_file(),
                modelo.get_path_to_tokenizer_file(),
                invalido,
            )
        assert any(e["type"] == "callable_type" for e in fallo.value.errors())


def test_reply_rechaza_un_user_prompt_que_no_es_str(cara):
    """R5: 5, None o una lista en reply salen por ValidationError del @validate_call."""
    for invalido in (5, None, ["Greet shrek"], 3.5, {"prompt": "Greet shrek"}):
        with pytest.raises(ValidationError):
            cara.reply(invalido)


# ==========================================================================
# 8 - ADENDA 5.2: _valid_parameters y _costume_translater, en directo (A4)
#
# Excepcion autorizada por el estudiante a la regla de corte: estos dos
# metodos privados se llaman de forma directa sobre la fixture `cara`,
# porque a traves de reply es estructuralmente imposible llegar a los casos
# 5 y 6 de log (A2). E6 y E7 son elementos de nivel 2 - fabricados, pero
# cubren todas las combinaciones de profundidad y tipo que la clase declara
# aceptar (F3).
# ==========================================================================

@pytest.fixture(scope="session")
def funcion_simple() -> Function:
    """E6 - una Function de un solo parametro number, sin anidar."""
    return Function(
        name="fn_test_simple",
        description="funcion fabricada para probar _valid_parameters sin anidar",
        parameters={"a": TypeSpec(type="number")},
        returns=TypeSpec(type="string"),
    )


@pytest.fixture(scope="session")
def funcion_anidada() -> Function:
    """E7 - una Function con dos niveles de objeto anidado (bonus 7)."""
    return Function(
        name="fn_test_anidada",
        description="funcion fabricada para probar _valid_parameters con dos niveles",
        parameters={
            "user": TypeSpec(type="object", properties={
                "name": TypeSpec(type="string"),
                "address": TypeSpec(type="object", properties={
                    "city": TypeSpec(type="string"),
                    "zip": TypeSpec(type="number"),
                }),
            }),
            "active": TypeSpec(type="string"),
        },
        returns=TypeSpec(type="string"),
    )


ERROR_TIPO = {"ERROR": "processed function doesn't match the function parameters"}


def test_valid_parameters_acepta_un_parametro_simple_correcto(cara, funcion_simple):
    """Caso 1 de A5: un unico parametro number con el tipo correcto pasa sin ERROR."""
    assert cara._valid_parameters(funcion_simple, {"a": 3}) == {"a": 3}


def test_valid_parameters_acepta_los_dos_niveles_de_anidamiento_correctos(cara, funcion_anidada):
    """Caso 3 de A5: user.address.city/zip y active, todos con el tipo correcto, pasan sin tocar el dict."""
    entrada = {
        "user": {"name": "shrek", "address": {"city": "Duloc", "zip": 12345}},
        "active": "yes",
    }
    assert cara._valid_parameters(funcion_anidada, entrada) == entrada


def test_valid_parameters_rechaza_un_tipo_equivocado_sin_anidar(cara, funcion_simple):
    """Caso 2 de A5: 'a' deberia ser number y llega como str."""
    assert cara._valid_parameters(funcion_simple, {"a": "x"}) == ERROR_TIPO


def test_valid_parameters_propaga_el_error_desde_el_nivel_mas_profundo(cara, funcion_anidada):
    """Caso 4 de A5, la invariante central de esta adenda: zip deberia ser number y llega como str
    dentro de user.address, y el error se propaga hasta la raiz en vez de quedar enmascarado."""
    entrada = {
        "user": {"name": "shrek", "address": {"city": "Duloc", "zip": "12345"}},
        "active": "yes",
    }
    assert cara._valid_parameters(funcion_anidada, entrada) == ERROR_TIPO


def test_valid_parameters_rechaza_un_nivel_intermedio_que_no_es_objeto(cara, funcion_anidada):
    """Caso 5 de A5: 'user' deberia ser un objeto y llega como str."""
    entrada = {"user": "no soy un dict", "active": "yes"}
    assert cara._valid_parameters(funcion_anidada, entrada) == ERROR_TIPO


def test_costume_translater_traduce_una_hoja_con_disfraz_real(cara):
    """Caso 6 de A5: una hoja con el disfraz real del vocabulario (Ġ) sale traducida a texto legible."""
    resultado = cara._costume_translater({"source_string": "ProgrammingĠisĠfun"})
    assert resultado == {"source_string": "Programming is fun"}
