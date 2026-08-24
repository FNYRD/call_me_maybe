"""Tests del Bloque 1 — `Tokenizer`.

Todo corre con archivos de juguete (`vocab.json`, `merges.txt`, `tokenizer.json`)
creados en un directorio temporal: ningun test necesita el modelo ni la red.

El unico que si lo necesita es el de comparacion con el SDK, al final, que se
salta solo si el modelo no esta descargado.
"""
import json
from typing import Dict, List, Tuple

import pytest
from pydantic import ValidationError

from src.tokenizer import Tokenizer

# Patron de pre-tokenizacion real de Qwen, copiado del tokenizer.json.
PATRON_QWEN = (
    r"(?i:'s|'t|'re|'ve|'m|'ll|'d)|[^\r\n\p{L}\p{N}]?\p{L}+|\p{N}|"
    r" ?[^\s\p{L}\p{N}]+[\r\n]*|\s*[\r\n]+|\s+(?!\S)|\s+"
)

IM_START = "<|im_start|>"
IM_END = "<|im_end|>"
ENDOFTEXT = "<|endoftext|>"


# --------------------------------------------------------------------------
# Oraculo independiente de la tabla byte -> caracter
# --------------------------------------------------------------------------

def tabla_bytes_esperada() -> Dict[int, str]:
    """Construye la tabla byte -> caracter sin mirar la implementacion.

    Es la tabla estandar de BPE byte-level: los bytes imprimibles se
    representan a si mismos y el resto se desplazan a partir de 256, en orden.
    """
    visibles: List[int] = (list(range(33, 127))
                           + list(range(161, 173))
                           + list(range(174, 256)))
    tabla: Dict[int, str] = {byte: chr(byte) for byte in visibles}
    siguiente: int = 256
    for byte in range(256):
        if byte not in tabla:
            tabla[byte] = chr(siguiente)
            siguiente += 1
    return tabla


TABLA = tabla_bytes_esperada()


def disfraz(texto: str) -> str:
    """Pasa un texto a su forma disfrazada, como la escribe `vocab.json`."""
    return "".join(TABLA[byte] for byte in texto.encode("utf-8"))


# --------------------------------------------------------------------------
# Fabricas de archivos de juguete
# --------------------------------------------------------------------------

def escribir_vocab(ruta, extra: Dict[str, int] = None) -> str:
    """Vocabulario con los 256 caracteres disfrazados + los tokens de `extra`."""
    vocab: Dict[str, int] = {TABLA[byte]: byte for byte in range(256)}
    if extra:
        vocab.update(extra)
    archivo = ruta / "vocab.json"
    archivo.write_text(json.dumps(vocab), encoding="utf-8")
    return str(archivo)


def escribir_merges(ruta, reglas: List[Tuple[str, str]] = None) -> str:
    """`merges.txt` con cabecera; el orden de las reglas es su prioridad."""
    lineas: List[str] = ["#version: 0.2"]
    for izquierda, derecha in (reglas or [("Ġ", "a")]):
        lineas.append(f"{izquierda} {derecha}")
    archivo = ruta / "merges.txt"
    archivo.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    return str(archivo)


def escribir_tokenizer(ruta, patron: str = PATRON_QWEN) -> str:
    """`tokenizer.json` con lo unico que la clase le pide: especiales y patron."""
    contenido = {
        "added_tokens": [
            {"content": ENDOFTEXT, "id": 151643},
            {"content": IM_START, "id": 151644},
            {"content": IM_END, "id": 151645},
            {"content": "<|object_ref_start|>", "id": 151646},
        ],
        "pre_tokenizer": {
            "pretokenizers": [{"pattern": {"Regex": patron}}]
        },
    }
    archivo = ruta / "tokenizer.json"
    archivo.write_text(json.dumps(contenido), encoding="utf-8")
    return str(archivo)


@pytest.fixture
def rutas(tmp_path):
    """Las tres rutas de un tokenizer de juguete valido."""
    return (escribir_vocab(tmp_path),
            escribir_merges(tmp_path),
            escribir_tokenizer(tmp_path))


