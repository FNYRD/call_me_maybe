"""Tests del Bloque 4 — `Guardian`.

Escritos a caja negra contra `block_mockup/bloque_4_guardian_contrato.pdf`:
ninguna afirmacion sale de leer la implementacion.

Los elementos objetivos son reales, no ejemplos escogidos a mano:

  E1  vocabulario  ->  `Tokenizer.get_vocab()` sobre los archivos del modelo
  E2  inverso      ->  `Tokenizer.get_reversed_vocab()`
  E3  catalogo     ->  `FileManager.get_functions()` sobre `data/input/`
  E4  prompts      ->  `FileManager.get_prompts()` sobre `data/input/`
  E5  catalogo ampliado -> E3 mas funciones fabricadas aqui, para los casos
      que el catalogo real no contiene
  E6  valores sueltos forzados a mano, solo para bordes declarados

Las rutas del modelo salen del SDK, no clavadas a mano, para que valgan en
otra maquina.

Pendiente por decision del estudiante (S5), sin testear todavia:
  - `get_valid_ids()` sin hueco abierto
  - `add_token` antes del primer `start`
  - `get_json()` antes del primer `start`
"""
import json
import random
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

import pytest
from pydantic import TypeAdapter, ValidationError

from llm_sdk import Small_LLM_Model

from src.filemanager import FileManager, Function, Prompt
from src.guardian import Guardian
from src.tokenizer import Tokenizer

# --------------------------------------------------------------------------
# Rutas de los artefactos reales del proyecto
# --------------------------------------------------------------------------

RAIZ = Path(__file__).resolve().parent.parent
FUNCIONES = RAIZ / "data" / "input" / "functions_definition.json"
PROMPTS = RAIZ / "data" / "input" / "function_calling_tests.json"

CIERRES = ('"', ',', '}')
DIGITOS = "0123456789"

# Tope de pasos de un recorrido: si se pasa, el recorrido no termina y eso
# es un rojo, no un cuelgue.
TOPE_PASOS = 300

# En una hoja `string` casi todo el vocabulario es admisible: recorrer los
# 150.000 candidatos por paso no cabe en una suite. Cuando la lista pasa de
# `TOPE_EXHAUSTIVO` se toma una muestra determinista de `TAM_MUESTRA`.
# LIMITACION DECLARADA: en esas hojas la pasada no es exhaustiva.
TOPE_EXHAUSTIVO = 20
TAM_MUESTRA = 8


# --------------------------------------------------------------------------
# Elementos objetivos — fixtures de sesion: cargar el modelo es caro
# --------------------------------------------------------------------------

@pytest.fixture(scope="session")
def tokenizer() -> Tokenizer:
    """El `Tokenizer` del Bloque 1 sobre los archivos reales de Qwen."""
    modelo = Small_LLM_Model()
    return Tokenizer(modelo.get_path_to_vocab_file(),
                     modelo.get_path_to_merges_file(),
                     modelo.get_path_to_tokenizer_file())


@pytest.fixture(scope="session")
def vocab(tokenizer) -> Dict[str, int]:
    """E1 — el vocabulario real, texto -> id."""
    return tokenizer.get_vocab()


@pytest.fixture(scope="session")
def reversed_vocab(tokenizer) -> Dict[int, str]:
    """E2 — el vocabulario real en la otra direccion, id -> texto."""
    return tokenizer.get_reversed_vocab()


@pytest.fixture(scope="session")
def manager(tmp_path_factory) -> FileManager:
    """El `FileManager` del Bloque 2 sobre el catalogo y los prompts reales.

    La ruta de salida apunta a un temporal: construirlo no escribe nada.
    """
    salida = tmp_path_factory.mktemp("salida") / "res.json"
    return FileManager(FUNCIONES, PROMPTS, salida)


@pytest.fixture(scope="session")
def functions(manager) -> List[Function]:
    """E3 — el catalogo real, ya validado como `List[Function]`."""
    return manager.get_functions()


@pytest.fixture(scope="session")
def prompts(manager) -> List[Prompt]:
    """E4 — los prompts reales."""
    return manager.get_prompts()


# --------------------------------------------------------------------------
# E5 — catalogo ampliado: lo que el real no contiene
#
# Lista viva de caracteristicas que reproduce:
#   nombre que es prefijo estricto de otro  ->  fn_greet / fn_greeting
#   funcion sin parametros                  ->  fn_nada
#   funcion de un solo parametro            ->  fn_uno
#   anidamiento a dos niveles               ->  fn_move
#   mas de dos parametros y tipos mezclados ->  fn_mixto
# --------------------------------------------------------------------------

def ampliadas() -> List[Dict[str, Any]]:
    """Las funciones fabricadas que se apilan encima del catalogo real."""
    return [
        {"name": "fn_greeting",
         "description": "Longer name that starts with another one.",
         "parameters": {"who": {"type": "string"}},
         "returns": {"type": "string"}},
        {"name": "fn_nada",
         "description": "Takes no parameters at all.",
         "parameters": {},
         "returns": {"type": "string"}},
        {"name": "fn_uno",
         "description": "One single parameter.",
         "parameters": {"n": {"type": "number"}},
         "returns": {"type": "number"}},
        {"name": "fn_move",
         "description": "A parameter that is an object with fields inside.",
         "parameters": {"punto": {"type": "object",
                                  "properties": {"x": {"type": "number"},
                                                 "y": {"type": "number"}}},
                        "b": {"type": "number"}},
         "returns": {"type": "string"}},
        {"name": "fn_mixto",
         "description": "Several parameters of mixed types.",
         "parameters": {"uno": {"type": "number"},
                        "dos": {"type": "string"},
                        "tres": {"type": "number"},
                        "cuatro": {"type": "string"}},
         "returns": {"type": "string"}},
    ]


def como_funciones(brutas: List[Dict[str, Any]]) -> List[Function]:
    """Valida dicts con el mismo modelo que usa el Bloque 2."""
    return TypeAdapter(List[Function]).validate_python(brutas)


@pytest.fixture(scope="session")
def ampliado(functions) -> List[Function]:
    """E5 — el catalogo real mas las funciones fabricadas."""
    return list(functions) + como_funciones(ampliadas())


@pytest.fixture(scope="session")
def una_sola(functions) -> List[Function]:
    """Catalogo de una unica funcion, para el atajo del nombre unico."""
    return [f for f in functions if f.name == "fn_greet"]


# --------------------------------------------------------------------------
# Conductor: el papel que en produccion hace el Bloque 5
#
# El contrato dice que elegir cualquiera de los ids devueltos es igual de
# valido que el `argmax` del modelo, asi que aqui se elige a proposito.
# --------------------------------------------------------------------------

