import sys
import json
import random
import shutil
import threading
import time
from pathlib import Path
from typing import List, Callable, Optional

import numpy as np
import numpy.typing as npt
from pydantic import TypeAdapter

sys.path.insert(0, "/Users/jesusrosales/Documents/call_me_maybe")
from src.filemanager import Function, Prompt  # noqa: E402
from src.promptbuilder import PromptBuilder  # noqa: E402
from src.tokenizer import Tokenizer  # noqa: E402
from src.guardian import Guardian  # noqa: E402
from llm_sdk import Small_LLM_Model  # noqa: E402

VOCAB = Path(
    "/Users/jesusrosales/.cache/huggingface/hub/models--Qwen--Qwen3-0.6B/"
    "snapshots/c1899de289a04d12100db370d81485cdf75e47ca/vocab.json")
MERGES = Path(
    "/Users/jesusrosales/.cache/huggingface/hub/models--Qwen--Qwen3-0.6B/"
    "snapshots/c1899de289a04d12100db370d81485cdf75e47ca/merges.txt")
TOKENIZER = Path(
    "/Users/jesusrosales/.cache/huggingface/hub/models--Qwen--Qwen3-0.6B/"
    "snapshots/c1899de289a04d12100db370d81485cdf75e47ca/tokenizer.json")
FUNCIONES = Path(
    "/Users/jesusrosales/Documents/call_me_maybe/data/input/"
    "functions_definition.json")
PROMPTS = Path(
    "/Users/jesusrosales/Documents/call_me_maybe/data/input/"
    "function_calling_tests.json")

PAUSE = 1
PAUSE_TOKENIZER = 2.5
LETRA = 0.05
LETRA_LENTA = 0.12

RESET = "\033[0m"
CIAN = "\033[1;36m"
VERDE = "\033[1;32m"
ROJO = "\033[1;31m"
AMARILLO = "\033[1;33m"
AZUL = "\033[1;34m"

TITULO = "CALL_ME_MAYBE"
AUTOR = "Jesus Rosales"