def construir(tmp_path, extra_vocab=None, reglas=None) -> Tokenizer:
    """Atajo: un `Tokenizer` con el vocabulario y las reglas que pida el test."""
    return Tokenizer(escribir_vocab(tmp_path, extra_vocab),
                     escribir_merges(tmp_path, reglas),
                     escribir_tokenizer(tmp_path))


# --------------------------------------------------------------------------
# 1. Creacion correcta
# --------------------------------------------------------------------------

def test_construye_con_los_tres_archivos(rutas):
    """El caso normal: los tres archivos existen y son validos."""
    tokenizer = Tokenizer(*rutas)
    assert isinstance(tokenizer, Tokenizer)


def test_get_vocab_devuelve_el_diccionario(rutas):
    """`get_vocab` entrega el dict que consumira el Bloque 4, sin `Optional`."""
    vocab = Tokenizer(*rutas).get_vocab()
    assert isinstance(vocab, dict)
    assert vocab["A"] == 65
    assert len(vocab) == 256


def test_los_especiales_se_cargan_del_tokenizer_json(rutas):
    """Los ids de los especiales salen de `added_tokens`, no de `vocab.json`."""
    tokenizer = Tokenizer(*rutas)
    assert tokenizer._special_ids[IM_START] == 151644
    assert IM_START not in tokenizer.get_vocab()


def test_get_special_id_con_token_desconocido(rutas):
    """Un texto que no es especial devuelve 0, que nunca es un id especial."""
    tokenizer = Tokenizer(*rutas)
    assert tokenizer.get_special_id(IM_END) == 151645
    assert tokenizer.get_special_id("Greet") == 0


# --------------------------------------------------------------------------
# 2. Tabla byte <-> caracter
# --------------------------------------------------------------------------

def test_tabla_de_bytes_contra_oraculo(rutas):
    """Los 256 disfraces coinciden con la tabla estandar, calculada aparte."""
    tokenizer = Tokenizer(*rutas)
    assert tokenizer._byte_char == TABLA


def test_tabla_de_bytes_es_biyectiva(rutas):
    """Ningun byte comparte disfraz: `decode` podra volver sin ambiguedad."""
    tokenizer = Tokenizer(*rutas)
    assert len(tokenizer._char_byte) == 256
    for byte, char in tokenizer._byte_char.items():
        assert tokenizer._char_byte[char] == byte


def test_casos_conocidos_de_la_tabla(rutas):
    """Los cuatro disfraces que aparecen en el diseno."""
    tokenizer = Tokenizer(*rutas)
    assert tokenizer._byte_char[32] == "Ġ"
    assert tokenizer._byte_char[10] == "Ċ"
    assert tokenizer._byte_char[65] == "A"
    assert tokenizer._byte_char[195] == "Ã"


# --------------------------------------------------------------------------
# 3. Entradas invalidas en la construccion
# --------------------------------------------------------------------------

def test_vocab_ausente(tmp_path):
    """Ruta que no lleva a ningun archivo: la corta `FilePath` de pydantic."""
    with pytest.raises(ValidationError, match="path_not_file"):
        Tokenizer(str(tmp_path / "no_existe.json"),
                  escribir_merges(tmp_path),
                  escribir_tokenizer(tmp_path))


def test_vocab_vacio(tmp_path):
    """Un `{}` no es un vocabulario utilizable."""
    archivo = tmp_path / "vocab.json"
    archivo.write_text("{}", encoding="utf-8")
    with pytest.raises(ValueError, match="empty"):
        Tokenizer(str(archivo),
                  escribir_merges(tmp_path),
                  escribir_tokenizer(tmp_path))


def test_vocab_corrupto(tmp_path):
    """JSON invalido: el mensaje debe distinguirse del de archivo vacio."""
    archivo = tmp_path / "vocab.json"
    archivo.write_text('{"A": 65,', encoding="utf-8")
    with pytest.raises(ValueError, match="Corrupt JSON"):
        Tokenizer(str(archivo),
                  escribir_merges(tmp_path),
                  escribir_tokenizer(tmp_path))