class Conductor:
    """Conduce una sesion de `Guardian` sin mirar por dentro de la clase."""

    def __init__(self, guardian: Guardian, rv: Dict[int, str],
                 prompt: str) -> None:
        self.g = guardian
        self.rv = rv
        self.prompt = prompt
        self.elegidos: List[int] = []
        self.g.start(prompt)

    def txt(self, token_id: int) -> str:
        """El texto que escribe un id."""
        return self.rv[token_id]

    def ids(self) -> List[int]:
        """Los ids admisibles en el hueco actual."""
        return self.g.get_valid_ids()

    def json(self) -> str:
        """El JSON acumulado hasta ahora."""
        return self.g.get_json()

    def pon(self, token_id: int) -> None:
        """Comunica el token elegido y anota la traza para poder repetirla."""
        self.elegidos.append(token_id)
        self.g.add_token(token_id)

    def cierra_uno(self) -> None:
        """Da un paso prefiriendo el token que cierra el hueco cuanto antes."""
        ids = self.ids()
        cierres = [i for i in ids if self.txt(i)[:1] in CIERRES]
        candidatos = cierres or ids
        self.pon(min(candidatos, key=lambda i: (len(self.txt(i)), i)))

    def cierra_todo(self) -> str:
        """Lleva la sesion hasta el final por el camino mas corto."""
        pasos = 0
        while self.g.is_open():
            self.cierra_uno()
            pasos += 1
            assert pasos <= TOPE_PASOS, (
                f"el recorrido no termina tras {TOPE_PASOS} pasos "
                f"con el prompt {self.prompt!r}")
        return self.json()

    def escribe(self, texto: str) -> None:
        """Escribe exactamente `texto` en el hueco actual, token a token.

        Si el atajo del nombre unico completa por su cuenta, el JSON pasa a
        empezar por la meta igualmente y el bucle para.
        """
        meta = self.json() + texto
        pasos = 0
        while not self.json().startswith(meta):
            actual = self.json()
            assert meta.startswith(actual), (
                f"la sesion se ha ido de la meta {meta!r}: {actual!r}")
            falta = meta[len(actual):]
            candidatos = [i for i in self.ids()
                          if falta.startswith(self.txt(i))]
            assert candidatos, (
                f"no hay ningun token admisible para escribir {falta!r}")
            self.pon(max(candidatos, key=lambda i: len(self.txt(i))))
            pasos += 1
            assert pasos <= TOPE_PASOS, f"no se puede escribir {texto!r}"


def nueva(vocab, reversed_vocab, functions, prompt: str) -> Conductor:
    """Un `Guardian` recien creado y arrancado con `prompt`."""
    return Conductor(Guardian(vocab, reversed_vocab, functions),
                     reversed_vocab, prompt)


def repetir(vocab, reversed_vocab, functions, prompt: str,
            traza: List[int]) -> Conductor:
    """Reconstruye una sesion y repite una traza de tokens ya elegida."""
    conductor = nueva(vocab, reversed_vocab, functions, prompt)
    for token_id in traza:
        conductor.pon(token_id)
    return conductor


def id_de(vocab: Dict[str, int], texto: str) -> int:
    """El id del token que escribe exactamente `texto`.

    Que un caracter suelto —`.`, `,`, `}`, `"`— exista como token propio del
    vocabulario es una suposicion sobre el vocabulario real, no algo que el
    contrato prometa: si no esta, el rojo lo dice aqui y no salta un
    `KeyError` a mitad de un assert.
    """
    assert texto in vocab, (
        f"el vocabulario real no trae {texto!r} como token suelto")
    return vocab[texto]


def muestra(ids: List[int]) -> List[int]:
    """Los candidatos a revisar en un paso: todos, o una muestra estable."""
    if len(ids) <= TOPE_EXHAUSTIVO:
        return list(ids)
    return random.Random(0).sample(sorted(ids), TAM_MUESTRA)


def pares(texto: str) -> Any:
    """Parsea conservando el orden de las claves de cada objeto."""
    return json.loads(texto, object_pairs_hook=lambda p: p)


def claves(objeto: Any) -> List[str]:
    """Las claves de un objeto parseado con `pares`, en su orden."""
    return [clave for clave, _ in objeto]


def valor(objeto: Any, clave: str) -> Any:
    """El valor de una clave en un objeto parseado con `pares`."""
    return next(v for k, v in objeto if k == clave)


def esperadas(spec: Any) -> List[str]:
    """Las claves que el schema de un `TypeSpec` promete, en su orden."""
    return list(spec.properties or {})


# --------------------------------------------------------------------------
# 1. `__init__` — creacion correcta, flujo normal, limite, stress, invalidas
# --------------------------------------------------------------------------

def test_construye_con_vocabulario_y_catalogo_reales(
        vocab, reversed_vocab, functions):
    """Lo que producen los Bloques 1 y 2 entra tal cual, y deja la sesion en
    reposo."""
    guardian = Guardian(vocab, reversed_vocab, functions)

    assert isinstance(guardian, Guardian)
    assert guardian.is_open() is False


def test_construye_con_catalogo_de_varias_funciones(
        vocab, reversed_vocab, functions, prompts):
    """El caso normal: catalogo de muchas funciones y sesion que arranca."""
    guardian = Guardian(vocab, reversed_vocab, functions)
    guardian.start(prompts[0].prompt)

    assert len(functions) > 1
    assert guardian.is_open() is True


def test_construye_con_catalogo_de_una_sola_funcion(
        vocab, reversed_vocab, una_sola, prompts):
    """El limite declarado: un catalogo con una unica funcion es valido."""
    guardian = Guardian(vocab, reversed_vocab, una_sola)
    guardian.start(prompts[0].prompt)

    assert len(una_sola) == 1
    assert guardian.is_open() is True


def test_construye_con_el_catalogo_ampliado(
        vocab, reversed_vocab, ampliado, prompts):
    """Stress: vocabulario entero y catalogo con anidamiento, funcion sin
    parametros y nombres con prefijo compartido."""
    guardian = Guardian(vocab, reversed_vocab, ampliado)
    guardian.start(prompts[0].prompt)

    assert len(vocab) > 150000
    assert guardian.is_open() is True


@pytest.mark.parametrize("mal_vocab, mal_reverso, mal_catalogo", [
    ("no soy un dict", {}, []),
    ({}, "no soy un dict", []),
    ({}, {}, "no soy una lista"),
    ({}, {}, ["no soy una Function"]),
    (None, None, None),
])
def test_init_rechaza_argumentos_de_tipo_equivocado(
        mal_vocab, mal_reverso, mal_catalogo):
    """`@validate_call` corta en la puerta lo que no tiene la forma pactada."""
    with pytest.raises(ValidationError):
        Guardian(mal_vocab, mal_reverso, mal_catalogo)


# --------------------------------------------------------------------------
# 2. `start` — flujo normal, limite, stress, invalidas
# --------------------------------------------------------------------------

