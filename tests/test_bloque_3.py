"""Tests del Bloque 3 — `PromptBuilder`.

Ninguno necesita el modelo ni la red: el bloque solo arma una string.
"""
from typing import Any, Dict, List

import pytest
from pydantic import TypeAdapter, ValidationError

from src.filemanager import Function
from src.promptbuilder import PromptBuilder

IM_START = "<|im_start|>"
IM_END = "<|im_end|>"


def catalogo() -> List[Dict[str, Any]]:
    """Catalogo plano, con la misma forma que el real pero mas corto."""
    return [
        {"name": "fn_add_numbers",
         "description": "Add two numbers together and return their sum.",
         "parameters": {"a": {"type": "number"}, "b": {"type": "number"}},
         "returns": {"type": "number"}},
        {"name": "fn_greet",
         "description": "Generate a greeting message for a person by name.",
         "parameters": {"name": {"type": "string"}},
         "returns": {"type": "string"}},
    ]


def funciones(crudo: Any = None) -> List[Function]:
    """Convierte el catalogo crudo en los objetos que entrega el Bloque 2."""
    return TypeAdapter(List[Function]).validate_python(
        catalogo() if crudo is None else crudo)


@pytest.fixture
def builder() -> PromptBuilder:
    """Un `PromptBuilder` ya montado con el catalogo de dos funciones."""
    return PromptBuilder(funciones())


# --------------------------------------------------------------------------
# 1. Creacion correcta
# --------------------------------------------------------------------------

def test_construye_con_una_lista_de_funciones():
    """Con lo que entrega el Bloque 2, el objeto nace sin lanzar."""
    assert isinstance(PromptBuilder(funciones()), PromptBuilder)


def test_construye_con_el_catalogo_vacio():
    """Sin funciones no lanza: ese guard vive en el Bloque 2."""
    assert isinstance(PromptBuilder([]), PromptBuilder)


def test_no_acepta_algo_que_no_sea_una_lista():
    """`@validate_call` corta antes de entrar al cuerpo."""
    with pytest.raises(ValidationError):
        PromptBuilder("fn_add_numbers")


def test_no_acepta_una_lista_de_cualquier_cosa():
    """Una lista de strings no son funciones."""
    with pytest.raises(ValidationError):
        PromptBuilder(["fn_add_numbers"])


# --------------------------------------------------------------------------
# 2. El catalogo dentro del prompt
# --------------------------------------------------------------------------

def test_el_catalogo_entra_como_json(builder):
    """Lo que se mete es el JSON, no el `repr` de los objetos `Function`."""
    texto = builder.get_prompt("Greet shrek")
    assert '{"name":"fn_add_numbers"' in texto
    assert "Function(" not in texto


def test_el_json_no_arrastra_properties_nulos(builder):
    """`exclude_none=True`: los `properties: null` no llegan al modelo."""
    assert "null" not in builder.get_prompt("Greet shrek")


def test_estan_todas_las_funciones_y_en_orden():
    """El catalogo entero, en el orden del archivo."""
    texto = PromptBuilder(funciones()).get_prompt("Greet shrek")
    assert texto.index("fn_add_numbers") < texto.index("fn_greet")


def test_las_descripciones_llegan_al_modelo(builder):
    """Son las que le dicen al modelo cual elegir."""
    assert "Add two numbers together" in builder.get_prompt("Greet shrek")


def test_un_catalogo_anidado_entra_igual():
    """El bonus 7: pasando el JSON tal cual, este bloque no se entera."""
    anidado = [{"name": "fn_move",
                "description": "Move something.",
                "parameters": {"punto": {"type": "object", "properties": {
                    "x": {"type": "number"}}}},
                "returns": {"type": "string"}}]
    texto = PromptBuilder(funciones(anidado)).get_prompt("Move it")
    assert '"properties"' in texto and '"x"' in texto


# --------------------------------------------------------------------------
# 3. La plantilla de chat
# --------------------------------------------------------------------------

def test_el_prompt_abre_con_la_seccion_de_sistema(builder):
    """Salto de linea tras el rol, como la plantilla real de Qwen."""
    assert builder.get_prompt("Greet shrek").startswith(f"{IM_START}system\n")


def test_el_prompt_termina_cediendo_el_turno(builder):
    """Se corta en `assistant`: es la señal de que ahora escribe el modelo."""
    assert builder.get_prompt("Greet shrek").endswith(
        f"{IM_START}assistant\n")


def test_cada_im_end_lleva_su_salto_de_linea(builder):
    """Los dos `<|im_end|>` van seguidos de `\\n`, nunca de un espacio."""
    texto = builder.get_prompt("Greet shrek")
    assert texto.count(IM_END) == 2
    assert texto.count(f"{IM_END}\n") == 2


def test_la_seccion_de_usuario_lleva_el_prompt_tal_cual(builder):
    """La frase del usuario entra sin tocar, entre sus dos marcas."""
    assert f"{IM_START}user\nGreet shrek{IM_END}" in builder.get_prompt(
        "Greet shrek")


def test_el_prompt_dice_que_claves_quiere(builder):
    """Sin nombrarlas, el modelo puede escribir `function`/`arguments`."""
    texto = builder.get_prompt("Greet shrek")
    assert '"name"' in texto and '"parameters"' in texto


# --------------------------------------------------------------------------
# 4. Flujo normal, prompt a prompt
# --------------------------------------------------------------------------

def test_solo_cambia_la_linea_del_usuario(builder):
    """El catalogo se monta una vez: dos prompts comparten toda la cabecera."""
    uno = builder.get_prompt("Greet shrek")
    otro = builder.get_prompt("Greet john")
    corte = uno.index(f"{IM_START}user")
    assert uno[:corte] == otro[:corte]
    assert uno != otro


def test_llamarlo_dos_veces_con_el_mismo_prompt_da_lo_mismo(builder):
    """No arrastra estado entre llamadas."""
    assert builder.get_prompt("Greet shrek") == builder.get_prompt(
        "Greet shrek")


def test_el_prompt_vacio_no_rompe(builder):
    """Un prompt vacio produce la seccion de usuario vacia, no un fallo."""
    assert f"{IM_START}user\n{IM_END}" in builder.get_prompt("")


def test_el_prompt_conserva_acentos_y_comillas(builder):
    """Lo que escribio el usuario llega al modelo tal cual."""
    frase = 'Reverse the string \'hello\' y saluda a José'
    assert frase in builder.get_prompt(frase)


# --------------------------------------------------------------------------
# 5. Limite y stress
# --------------------------------------------------------------------------

def test_un_catalogo_de_cien_funciones(builder):
    """El catalogo del peer review puede ser mucho mayor que el del ejemplo."""
    grande = [{"name": f"fn_{i}",
               "description": f"Funcion numero {i}.",
               "parameters": {"a": {"type": "number"}},
               "returns": {"type": "number"}} for i in range(100)]
    texto = PromptBuilder(funciones(grande)).get_prompt("Greet shrek")
    assert '"fn_99"' in texto


def test_un_prompt_muy_largo(builder):
    """Un prompt de 5.000 caracteres entra entero."""
    largo = "Greet shrek. " * 400
    assert largo in builder.get_prompt(largo)