def test_merges_ausente(tmp_path):
    """Falta `merges.txt`: la corta `FilePath` de pydantic."""
    with pytest.raises(ValidationError, match="path_not_file"):
        Tokenizer(escribir_vocab(tmp_path),
                  str(tmp_path / "no_existe.txt"),
                  escribir_tokenizer(tmp_path))


def test_merges_solo_cabecera(tmp_path):
    """Un `merges.txt` sin ninguna regla deja la tabla vacia."""
    archivo = tmp_path / "merges.txt"
    archivo.write_text("#version: 0.2\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Merge board is empty"):
        Tokenizer(escribir_vocab(tmp_path),
                  str(archivo),
                  escribir_tokenizer(tmp_path))


def test_merges_con_lineas_de_una_sola_pieza(tmp_path):
    """Las lineas que no traen dos piezas se ignoran, no revientan."""
    archivo = tmp_path / "merges.txt"
    archivo.write_text("#version: 0.2\nĠ a\nsuelto\n\nb c\n", encoding="utf-8")
    tokenizer = Tokenizer(escribir_vocab(tmp_path),
                          str(archivo),
                          escribir_tokenizer(tmp_path))
    assert ("Ġ", "a") in tokenizer._merge_board
    assert ("b", "c") in tokenizer._merge_board
    assert len(tokenizer._merge_board) == 2


def test_tokenizer_ausente(tmp_path):
    """Falta `tokenizer.json`: la corta `FilePath` de pydantic."""
    with pytest.raises(ValidationError, match="path_not_file"):
        Tokenizer(escribir_vocab(tmp_path),
                  escribir_merges(tmp_path),
                  str(tmp_path / "no_existe.json"))


def test_tokenizer_corrupto(tmp_path):
    """JSON invalido en `tokenizer.json`."""
    archivo = tmp_path / "tokenizer.json"
    archivo.write_text('{"added_tokens": [', encoding="utf-8")
    with pytest.raises(ValueError, match="Corrupt JSON"):
        Tokenizer(escribir_vocab(tmp_path),
                  escribir_merges(tmp_path),
                  str(archivo))


def test_tokenizer_sin_pre_tokenizer(tmp_path):
    """Falta la clave del patron: el error debe decir que fue leyendo ese archivo."""
    archivo = tmp_path / "tokenizer.json"
    archivo.write_text(json.dumps({"added_tokens": []}), encoding="utf-8")
    with pytest.raises(KeyError):
        Tokenizer(escribir_vocab(tmp_path),
                  escribir_merges(tmp_path),
                  str(archivo))


# --------------------------------------------------------------------------
# 4. `encode` — flujo normal
# --------------------------------------------------------------------------

def test_encode_texto_vacio(tmp_path):
    """Sin texto no hay tokens."""
    assert construir(tmp_path).encode("") == []


def test_encode_sin_ninguna_fusion(tmp_path):
    """Sin reglas aplicables, cada caracter disfrazado es un token."""
    tokenizer = construir(tmp_path, reglas=[("z", "z")])
    assert tokenizer.encode("Ab") == [ord("A"), ord("b")]


def test_encode_espacio_pegado_a_la_palabra(tmp_path):
    """El patron deja el espacio dentro del trozo: ' b' viaja junto."""
    tokenizer = construir(tmp_path, reglas=[("z", "z")])
    assert tokenizer.encode("a b") == [ord("a"), 32, ord("b")]


def test_encode_aplica_una_fusion(tmp_path):
    """Con la regla en la tabla, las dos piezas salen como un solo id."""
    tokenizer = construir(tmp_path,
                          extra_vocab={"ab": 900},
                          reglas=[("a", "b")])
    assert tokenizer.encode("ab") == [900]