def test_start_abre_la_sesion_con_los_prompts_reales(
        vocab, reversed_vocab, functions, prompts):
    """`start` enciende la sesion con cualquiera de los prompts reales."""
    guardian = Guardian(vocab, reversed_vocab, functions)

    for entrada in prompts:
        guardian.start(entrada.prompt)
        assert guardian.is_open() is True, entrada.prompt


def test_start_acepta_el_prompt_vacio(vocab, reversed_vocab, functions):
    """El prompt vacio es un caso aceptado: abre sesion como cualquier otro.

    Ningun prompt real esta vacio, asi que este valor se fuerza a mano: es un
    borde declarado por el contrato, no una invariante.
    """
    guardian = Guardian(vocab, reversed_vocab, functions)

    guardian.start("")

    assert guardian.is_open() is True


DUROS = [
    '',
    'dice "hola" con comillas',
    'con {llaves} y "comillas" a la vez',
    'con\nsaltos\r\nde linea',
    'con acentos y emoji: aeiou n cafe 🐸 ✅',
    'con barra invertida \\ y tabulador \t',
    'muy largo ' * 400,
]


@pytest.mark.parametrize("texto", DUROS)
def test_start_acepta_prompts_dificiles(
        vocab, reversed_vocab, functions, texto):
    """Comillas, llaves, saltos, no ASCII y textos largos abren sesion."""
    guardian = Guardian(vocab, reversed_vocab, functions)

    guardian.start(texto)

    assert guardian.is_open() is True


def test_start_repetido_borra_la_sesion_anterior(
        vocab, reversed_vocab, functions, prompts):
    """Invariante 10: nada del prompt anterior sobrevive al `start` nuevo."""
    primero = "SHREK_ANTERIOR pide algo"
    conductor = nueva(vocab, reversed_vocab, functions, primero)
    conductor.cierra_todo()

    conductor.g.start(prompts[0].prompt)
    conductor.elegidos = []

    assert conductor.g.is_open() is True
    assert "SHREK_ANTERIOR" not in conductor.json()
    conductor.cierra_todo()
    assert "SHREK_ANTERIOR" not in conductor.json()


@pytest.mark.parametrize("malo", [123, None, 4.5, ["texto"], {"p": "texto"}])
def test_start_rechaza_lo_que_no_es_texto(
        vocab, reversed_vocab, functions, malo):
    """`start` solo acepta `str`: cualquier otra cosa se corta en la puerta."""
    guardian = Guardian(vocab, reversed_vocab, functions)

    with pytest.raises(ValidationError):
        guardian.start(malo)


# --------------------------------------------------------------------------
# 3. `is_open`
# --------------------------------------------------------------------------

def test_is_open_es_falso_antes_del_primer_start(
        vocab, reversed_vocab, functions):
    """Invariante 9, primera mitad: sin `start` no hay sesion."""
    assert Guardian(vocab, reversed_vocab, functions).is_open() is False


def test_is_open_se_apaga_justo_en_el_token_que_cierra(
        vocab, reversed_vocab, functions, prompts):
    """Sigue en `True` en cada paso y solo pasa a `False` con el ultimo."""
    conductor = nueva(vocab, reversed_vocab, functions, prompts[0].prompt)

    pasos = 0
    while conductor.g.is_open():
        assert conductor.g.is_open() is True
        conductor.cierra_uno()
        pasos += 1
        assert pasos <= TOPE_PASOS

    assert conductor.g.is_open() is False
    assert pasos > 1


def test_is_open_repetido_no_mueve_nada(
        vocab, reversed_vocab, functions, prompts):
    """Preguntar muchas veces no avanza el estado ni cambia la respuesta."""
    conductor = nueva(vocab, reversed_vocab, functions, prompts[0].prompt)
    antes = conductor.json()

    respuestas = [conductor.g.is_open() for _ in range(50)]

    assert respuestas == [True] * 50
    assert conductor.json() == antes


def test_is_open_nunca_lanza_en_ningun_momento(
        vocab, reversed_vocab, functions, prompts):
    """Invariante 13: preguntarlo en cualquier punto del recorrido no
    revienta."""
    conductor = nueva(vocab, reversed_vocab, functions, prompts[0].prompt)

    while conductor.g.is_open():
        assert isinstance(conductor.g.is_open(), bool)
        conductor.cierra_uno()

    assert conductor.g.is_open() is False


# --------------------------------------------------------------------------
# 4. `get_valid_ids`
# --------------------------------------------------------------------------

def test_get_valid_ids_devuelve_ids_mientras_haya_hueco(
        vocab, reversed_vocab, functions, prompts):
    """Invariante 11: con un hueco abierto siempre hay con que continuar."""
    conductor = nueva(vocab, reversed_vocab, functions, prompts[0].prompt)

    while conductor.g.is_open():
        ids = conductor.ids()
        assert isinstance(ids, list)
        assert ids, "lista vacia con el hueco abierto"
        assert all(isinstance(i, int) for i in ids)
        conductor.cierra_uno()


def test_todos_los_ids_ofrecidos_existen_en_el_vocabulario(
        vocab, reversed_vocab, functions, prompts):
    """Invariante 1, contra el vocabulario real entero y los 11 prompts."""
    validos = set(vocab.values())

    for entrada in prompts:
        conductor = nueva(vocab, reversed_vocab, functions, entrada.prompt)
        while conductor.g.is_open():
            ofrecidos = set(conductor.ids())
            assert ofrecidos <= validos, entrada.prompt
            conductor.cierra_uno()


def test_consultar_los_ids_no_altera_el_estado(
        vocab, reversed_vocab, functions, prompts):
    """Invariante 8: dos consultas seguidas dan lo mismo y no abren ni
    cierran."""
    conductor = nueva(vocab, reversed_vocab, functions, prompts[0].prompt)

    while conductor.g.is_open():
        primera = conductor.ids()
        abierto = conductor.g.is_open()
        segunda = conductor.ids()

        assert sorted(primera) == sorted(segunda)
        assert conductor.g.is_open() is abierto
        assert conductor.json() == conductor.json()
        conductor.cierra_uno()


def test_la_comilla_cierra_el_nombre_en_cuanto_esta_completo(
        vocab, reversed_vocab, ampliado):
    """Con `fn_greet` y `fn_greeting` en el catalogo, la comilla entra en
    cuanto lo escrito es un nombre completo, aunque queden candidatos mas
    largos."""
    conductor = nueva(vocab, reversed_vocab, ampliado, "Greet shrek")
    conductor.escribe("fn_greet")

    assert id_de(vocab, '"') in conductor.ids()