def escribir_lento(texto: str, color: str = "", delay: float = LETRA) -> None:
    for char in texto:
        sys.stdout.write(f"{color}{char}{RESET}" if color else char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def resaltar_disfraz(texto: str, tk: Tokenizer) -> str:
    salida = ""
    for c in texto:
        byte = tk.char_byte[c]
        if 33 <= byte <= 126:
            salida += c
        else:
            salida += f"{ROJO}{c}{RESET}"
    return salida


def colorear_generacion(texto: str, tk: Tokenizer) -> str:
    salida = ""
    for c in texto:
        byte = tk.char_byte.get(c)
        if byte is not None and not (33 <= byte <= 126):
            salida += f"{ROJO}{c}{RESET}"
        else:
            salida += f"{CIAN}{c}{RESET}"
    return salida


LED_DELAY = 0.12

INTERIOR = TITULO.center(len(TITULO) + 4)
LARGO_CAJA = len(INTERIOR)
# perimetro: fila de arriba (incl. esquinas), baja por el lateral derecho,
# fila de abajo de vuelta (incl. esquinas), sube por el lateral izquierdo.
# cada paso se mueve a la celda vecina -> nunca hay salto.
PERIMETRO = (
    [("arriba", i) for i in range(LARGO_CAJA + 2)]
    + [("der", 0)]
    + [("abajo", i) for i in range(LARGO_CAJA + 1, -1, -1)]
    + [("izq", 0)]
)

ANCHO_LINEA = len(AUTOR)
COLORES_LINEA = [CIAN, AMARILLO]


def _lineas_caja(pos_perimetro: int) -> tuple[str, str, str]:
    arriba = list("╔" + "═" * LARGO_CAJA + "╗")
    abajo = list("╚" + "═" * LARGO_CAJA + "╝")
    izq_der = f"{CIAN}●{RESET}"
    mitad = len(PERIMETRO) // 2
    for offset in (0, mitad):
        fila, col = PERIMETRO[(pos_perimetro + offset) % len(PERIMETRO)]
        if fila == "arriba":
            arriba[col] = f"{CIAN}●{RESET}"
        elif fila == "abajo":
            abajo[col] = f"{CIAN}●{RESET}"
    return "".join(arriba), izq_der, "".join(abajo)


def _linea_rebote(pos: int, direccion: int, color_idx: int) -> str:
    linea = ["─"] * ANCHO_LINEA
    linea[pos] = f"{COLORES_LINEA[color_idx]}●{RESET}"
    return "".join(linea)


def header_led() -> None:
    """Dibuja el header una vez, quieto (para pantallas sin input detrás)."""
    ancho = shutil.get_terminal_size().columns
    pad = " " * max(0, (ancho - (LARGO_CAJA + 2)) // 2)
    mid = ("║" + INTERIOR + "║").center(ancho)
    autor = AUTOR.center(ancho)
    linea = ("─" * ANCHO_LINEA).center(ancho)
    print(pad + f"{CIAN}╔" + "═" * LARGO_CAJA + f"╗{RESET}")
    print(mid)
    print(pad + f"{CIAN}╚" + "═" * LARGO_CAJA + f"╝{RESET}")
    print(autor)
    print(linea)


def _frame_header(pos_perimetro: int, pos_linea: int, color_idx: int) -> str:
    ancho = shutil.get_terminal_size().columns
    pad = " " * max(0, (ancho - (LARGO_CAJA + 2)) // 2)
    pad_linea = " " * max(0, (ancho - ANCHO_LINEA) // 2)
    arriba, _, abajo = _lineas_caja(pos_perimetro)
    mid = ("║" + INTERIOR + "║").center(ancho)
    autor = AUTOR.center(ancho)
    linea = pad_linea + _linea_rebote(pos_linea, 1, color_idx)
    return (
        f"\0337\033[1;1H"
        f"\033[K{pad}{arriba}\n"
        f"\033[K{mid}\n"
        f"\033[K{pad}{abajo}\n"
        f"\033[K{autor}\n"
        f"\033[K{linea}\n"
        f"\0338"
    )


def _animar_header(detener: threading.Event) -> None:
    pos_perimetro = 0
    pos_linea = 0
    direccion = 1
    color_idx = 0
    while not detener.is_set():
        sys.stdout.write(_frame_header(pos_perimetro, pos_linea, color_idx))
        sys.stdout.flush()
        pos_perimetro += 1
        pos_linea += direccion
        if pos_linea in (0, ANCHO_LINEA - 1):
            direccion *= -1
            color_idx = (color_idx + 1) % len(COLORES_LINEA)
        time.sleep(LED_DELAY)


def input_animado(prompt: str) -> str:
    """input() normal, con el header animando arriba mientras se espera."""
    detener = threading.Event()
    hilo = threading.Thread(
        target=_animar_header, args=(detener,), daemon=True)
    hilo.start()
    try:
        respuesta = input(prompt)
    finally:
        detener.set()
        hilo.join()
    return respuesta


def limpiar_pantalla() -> None:
    sys.stdout.write("\033[2J\033[H")


def traducir_strings(parametros: dict, tk: Tokenizer) -> None:
    for clave, valor in parametros.items():
        if isinstance(valor, str):
            crudo = bytearray(tk.char_byte[c] for c in valor)
            real = crudo.replace(
                bytes([196, 160]), bytes([32])).decode("utf-8")
            sys.stdout.write(
                f"  {AMARILLO}{clave}{RESET}: "
                f"{resaltar_disfraz(valor, tk)} -> ")
            sys.stdout.flush()
            escribir_lento(real, color=VERDE, delay=LETRA_LENTA)
        elif isinstance(valor, dict):
            traducir_strings(valor, tk)


def generar(user_prompt: str, builder: PromptBuilder, tk: Tokenizer,
            guardian: Guardian,
            get_logits: Callable[[List[int]], List[float]]) -> None:
    system_prompt = builder.get_prompt(user_prompt)
    guardian.start(user_prompt)
    limite: Callable[[], bool] = (
        lambda: len(guardian.get_written()) <= len(user_prompt))

    # el esqueleto ({"prompt":"...", "name": ") ya lo escribió start(),
    # no lo escribió el modelo -- va sin colorear.
    sys.stdout.write(guardian.get_json())
    sys.stdout.flush()
    escrito_hasta = len(guardian.get_json())
    while guardian.is_open() and limite():
        tokenizados = tk.encode(system_prompt + guardian.get_json())
        validos = guardian.get_valid_ids()
        logits: npt.NDArray[np.float64] = np.array(get_logits(tokenizados))
        limpios: npt.NDArray[np.float64] = np.full(len(logits), -np.inf)
        limpios[validos] = logits[validos]
        elegido = int(np.argmax(limpios))
        guardian.add_token(elegido)

        actual = guardian.get_json()
        nuevo = actual[escrito_hasta:]
        escrito_hasta = len(actual)
        sys.stdout.write(colorear_generacion(nuevo, tk))
        sys.stdout.flush()
        time.sleep(PAUSE)

    print()
    if not limite():
        print("(the model entered a loop, didn't close the JSON)")
        return

    resultado = json.loads(guardian.get_json())
    if isinstance(resultado.get("parameters"), dict):
        print("String translation:")
        traducir_strings(resultado["parameters"], tk)


def menu_generar(prompts: List[Prompt], builder: PromptBuilder,
                  tk: Tokenizer, funciones: List[Function],
                  get_logits: Callable[[List[int]], List[float]]) -> None:
    while True:
        limpiar_pantalla()
        header_led()
        print(f"\n{AZUL}Pick a prompt (0 to go back):{RESET}")
        for i, p in enumerate(prompts, start=1):
            print(f"  {AMARILLO}{i}.{RESET} {p.prompt}")
        eleccion = input_animado("> ").strip()
        if eleccion == "0":
            return
        if not eleccion.isdigit() or not (1 <= int(eleccion) <= len(prompts)):
            print(f"{ROJO}Invalid option.{RESET}")
            continue
        guardian = Guardian(
            tk.get_vocab(), tk.get_reversed_vocab(), funciones)
        generar(
            prompts[int(eleccion) - 1].prompt,
            builder, tk, guardian, get_logits)
        input("\n(enter to go back to the menu)")


def paso(numero: int, titulo: str, valor: object,
          pausa: float = PAUSE) -> None:
    print(f"\n{CIAN}{numero}.{RESET} {titulo}")
    print(f"   {valor!r}")
    time.sleep(pausa)


def proceso_tokenizer(tk: Tokenizer) -> None:
    limpiar_pantalla()
    header_led()
    print(f"\n{AZUL}View generation and translation process{RESET}")
    print("(this doesn't call the model, everything else is real)\n")
    texto = input_animado("Type a text: ")
    byte_char = {byte: char for char, byte in tk.char_byte.items()}

    # --- encode, from sentence to token id ---
    paso(1, "Input text", texto, pausa=PAUSE_TOKENIZER)

    bytes_utf8 = list(texto.encode("utf-8"))
    paso(2, "Text to UTF-8 bytes", bytes_utf8, pausa=PAUSE_TOKENIZER)

    disfrazado_entrada = "".join(byte_char[b] for b in bytes_utf8)
    print(f"\n{CIAN}3.{RESET} Bytes to 'byte-256' "
          "(visible-character disguise)")
    print(f"   {resaltar_disfraz(disfrazado_entrada, tk)}")
    time.sleep(PAUSE_TOKENIZER)

    ids = tk.encode(texto)
    paso(4, "real encode() (also includes the split and BPE merges) "
         "-> token ids", ids, pausa=PAUSE_TOKENIZER)

    # --- the model, simulated ---
    logits_ejemplo = {tid: round(random.uniform(-5, 5), 2) for tid in ids}
    paso(5, "Logits simulation", logits_ejemplo, pausa=PAUSE_TOKENIZER)

    print(f"\n{CIAN}6.{RESET} (SIMULATED) the model 'chose' to return "
          "this same full sequence of ids:")
    print(f"   {ids}")
    time.sleep(PAUSE_TOKENIZER)

    # --- decode, from token id back to sentence, same detail ---
    disfrazado_salida = "".join(tk.get_reversed_vocab()[i] for i in ids)
    print(f"\n{CIAN}7.{RESET} Token ids to disguised text "
          "(vocab, untranslated)")
    print(f"   {resaltar_disfraz(disfrazado_salida, tk)}")
    time.sleep(PAUSE_TOKENIZER)

    bytes_salida = [tk.char_byte[c] for c in disfrazado_salida]
    paso(8, "Disguised text to real 'byte-256'", bytes_salida,
         pausa=PAUSE_TOKENIZER)

    real = tk.decode(ids)
    print(f"\n{CIAN}9.{RESET} Real bytes to final str "
          "(real decode(), with translation)")
    sys.stdout.write("   ")
    escribir_lento(real, color=VERDE, delay=LETRA_LENTA)
    time.sleep(PAUSE_TOKENIZER)

    input("\n(enter to go back to the menu)")


def main() -> None:
    with open(FUNCIONES, "r", encoding="utf-8") as file:
        funciones: List[Function] = TypeAdapter(
            List[Function]).validate_python(json.load(file))
    with open(PROMPTS, "r", encoding="utf-8") as file:
        prompts: List[Prompt] = TypeAdapter(
            List[Prompt]).validate_python(json.load(file))

    tk = Tokenizer(VOCAB, MERGES, TOKENIZER)
    builder = PromptBuilder(funciones)
    get_logits: Optional[Callable[[List[int]], List[float]]] = None

    while True:
        limpiar_pantalla()
        header_led()
        print(f"\n{AMARILLO}1.{RESET} Generate response")
        print(f"{AMARILLO}2.{RESET} View generation and translation process")
        print(f"{AMARILLO}0.{RESET} Exit")
        eleccion = input_animado("> ").strip()
        if eleccion == "0":
            break
        elif eleccion == "1":
            if get_logits is None:
                print(f"\n{AZUL}Loading the model...{RESET}")
                modelo = Small_LLM_Model()
                get_logits = modelo.get_logits_from_input_ids
            menu_generar(prompts, builder, tk, funciones, get_logits)
        elif eleccion == "2":
            proceso_tokenizer(tk)
        else:
            print(f"{ROJO}Invalid option.{RESET}")
            time.sleep(PAUSE)


if __name__ == "__main__":
    main()