def test_encode_respeta_la_prioridad_de_la_tabla(tmp_path):
    """Se fusiona la regla de linea mas baja, no la que aparece antes en el texto."""
    tokenizer = construir(tmp_path,
                          extra_vocab={"ow": 900, "l": ord("l")},
                          reglas=[("o", "w"), ("l", "o")])
    assert tokenizer.encode("low") == [ord("l"), 900]


def test_encode_encadena_fusiones(tmp_path):
    """Una fusion habilita la siguiente: el bucle vuelve a mirar desde el principio."""
    tokenizer = construir(tmp_path,
                          extra_vocab={"ab": 900, "abc": 901},
                          reglas=[("a", "b"), ("ab", "c")])
    assert tokenizer.encode("abc") == [901]


def test_encode_no_cruza_la_frontera_entre_trozos(tmp_path):
    """La pre-tokenizacion pone muros: ninguna fusion salta de un trozo a otro."""
    tokenizer = construir(tmp_path,
                          extra_vocab={"tĠ": 900},
                          reglas=[("t", "Ġ")])
    ids = tokenizer.encode("at b")
    assert 900 not in ids


def test_encode_numeros_digito_a_digito(tmp_path):
    """El patron lleva `\\p{N}` sin `+`: '40' nunca llega junto al bucle."""
    tokenizer = construir(tmp_path,
                          extra_vocab={"40": 900},
                          reglas=[("4", "0")])
    assert tokenizer.encode("40") == [ord("4"), ord("0")]


def test_encode_texto_no_ascii(tmp_path):
    """'José' entra como 5 simbolos: la 'é' son dos bytes."""
    tokenizer = construir(tmp_path, reglas=[("z", "z")])
    esperado = list("José".encode("utf-8"))
    assert tokenizer.encode("José") == esperado
    assert len(esperado) == 5


def test_encode_emoji_nunca_visto(tmp_path):
    """El suelo son los 256 bytes: ningun texto es intokenizable."""
    tokenizer = construir(tmp_path, reglas=[("z", "z")])
    ids = tokenizer.encode("🜛")
    assert ids == list("🜛".encode("utf-8"))


# --------------------------------------------------------------------------
# 5. `encode` — tokens especiales
# --------------------------------------------------------------------------

def test_encode_un_especial_solo(tmp_path):
    """Un especial es un unico id, y sale de `added_tokens`."""
    assert construir(tmp_path).encode(IM_START) == [151644]


def test_encode_especial_no_se_despedaza(tmp_path):
    """Sin el split previo, el patron partiria `<|im_start|>` en cuatro trozos."""
    tokenizer = construir(tmp_path)
    ids = tokenizer.encode(f"{IM_START}a{IM_END}")
    assert ids == [151644, ord("a"), 151645]


def test_encode_plantilla_de_chat(tmp_path):
    """Caso real: especiales, salto de linea y texto en el mismo string."""
    tokenizer = construir(tmp_path, reglas=[("z", "z")])
    ids = tokenizer.encode(f"{IM_START}user\nHi{IM_END}\n")
    assert ids[0] == 151644
    assert 151645 in ids
    assert 10 in ids  # el salto de linea, byte 10


# --------------------------------------------------------------------------
# 6. Limite y stress
# --------------------------------------------------------------------------

def test_encode_un_solo_caracter(tmp_path):
    """Trozo de longitud 1: no hay ningun par vecino que mirar."""
    assert construir(tmp_path).encode("a") == [ord("a")]


def test_encode_todo_el_texto_se_fusiona_en_uno(tmp_path):
    """Limite del bucle: fusiona hasta que solo queda un simbolo."""
    tokenizer = construir(tmp_path,
                          extra_vocab={"aa": 900, "aaaa": 901},
                          reglas=[("a", "a"), ("aa", "aa")])
    assert tokenizer.encode("aaaa") == [901]