def test_el_nombre_no_admite_prefijos_imposibles_ni_comilla_temprana(
        vocab, reversed_vocab, functions):
    """En el hueco del nombre no entra lo que no sea prefijo de algun nombre,
    ni la comilla mientras el nombre este a medias o sin empezar."""
    nombres = [f.name for f in functions]
    conductor = nueva(vocab, reversed_vocab, functions, "Greet shrek")

    # Sin nada escrito la comilla no cierra.
    assert id_de(vocab, '"') not in conductor.ids()

    # Todo lo ofrecido mantiene la posibilidad de completar algun nombre.
    escrito = ""
    for _ in range(3):
        for token_id in conductor.ids():
            texto = escrito + conductor.txt(token_id)
            assert any(n.startswith(texto) or texto.startswith(n + '"')
                       or texto == '"' for n in nombres), texto
        elegido = max((i for i in conductor.ids()
                       if any(n.startswith(escrito + conductor.txt(i))
                              for n in nombres)),
                      key=lambda i: len(conductor.txt(i)))
        escrito += conductor.txt(elegido)
        conductor.pon(elegido)
        # El atajo del nombre unico puede haber completado y cerrado el
        # nombre por su cuenta: a partir de ahi el hueco ya no es el nombre
        # y lo que se ofrece son caracteres de una hoja.
        if '"parameters"' in conductor.json():
            break
        if any(n == escrito for n in nombres):
            break

    # Con el nombre a medias, la comilla sigue fuera.
    conductor = nueva(vocab, reversed_vocab, functions, "Greet shrek")
    conductor.escribe("fn_")
    if not conductor.json().rstrip().endswith('"'):
        assert id_de(vocab, '"') not in conductor.ids()


def hasta_hoja_number(vocab, reversed_vocab, functions) -> Conductor:
    """Deja la sesion justo en la primera hoja `number` de
    `fn_add_numbers`."""
    conductor = nueva(vocab, reversed_vocab, functions,
                      "What is the sum of 40 and 2?")
    conductor.escribe('fn_add_numbers')
    while not conductor.json().rstrip().endswith(':'):
        conductor.cierra_uno()
        assert conductor.g.is_open(), "no se llego a la hoja number"
    return conductor


def test_la_hoja_number_no_admite_cierre_ni_punto_sin_digito(
        vocab, reversed_vocab, functions):
    """Recien abierta una hoja `number`, ni el cierre ni el punto son
    admisibles: hace falta un digito antes."""
    conductor = hasta_hoja_number(vocab, reversed_vocab, functions)
    ofrecidos = set(conductor.ids())

    assert id_de(vocab, ',') not in ofrecidos
    assert id_de(vocab, '}') not in ofrecidos
    assert id_de(vocab, '.') not in ofrecidos
    assert all(conductor.txt(i)[:1] in DIGITOS + "-" for i in ofrecidos)


def test_la_hoja_number_no_admite_falsos_digitos(
        vocab, reversed_vocab, functions):
    """Barrido del vocabulario real: ningun caracter que Python da por digito
    pero JSON no —superindices y digitos de otras escrituras— entra en la
    lista blanca."""
    falsos = {vocab[t] for t in vocab
              if len(t) == 1 and t.isnumeric() and t not in DIGITOS}
    assert falsos, "el vocabulario real deberia traer falsos digitos"

    conductor = hasta_hoja_number(vocab, reversed_vocab, functions)

    assert falsos.isdisjoint(set(conductor.ids()))


def test_la_hoja_number_no_admite_un_segundo_punto(
        vocab, reversed_vocab, functions):
    """Con `40.5` escrito, el punto ya se uso y no vuelve a ser admisible."""
    conductor = hasta_hoja_number(vocab, reversed_vocab, functions)
    conductor.escribe("40.5")

    for token_id in conductor.ids():
        assert '.' not in conductor.txt(token_id), conductor.txt(token_id)


def test_en_la_hoja_number_solo_hay_un_cierre_admisible(
        vocab, reversed_vocab, functions):
    """Invariante 7: con un digito escrito, la coma y la llave nunca son
    admisibles a la vez."""
    conductor = hasta_hoja_number(vocab, reversed_vocab, functions)
    conductor.escribe("40")
    ofrecidos = set(conductor.ids())

    coma, llave = id_de(vocab, ','), id_de(vocab, '}')

    assert not (coma in ofrecidos and llave in ofrecidos)
    assert coma in ofrecidos or llave in ofrecidos


def test_todo_lo_ofrecido_en_una_hoja_number_deja_un_numero_valido(
        vocab, reversed_vocab, functions):
    """Invariante 16, pasada bruta sobre la lista entera de la hoja: cada id
    ofrecido lleva a un JSON que `json.loads` acepta."""
    conductor = hasta_hoja_number(vocab, reversed_vocab, functions)
    traza = list(conductor.elegidos)
    prompt = conductor.prompt

    for token_id in conductor.ids():
        otro = repetir(vocab, reversed_vocab, functions, prompt, traza)
        otro.pon(token_id)
        json.loads(otro.cierra_todo())


def hasta_hoja_string(vocab, reversed_vocab, functions) -> Conductor:
    """Deja la sesion dentro de la hoja `string` de `fn_greet`, con el
    contenido `hello` ya escrito."""
    conductor = nueva(vocab, reversed_vocab, functions, "Greet shrek")
    conductor.escribe('fn_greet')
    while not conductor.json().rstrip().endswith('"'):
        conductor.cierra_uno()
        assert conductor.g.is_open(), "no se llego a la hoja string"
    conductor.escribe("hello")
    return conductor


def test_la_hoja_string_no_admite_barra_invertida(
        vocab, reversed_vocab, functions):
    """Barrido del vocabulario real: ningun token con barra invertida entra
    en una hoja `string`, porque no hay escapado."""
    conductor = hasta_hoja_string(vocab, reversed_vocab, functions)

    for token_id in conductor.ids():
        assert '\\' not in conductor.txt(token_id), conductor.txt(token_id)


def test_la_hoja_string_no_cierra_con_coma_ni_llave(
        vocab, reversed_vocab, functions):
    """Mientras el modelo no escriba su comilla, ni la coma ni la llave
    cierran la hoja: son contenido, no cierre."""
    conductor = hasta_hoja_string(vocab, reversed_vocab, functions)
    antes = conductor.json()

    conductor.pon(id_de(vocab, ','))

    assert conductor.g.is_open() is True
    assert conductor.json().startswith(antes + ',')


def test_tras_la_comilla_la_hoja_string_no_admite_mas_contenido(
        vocab, reversed_vocab, functions):
    """Escrita la comilla, la hoja termino: lo unico admisible es seguir con
    la estructura, no anadir texto."""
    conductor = hasta_hoja_string(vocab, reversed_vocab, functions)
    conductor.escribe('"')

    for token_id in conductor.ids():
        texto = conductor.txt(token_id)
        assert texto[:1] in CIERRES, texto


def test_ningun_id_ofrecido_rompe_el_json(
        vocab, reversed_vocab, functions, prompts):
    """Invariante 2, la mas cara: en cada paso, cualquiera de los ids
    ofrecidos deja un JSON que todavia puede completarse hasta el final.

    Exhaustivo cuando la lista cabe; muestra determinista en las hojas
    `string`, donde el vocabulario admisible pasa de 150.000 candidatos.
    """
    prompt = prompts[0].prompt
    conductor = nueva(vocab, reversed_vocab, functions, prompt)

    while conductor.g.is_open():
        traza = list(conductor.elegidos)
        for token_id in muestra(conductor.ids()):
            otro = repetir(vocab, reversed_vocab, functions, prompt, traza)
            otro.pon(token_id)
            json.loads(otro.cierra_todo())
        conductor.cierra_uno()


# --------------------------------------------------------------------------
# 5. `add_token`
# --------------------------------------------------------------------------

def test_add_token_avanza_el_estado(
        vocab, reversed_vocab, functions, prompts):
    """Incorporar un token elegido mueve la sesion: el JSON crece."""
    conductor = nueva(vocab, reversed_vocab, functions, prompts[0].prompt)
    antes = conductor.json()

    conductor.cierra_uno()

    assert len(conductor.json()) > len(antes)
    assert conductor.json().startswith(antes)


def test_el_ultimo_token_cierra_la_sesion(
        vocab, reversed_vocab, functions, prompts):
    """El token que cierra la raiz apaga `is_open` y deja el JSON terminado."""
    conductor = nueva(vocab, reversed_vocab, functions, prompts[0].prompt)

    resultado = conductor.cierra_todo()

    assert conductor.g.is_open() is False
    assert json.loads(resultado)


@pytest.mark.parametrize("malo", ["abc", 4.5, None, [1]])
def test_add_token_rechaza_lo_que_no_es_un_entero(
        vocab, reversed_vocab, functions, prompts, malo):
    """`add_token` corta en la puerta lo que no es un id de token.

    Fuera quedan `"40"` y `True`: `@validate_call` los convierte a `40` y a
    `1` en vez de rechazarlos, asi que exigirle que lancen seria pedirle al
    contrato algo que no promete."""
    conductor = nueva(vocab, reversed_vocab, functions, prompts[0].prompt)

    with pytest.raises(ValidationError):
        conductor.g.add_token(malo)


# --------------------------------------------------------------------------
# 6. `get_json` y la forma del resultado
# --------------------------------------------------------------------------

def test_get_json_a_medias_no_lanza(
        vocab, reversed_vocab, functions, prompts):
    """Con la sesion abierta devuelve el JSON incompleto para inspeccionar."""
    conductor = nueva(vocab, reversed_vocab, functions, prompts[0].prompt)

    parcial = conductor.json()

    assert isinstance(parcial, str)
    assert conductor.g.is_open() is True


def test_el_resultado_tiene_exactamente_las_tres_claves(
        vocab, reversed_vocab, functions, prompts):
    """Invariante 3: cerrado, el JSON parsea y trae `prompt`, `name` y
    `parameters`, ni una mas ni una menos."""
    for entrada in prompts:
        conductor = nueva(vocab, reversed_vocab, functions, entrada.prompt)
        resultado = pares(conductor.cierra_todo())

        assert claves(resultado) == ["prompt", "name", "parameters"]


def test_el_nombre_del_resultado_es_uno_del_catalogo(
        vocab, reversed_vocab, functions, prompts):
    """Invariante 4: el nombre sale tal cual del catalogo, sin inventarse."""
    nombres = {f.name for f in functions}

    for entrada in prompts:
        conductor = nueva(vocab, reversed_vocab, functions, entrada.prompt)
        resultado = pares(conductor.cierra_todo())

        assert valor(resultado, "name") in nombres


def test_el_prompt_del_resultado_es_identico_al_recibido(
        vocab, reversed_vocab, functions, prompts):
    """Invariante 6, tambien con prompts que traen comillas, llaves y saltos:
    el texto vuelve intacto."""
    textos = [p.prompt for p in prompts] + DUROS[:6]

    for texto in textos:
        conductor = nueva(vocab, reversed_vocab, functions, texto)
        resultado = pares(conductor.cierra_todo())

        assert valor(resultado, "prompt") == texto


def test_los_parametros_son_los_del_schema_en_su_orden(
        vocab, reversed_vocab, ampliado, prompts):
    """Invariante 5: a cualquier profundidad, las claves de `parameters` son
    las del schema de esa funcion, ni una de mas ni una de menos, en orden."""
    por_nombre = {f.name: f for f in ampliado}

    for entrada in prompts:
        conductor = nueva(vocab, reversed_vocab, ampliado, entrada.prompt)
        resultado = pares(conductor.cierra_todo())
        funcion = por_nombre[valor(resultado, "name")]
        comprobar_nivel(valor(resultado, "parameters"), funcion.parameters)


def comprobar_nivel(objeto: Any, spec: Dict[str, Any]) -> None:
    """Compara un nivel del resultado con su trozo de schema, y baja."""
    assert claves(objeto) == list(spec), (claves(objeto), list(spec))
    for clave, tipo in spec.items():
        if tipo.properties:
            comprobar_nivel(valor(objeto, clave), tipo.properties)


def test_el_anidamiento_de_dos_niveles_se_completa(
        vocab, reversed_vocab, ampliado):
    """Un parametro que es un objeto con campos dentro se escribe entero y el
    JSON cierra igual que uno plano."""
    conductor = nueva(vocab, reversed_vocab, ampliado, "Move the point")
    conductor.escribe('fn_move')
    resultado = pares(conductor.cierra_todo())

    assert valor(resultado, "name") == "fn_move"
    assert claves(valor(resultado, "parameters")) == ["punto", "b"]
    assert claves(valor(valor(resultado, "parameters"), "punto")) == ["x", "y"]


def test_la_funcion_sin_parametros_deja_un_objeto_vacio(
        vocab, reversed_vocab, ampliado):
    """Una funcion sin parametros no pide nada al modelo: `parameters` sale
    vacio y el JSON queda completo."""
    conductor = nueva(vocab, reversed_vocab, ampliado, "Do nothing")
    conductor.escribe('fn_nada')
    resultado = pares(conductor.cierra_todo())

    assert valor(resultado, "name") == "fn_nada"
    assert valor(resultado, "parameters") == []


def test_todos_los_prompts_reales_terminan_en_un_json_valido(
        vocab, reversed_vocab, functions, prompts):
    """Stress del ciclo entero: los 11 prompts reales, con recorridos
    aleatorios legales, siempre acaban en un JSON parseable."""
    for semilla, entrada in enumerate(prompts):
        azar = random.Random(semilla)
        conductor = nueva(vocab, reversed_vocab, functions, entrada.prompt)

        pasos = 0
        while conductor.g.is_open():
            ids = conductor.ids()
            cierres = [i for i in ids if conductor.txt(i)[:1] in CIERRES]
            abiertos = [i for i in ids if i not in cierres]
            if pasos < 4 and abiertos and azar.random() < 0.5:
                conductor.pon(azar.choice(abiertos))
            else:
                conductor.cierra_uno()
            pasos += 1
            assert pasos <= TOPE_PASOS, entrada.prompt

        resultado = pares(conductor.cierra_todo())
        assert claves(resultado) == ["prompt", "name", "parameters"]