def test_encode_repetido_no_arrastra_estado(tmp_path):
    """Dos llamadas seguidas dan lo mismo: nada queda vivo entre trozos."""
    tokenizer = construir(tmp_path,
                          extra_vocab={"ab": 900},
                          reglas=[("a", "b")])
    primera = tokenizer.encode("ab ab ab")
    segunda = tokenizer.encode("ab ab ab")
    assert primera == segunda
    assert primera.count(900) == 3


def test_encode_texto_largo_termina(tmp_path):
    """Stress: 2000 caracteres con reglas encadenadas, sin colgarse."""
    tokenizer = construir(tmp_path,
                          extra_vocab={"ab": 900, "abab": 901},
                          reglas=[("a", "b"), ("ab", "ab")])
    ids = tokenizer.encode("abab" * 500)
    assert ids == [901] * 500


# --------------------------------------------------------------------------
# 7. Pendientes del bloque — documentan lo que todavia no esta
# --------------------------------------------------------------------------

def test_decode_ida_y_vuelta(tmp_path):
    """Lo que sale de `encode` vuelve igual."""
    tokenizer = construir(tmp_path, reglas=[("z", "z")])
    for texto in ["a", "Greet shrek", "What is the sum of 40 and 2?",
                  "  espacios \n y saltos"]:
        assert tokenizer.decode(tokenizer.encode(texto)) == texto


def test_decode_no_ascii_de_una_sola_pieza(tmp_path):
    """'José' vuelve entero: los bytes se acumulan y se decodifican al final."""
    tokenizer = construir(tmp_path, reglas=[("z", "z")])
    assert tokenizer.decode(tokenizer.encode("Greet José")) == "Greet José"


def test_decode_con_fusiones(tmp_path):
    """La vuelta funciona igual cuando los ids son tokens fusionados."""
    tokenizer = construir(tmp_path,
                          extra_vocab={"ab": 900, "abc": 901},
                          reglas=[("a", "b"), ("ab", "c")])
    assert tokenizer.decode(tokenizer.encode("abc abc")) == "abc abc"


def test_decode_tira_los_especiales(tmp_path):
    """La vuelta es limpia: los especiales no llegan al string final."""
    tokenizer = construir(tmp_path, reglas=[("z", "z")])
    ids = tokenizer.encode(f"{IM_START}user\nHi{IM_END}")
    assert tokenizer.decode(ids) == "user\nHi"


def test_decode_id_invalido(tmp_path):
    """Un id que no existe ni en el vocabulario ni en los especiales."""
    tokenizer = construir(tmp_path)
    with pytest.raises(ValueError, match="isn't a valid id"):
        tokenizer.decode([999999])


def test_decode_lista_vacia(tmp_path):
    """Decision suya, 2026-08-24: simetrico con `encode("") -> []`."""
    tokenizer = construir(tmp_path)
    assert tokenizer.decode([]) == ""


def test_encode_con_token_fuera_del_vocabulario(tmp_path):
    """Vocabulario y merges que no se corresponden: mensaje propio, no `KeyError`.

    La tabla permite fusionar `("a", "b")`, pero `"ab"` no est\u00e1 en el
    vocabulario. Pasa cuando los dos archivos vienen de modelos distintos.
    """
    tokenizer = construir(tmp_path,
                          extra_vocab=None,
                          reglas=[("a", "b")])
    with pytest.raises(ValueError, match="ab"):
        tokenizer.encode("ab")


# --------------------------------------------------------------------------
# 8. El test que zanja el bloque — necesita el modelo
# --------------------------------------------------------------------------