# --------------------------------------------------------------------------
# 7. Atajo del nombre unico
# --------------------------------------------------------------------------

def test_el_nombre_no_se_completa_sin_un_caracter_del_modelo(
        vocab, reversed_vocab, una_sola):
    """Invariante 15: con catalogo de una sola funcion, el nombre sigue sin
    escribirse hasta que el modelo pone su primer caracter."""
    conductor = nueva(vocab, reversed_vocab, una_sola, "Greet shrek")

    assert "fn_greet" not in conductor.json()
    assert id_de(vocab, '"') not in conductor.ids()


def test_con_un_solo_candidato_el_nombre_se_completa_y_cierra(
        vocab, reversed_vocab, una_sola):
    """Invariante 14: escrito el primer caracter, el nombre entero y su
    comilla aparecen sin pedir mas tokens."""
    conductor = nueva(vocab, reversed_vocab, una_sola, "Greet shrek")
    primero = min((i for i in conductor.ids()
                   if "fn_greet".startswith(conductor.txt(i))),
                  key=lambda i: len(conductor.txt(i)))

    conductor.pon(primero)

    assert '"fn_greet"' in conductor.json()


def test_el_atajo_tambien_salta_cuando_el_catalogo_se_reduce_a_uno(
        vocab, reversed_vocab, ampliado):
    """Con `fn_greet` y `fn_greeting` en juego, en cuanto lo escrito solo deja
    un candidato el nombre se completa entero y cerrado."""
    conductor = nueva(vocab, reversed_vocab, ampliado, "Greet shrek")
    conductor.escribe("fn_greeti")

    assert '"fn_greeting"' in conductor.json()


# --------------------------------------------------------------------------
# 8. Invariante 13 sobre el recorrido completo
# --------------------------------------------------------------------------

def test_ninguna_llamada_lanza_con_entradas_validas(
        vocab, reversed_vocab, ampliado, prompts):
    """Invariante 13: catalogo ampliado y prompts reales, ciclo entero, sin
    una sola excepcion."""
    for entrada in prompts:
        conductor = nueva(vocab, reversed_vocab, ampliado, entrada.prompt)
        while conductor.g.is_open():
            conductor.ids()
            conductor.json()
            conductor.cierra_uno()
        json.loads(conductor.json())


# --------------------------------------------------------------------------
# 9. Llamadas fuera de orden - decision del estudiante, 2026-08-31
# --------------------------------------------------------------------------

def test_pedir_ids_sin_sesion_abierta_lanza(
        vocab, reversed_vocab, functions, prompts):
    """Sin sesion abierta no se pueden pedir ids validos: ni antes del primer
    `start` ni despues de que el JSON haya cerrado."""
    g = Guardian(vocab, reversed_vocab, functions)
    with pytest.raises(ValueError):
        g.get_valid_ids()

    conductor = nueva(vocab, reversed_vocab, functions, prompts[0].prompt)
    while conductor.g.is_open():
        conductor.cierra_uno()
    with pytest.raises(ValueError):
        conductor.g.get_valid_ids()


def test_comunicar_un_token_sin_sesion_abierta_lanza(
        vocab, reversed_vocab, functions, prompts):
    """Sin sesion abierta, comunicar un token lanza en vez de escribirlo:
    antes se colaba en un `_json_str` que nadie habia arrancado."""
    g = Guardian(vocab, reversed_vocab, functions)
    with pytest.raises(ValueError):
        g.add_token(id_de(vocab, "fn"))

    conductor = nueva(vocab, reversed_vocab, functions, prompts[0].prompt)
    while conductor.g.is_open():
        conductor.cierra_uno()
    with pytest.raises(ValueError):
        conductor.g.add_token(id_de(vocab, "fn"))


def test_pedir_el_json_sin_haber_arrancado_no_lanza(
        vocab, reversed_vocab, functions):
    """`get_json` nunca lanza: es como se lee el resultado cuando la sesion
    ya cerro, asi que antes del primer `start` devuelve la cadena vacia."""
    g = Guardian(vocab, reversed_vocab, functions)

    assert g.get_json() == ""


def test_la_lista_entera_de_una_hoja_string_es_admisible(
        vocab, reversed_vocab, functions):
    """En una hoja `string`, TODOS los ids ofrecidos —no una muestra— dejan
    un JSON que todavia se puede terminar.

    Cierra el agujero declarado del muestreo: los tests de recorrido miran
    unos pocos candidatos por paso, y en una hoja de texto la lista ronda
    los 150.000. Aqui se congela un estado y se recorre la lista completa.
    """
    conductor = nueva(vocab, reversed_vocab, functions,
                      "Reverse the string 'hello'")
    conductor.escribe("fn_reverse_string")
    while not conductor.json().endswith('"'):
        conductor.cierra_uno()
        assert conductor.g.is_open(), "no se llego a la hoja string"
    conductor.escribe("hel")

    congelado = conductor.json()
    ofrecidos = conductor.ids()
    assert len(ofrecidos) > TOPE_EXHAUSTIVO, (
        "este test existe para una lista grande; con una pequena ya la "
        "cubren los tests de recorrido")

    # Colas minimas que completarian el JSON segun donde deje el token:
    # dentro del texto, justo tras la comilla, o con la llave ya escrita.
    colas = ('"}}', '}}', '}', '')
    for token_id in ofrecidos:
        candidato = congelado + conductor.txt(token_id)
        completable = False
        for cola in colas:
            try:
                resultado = json.loads(candidato + cola)
            except (json.JSONDecodeError, ValueError):
                continue
            if (set(resultado) == {"prompt", "name", "parameters"}
                    and resultado["name"] == "fn_reverse_string"
                    and str(resultado["parameters"]["s"]).startswith("hel")):
                completable = True
                break
        assert completable, (
            f"el id {token_id} ofrece {conductor.txt(token_id)!r} y deja un "
            f"JSON que no se puede terminar: {candidato!r}")


# --------------------------------------------------------------------------
# 10. Estabilidad de la lista blanca — la lista depende solo del estado
#
# Todo lo de esta seccion mira una sola cosa: `get_valid_ids()` responde al
# estado actual y nunca a la historia previa de la instancia. Los catalogos
# fabricados aqui son los que el real no trae: nombres que no comparten
# prefijo, y dos parametros del mismo tipo.
# --------------------------------------------------------------------------

def divergentes() -> List[Function]:
    """Catalogo de tres nombres: dos que no comparten ni la primera letra, y
    un tercero que comparte arranque con el primero.

    El tercero existe para que el recorrido del nombre de varios pasos antes
    de quedarse con un unico candidato: con solo dos nombres ajenos, la
    primera letra ya decide y el atajo del nombre unico cierra el hueco.
    """
    return como_funciones([
        {"name": "get_weather",
         "description": "Weather for a city.",
         "parameters": {"city": {"type": "string"}},
         "returns": {"type": "string"}},
        {"name": "send_mail",
         "description": "Send a mail to someone.",
         "parameters": {"to": {"type": "string"}},
         "returns": {"type": "string"}},
        {"name": "get_time",
         "description": "Shares its start with the first name.",
         "parameters": {"zone": {"type": "string"}},
         "returns": {"type": "string"}},
    ])


def dos_parametros() -> List[Function]:
    """Catalogo con una funcion de dos parametros del mismo tipo.

    Lleva una segunda funcion solo para que el nombre no se complete solo:
    con un unico nombre el atajo salta antes del primer token.
    """
    return como_funciones([
        {"name": "fn_dos",
         "description": "Two parameters of the same type.",
         "parameters": {"a": {"type": "number"}, "b": {"type": "number"}},
         "returns": {"type": "number"}},
        {"name": "zz_otra",
         "description": "Only here to keep two names alive.",
         "parameters": {"q": {"type": "string"}},
         "returns": {"type": "string"}},
    ])


def continuaciones(nombres: List[str], escrito: str,
                   vocab: Dict[str, int]) -> Set[int]:
    """Los ids que el hueco del nombre admite, calculados desde el catalogo.

    Un token vale si su texto, pegado a lo ya escrito, sigue siendo prefijo
    de algun nombre del catalogo o de ese nombre ya cerrado con comilla.
    """
    metas = [nombre + '"' for nombre in nombres]
    return {token_id for texto, token_id in vocab.items()
            if any(meta.startswith(escrito + texto) for meta in metas)}


def recorrido(conductor: Conductor) -> Tuple[List[List[int]], str]:
    """Las listas paso a paso de una sesion, y su JSON final."""
    listas: List[List[int]] = []
    while conductor.g.is_open():
        listas.append(conductor.ids())
        conductor.cierra_uno()
    return listas, conductor.json()


def hasta_number(conductor: Conductor) -> Conductor:
    """Avanza hasta que el hueco actual sea una hoja `number` sin escribir."""
    pasos = 0
    while not conductor.json().rstrip().endswith(':'):
        conductor.cierra_uno()
        pasos += 1
        assert conductor.g.is_open(), "no se llego a la hoja number"
        assert pasos <= TOPE_PASOS, "no se llego a la hoja number"
    return conductor


def hasta_string_vacia(vocab, reversed_vocab, functions) -> Conductor:
    """Deja la sesion en una hoja `string` recien abierta, sin contenido."""
    conductor = nueva(vocab, reversed_vocab, functions, "Greet shrek")
    conductor.escribe('fn_greet')
    while not conductor.json().rstrip().endswith('"'):
        conductor.cierra_uno()
        assert conductor.g.is_open(), "no se llego a la hoja string"
    return conductor


def test_dos_consultas_seguidas_devuelven_la_misma_lista(
        vocab, reversed_vocab, functions, prompts):
    """Caso 1: sin `add_token` en medio, la lista repite contenido Y orden,
    en todos los huecos de una sesion entera."""
    conductor = nueva(vocab, reversed_vocab, functions, prompts[0].prompt)

    while conductor.g.is_open():
        assert conductor.ids() == conductor.ids(), conductor.json()
        conductor.cierra_uno()


def test_dos_prompts_distintos_arrancan_con_la_misma_lista(
        vocab, reversed_vocab, functions):
    """Caso 2: el hueco del nombre no depende del texto del prompt, asi que
    dos sesiones distintas arrancan con listas identicas."""
    uno = nueva(vocab, reversed_vocab, functions, "Greet shrek")
    otro = nueva(vocab, reversed_vocab, functions,
                 "What is the sum of 40 and 2?")

    assert uno.ids() == otro.ids()


def test_una_instancia_reutilizada_da_lo_mismo_que_una_por_prompt(
        vocab, reversed_vocab, functions, prompts):
    """Caso 3, el central: N prompts sobre una sola instancia dan, paso a
    paso, las mismas listas y los mismos JSON que una instancia por prompt.

    Recorre tres prompts reales enteros dos veces: puede tardar.
    """
    textos = [entrada.prompt for entrada in prompts[:3]]
    guardian = Guardian(vocab, reversed_vocab, functions)

    seguidas = [recorrido(Conductor(guardian, reversed_vocab, texto))
                for texto in textos]

    for texto, esperado in zip(textos, seguidas):
        aparte = recorrido(nueva(vocab, reversed_vocab, functions, texto))
        assert aparte == esperado, texto


def test_start_nuevo_arranca_desde_cero_y_no_desde_lo_abandonado(
        vocab, reversed_vocab, functions):
    """Caso 4: `start` a mitad de una sesion tira el estado anterior; la
    primera lista es la del arranque, no la del hueco abandonado."""
    conductor = nueva(vocab, reversed_vocab, functions, "Greet shrek")
    for _ in range(3):
        conductor.cierra_uno()
    abandonada = conductor.ids()

    segunda = Conductor(conductor.g, reversed_vocab, "Reverse 'hello'")
    fresca = nueva(vocab, reversed_vocab, functions, "Reverse 'hello'")

    assert segunda.ids() == fresca.ids()
    assert segunda.ids() != abandonada


def test_dos_catalogos_distintos_no_comparten_lista(
        vocab, reversed_vocab, functions):
    """Caso 5: en el mismo estado —arranque, nada escrito— dos instancias con
    catalogos distintos ofrecen listas distintas, sin herencia entre ellas."""
    otro_catalogo = divergentes()
    uno = nueva(vocab, reversed_vocab, functions, "Greet shrek")
    otro = nueva(vocab, reversed_vocab, otro_catalogo, "Greet shrek")

    assert set(uno.ids()) != set(otro.ids())
    assert set(otro.ids()) == continuaciones(
        [f.name for f in otro_catalogo], "", vocab)


def test_una_hoja_number_y_una_string_vacias_ofrecen_listas_distintas(
        vocab, reversed_vocab, functions):
    """Caso 6: el tipo del hueco manda. Dos hojas recien abiertas, una
    `number` y una `string`, no ofrecen lo mismo."""
    numero = hasta_hoja_number(vocab, reversed_vocab, functions)
    texto = hasta_string_vacia(vocab, reversed_vocab, functions)

    assert set(numero.ids()) != set(texto.ids())


def test_lo_ya_escrito_en_la_hoja_cambia_la_lista(
        vocab, reversed_vocab, functions):
    """Caso 7: misma hoja `number`, distinto contenido escrito. Sin nada, ni
    el punto ni el cierre entran; con un digito, los dos aparecen."""
    vacia = hasta_hoja_number(vocab, reversed_vocab, functions)
    sin_nada = set(vacia.ids())

    vacia.escribe("4")
    con_digito = set(vacia.ids())

    assert id_de(vocab, '.') not in sin_nada
    assert id_de(vocab, '.') in con_digito
    assert not {id_de(vocab, ','), id_de(vocab, '}')} & sin_nada
    assert {id_de(vocab, ','), id_de(vocab, '}')} & con_digito
    assert sin_nada != con_digito