TEXTOS_REALES = [
    # los prompts del subject
    "What is the sum of 2 and 3?",
    "What is the sum of 265 and 345?",
    "Greet shrek",
    "Greet john",
    "Reverse the string 'hello'",
    # el JSON que el modelo tiene que escribir, que es lo que pasa por decode
    '{"name": "fn_add_numbers", "parameters": {"a": 40, "b": 2}}',
    '{"name": "fn_reverse_string", "parameters": {"s": "hello"}}',
    '{"a": ',
    '{"a": 40,',
    # numeros: el patron los parte digito a digito
    "0", "40", "1234567890", "-3", "0.5", "-0.001", "9" * 40,
    # acentos y multibyte
    "Greet José", "José", "ñandú", "áéíóú ÀÈÌÒÙ", "Straße", "Ω≈ç√",
    "🜛", "Greet 🙂 y 👨‍👩‍👧‍👦",
    # espacios, saltos y tabuladores, que son ramas distintas del patron
    " ", "  ", "\n", "\n\n", "\t", "a \n b", "  espacios   raros \n\n y saltos\t",
    "Greet shrek!\n\n",
    # puntuacion pegada y comillas escapadas
    "Hi!", "Hi!!!", "que?", '"comillas"', 'con \\" escapada',
    "'s 't 're 've 'm 'll 'd",
    # plantilla de chat completa
    f"{IM_START}user\nGreet shrek{IM_END}\n",
    f"{IM_START}system\nYou call functions.{IM_END}\n"
    f"{IM_START}user\nWhat is the sum of 40 and 2?{IM_END}\n"
    f"{IM_START}assistant\n",
    ENDOFTEXT,
    # limite: cadena vacia y texto largo
    "",
    "Greet shrek. " * 50,
]


@pytest.fixture(scope="module")
def modelo_real():
    """El modelo del SDK, una sola vez para todo el modulo. Se salta si no esta."""
    sdk = pytest.importorskip("llm_sdk")
    try:
        return sdk.Small_LLM_Model()
    except Exception as error:  # modelo no descargado, sin red, etc.
        pytest.skip(f"modelo no disponible: {error}")


@pytest.fixture(scope="module")
def tokenizer_real(modelo_real):
    """Un `Tokenizer` con los archivos reales de Qwen, no de juguete."""
    return Tokenizer(modelo_real.get_path_to_vocab_file(),
                     modelo_real.get_path_to_merges_file(),
                     modelo_real.get_path_to_tokenizer_file())


@pytest.mark.parametrize("texto", TEXTOS_REALES)
def test_ids_identicos_a_los_del_sdk(tokenizer_real, modelo_real, texto):
    """`assert mi_ids == sdk_ids`. Es binario: o son los mismos ids o no."""
    assert tokenizer_real.encode(texto) == modelo_real.encode(texto)[0].tolist()


@pytest.mark.parametrize("texto", TEXTOS_REALES)
def test_ida_y_vuelta_con_el_vocabulario_real(tokenizer_real, texto):
    """Con 150.000 entradas, `decode(encode(t))` sigue devolviendo `t`."""
    ids = tokenizer_real.encode(texto)
    if not ids:  # cadena vacia: decode lanza por decision suya
        return
    esperado = texto.replace(IM_START, "").replace(IM_END, "").replace(ENDOFTEXT, "")
    assert tokenizer_real.decode(ids) == esperado


def test_vocabulario_real_tiene_el_tamano_del_modelo(tokenizer_real):
    """El vocabulario real, para dejar constancia de contra que se probo."""
    assert len(tokenizer_real.get_vocab()) > 150000


def test_los_ids_especiales_reales_estan_todos(tokenizer_real):
    """Sin el `[:3]`: los 26 especiales de Qwen, no solo los tres del chat."""
    especiales = tokenizer_real._special_ids
    assert especiales[IM_START] == 151644
    assert especiales[IM_END] == 151645
    assert especiales[ENDOFTEXT] == 151643
    assert len(especiales) > 3
    assert "<think>" in especiales


def test_ningun_id_generado_cae_fuera_del_vocabulario(tokenizer_real):
    """Todo id que salga de `encode` tiene que poder volver por `decode`."""
    ids = tokenizer_real.encode(
        "Greet José 🜛 con 1234567890 y \"comillas\"!\n\n")
    vocab_ids = set(tokenizer_real.get_vocab().values())
    especiales = set(tokenizer_real._special_ids.values())
    assert all(token_id in vocab_ids or token_id in especiales
               for token_id in ids)