def test_el_cierre_admisible_depende_de_si_quedan_parametros(
        vocab, reversed_vocab):
    """Caso 8: dos hojas `number` con el mismo contenido escrito difieren en
    el cierre: coma en el parametro que no es el ultimo, llave en el ultimo.
    """
    catalogo = dos_parametros()
    conductor = nueva(vocab, reversed_vocab, catalogo, "Add 4 and 4")
    conductor.escribe("fn_dos")

    hasta_number(conductor)
    conductor.escribe("4")
    primera = set(conductor.ids())

    hasta_number(conductor)
    conductor.escribe("4")
    ultima = set(conductor.ids())

    assert id_de(vocab, ',') in primera and id_de(vocab, '}') not in primera
    assert id_de(vocab, '}') in ultima and id_de(vocab, ',') not in ultima
    assert primera != ultima


def test_un_cero_solo_no_admite_ningun_digito_detras(
        vocab, reversed_vocab, functions):
    """Caso 9: escrito un `0` en una hoja `number`, JSON no deja mas digitos
    a la izquierda del punto, asi que ninguno entra."""
    conductor = hasta_hoja_number(vocab, reversed_vocab, functions)
    conductor.escribe("0")

    for token_id in conductor.ids():
        texto = conductor.txt(token_id)
        assert texto[:1] not in DIGITOS, texto


def test_el_punto_no_vuelve_a_entrar_en_la_misma_hoja(
        vocab, reversed_vocab, functions):
    """Caso 10: escrito `0.`, el punto ya se gasto y desaparece de la lista.
    """
    conductor = hasta_hoja_number(vocab, reversed_vocab, functions)
    conductor.escribe("0.")

    for token_id in conductor.ids():
        texto = conductor.txt(token_id)
        assert '.' not in texto, texto


def test_la_lista_nunca_esta_vacia_con_la_sesion_abierta(
        vocab, reversed_vocab, ampliado, prompts):
    """Caso 11: mientras `is_open()` sea verdadero hay al menos un id, en
    todo el recorrido y con el catalogo ampliado."""
    conductor = nueva(vocab, reversed_vocab, ampliado, prompts[0].prompt)

    while conductor.g.is_open():
        assert conductor.ids(), conductor.json()
        conductor.cierra_uno()


def test_la_lista_del_nombre_es_todo_el_universo_admisible(
        vocab, reversed_vocab):
    """Caso 12: estado congelado —arranque, nada escrito— y pasada por TODO
    el vocabulario: la lista es exactamente el conjunto de tokens que
    continuan algun nombre del catalogo. Ni uno de mas, ni uno de menos.

    Recorre los 150.000 tokens del vocabulario real: puede tardar.
    """
    catalogo = divergentes()
    nombres = [f.name for f in catalogo]
    conductor = nueva(vocab, reversed_vocab, catalogo, "Weather in Madrid")

    assert set(conductor.ids()) == continuaciones(nombres, "", vocab)


def test_dos_nombres_sin_prefijo_comun_en_la_misma_instancia(
        vocab, reversed_vocab):
    """Caso 13: sobre UNA instancia se recorre cada nombre del catalogo, uno
    por sesion, con `start` nuevo entre medias.

    En cada paso la lista es exactamente la que se calcula desde el catalogo
    y lo escrito, asi que el camino de un nombre no hereda nada del anterior.
    El recorrido para en cuanto el atajo del nombre unico cierra el hueco:
    con `get_weather` y `get_time` vivos, eso ocurre pasada la letra que los
    separa, no en la primera.
    """
    catalogo = divergentes()
    nombres = [f.name for f in catalogo]
    guardian = Guardian(vocab, reversed_vocab, catalogo)

    for nombre in nombres:
        conductor = Conductor(guardian, reversed_vocab, "Do something")
        escrito = ""
        for letra in nombre:
            assert set(conductor.ids()) == continuaciones(
                nombres, escrito, vocab), (nombre, escrito)
            conductor.escribe(letra)
            escrito += letra
            # El atajo del nombre unico puede cerrar el nombre solo: a partir
            # de ahi el hueco ya no es el nombre.
            if '"parameters"' in conductor.json():
                break


def test_dos_nombres_que_divergen_tarde_se_separan_en_su_punto(
        vocab, reversed_vocab, ampliado):
    """Caso 14: `fn_greet` y `fn_greeting` comparten arranque. Paso a paso la
    lista es la de las continuaciones vivas, y la comilla de cierre solo
    aparece cuando lo escrito ES un nombre completo del catalogo."""
    nombres = [f.name for f in ampliado]
    conductor = nueva(vocab, reversed_vocab, ampliado, "Greet shrek")

    escrito = ""
    for letra in "fn_greet":
        assert set(conductor.ids()) == continuaciones(
            nombres, escrito, vocab), escrito
        cierra = id_de(vocab, '"') in conductor.ids()
        assert cierra is (escrito in nombres), escrito
        conductor.escribe(letra)
        escrito += letra

    assert escrito == "fn_greet" and escrito in nombres
    assert set(conductor.ids()) == continuaciones(nombres, escrito, vocab)
    assert id_de(vocab, '"') in conductor.ids()


def test_los_guardas_de_orden_y_de_id_desconocido(
        vocab, reversed_vocab, functions, prompts):
    """Caso 15: `get_valid_ids` y `add_token` antes de `start` lanzan
    `ValueError`; un id fuera del vocabulario tambien; `get_json` no lanza
    nunca.

    Solo se comprueba que `get_json` no lance: el contrato no dice que
    devuelva antes del primer `start`. Que sea la cadena vacia es una
    suposicion pendiente de confirmar, y se comprueba en la seccion 9.
    """
    guardian = Guardian(vocab, reversed_vocab, functions)

    with pytest.raises(ValueError):
        guardian.get_valid_ids()
    with pytest.raises(ValueError):
        guardian.add_token(id_de(vocab, "fn"))
    guardian.get_json()

    conductor = nueva(vocab, reversed_vocab, functions, prompts[0].prompt)
    fuera = max(reversed_vocab) + 1000
    with pytest.raises(ValueError):
        conductor.g.add_token(fuera)
    conductor.json()


def test_al_cerrar_la_sesion_el_json_esta_completo(
        vocab, reversed_vocab, functions, prompts):
    """Caso 16: terminado un prompt, `is_open()` es `False` y el JSON pasa
    `json.loads` sin error."""
    conductor = nueva(vocab, reversed_vocab, functions, prompts[0].prompt)

    salida = conductor.cierra_todo()

    assert conductor.g.is_open() is False
    assert json.loads(salida)
