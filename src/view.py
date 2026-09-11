import sys
import json
import random
import shutil
import threading
import time
from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np
import numpy.typing as npt
from pydantic import FilePath, TypeAdapter, validate_call

from .filemanager import Function, Prompt
from .promptbuilder import PromptBuilder
from .tokenizer import Tokenizer
from .guardian import Guardian
from llm_sdk import Small_LLM_Model

RESET = "\033[0m"
CYAN = "\033[1;36m"
GREEN = "\033[1;32m"
RED = "\033[1;31m"
YELLOW = "\033[1;33m"
BLUE = "\033[1;34m"

PAUSE = 1
TOKENIZER_PAUSE = 2.5
CHAR_DELAY = 0.05
SLOW_CHAR_DELAY = 0.12
LED_DELAY = 0.12
LINE_COLORS = [CYAN, YELLOW]


class View:
    @validate_call
    def __init__(self, vocab_path: FilePath, merges_path: FilePath,
                 tokenizer_path: FilePath, functions_path: FilePath,
                 prompts_path: FilePath, title: str, author: str) -> None:
        self._tokenizer: Tokenizer = Tokenizer(
            vocab_path, merges_path, tokenizer_path)
        self._functions: List[Function] = self._load_functions(
            functions_path)
        self._prompts: List[Prompt] = self._load_prompts(prompts_path)
        self._builder: PromptBuilder = PromptBuilder(self._functions)
        self._title: str = title
        self._author: str = author
        self._get_logits: Optional[
            Callable[[List[int]], List[float]]] = None
        self._box_interior: str = title.center(len(title) + 4)
        self._box_width: int = len(self._box_interior)
        self._box_perimeter: List[Tuple[str, int]] = (
            [("top", i) for i in range(self._box_width + 2)]
            + [("right", 0)]
            + [("bottom", i) for i in range(self._box_width + 1, -1, -1)]
            + [("left", 0)])
        self._line_width: int = len(author)

    @staticmethod
    def _load_functions(functions_path: FilePath) -> List[Function]:
        with open(functions_path, "r", encoding="utf-8") as file:
            return TypeAdapter(List[Function]).validate_python(
                json.load(file))

    @staticmethod
    def _load_prompts(prompts_path: FilePath) -> List[Prompt]:
        with open(prompts_path, "r", encoding="utf-8") as file:
            return TypeAdapter(List[Prompt]).validate_python(
                json.load(file))

    @staticmethod
    def _write_slowly(
            text: str, color: str = "", delay: float = CHAR_DELAY) -> None:
        for char in text:
            sys.stdout.write(f"{color}{char}{RESET}" if color else char)
            sys.stdout.flush()
            time.sleep(delay)
        print()

    def _highlight_disguise(self, text: str) -> str:
        output: str = ""
        for char in text:
            byte: int = self._tokenizer.char_byte[char]
            if 33 <= byte <= 126:
                output += char
            else:
                output += f"{RED}{char}{RESET}"
        return output

    def _colorize_generation(self, text: str) -> str:
        output: str = ""
        for char in text:
            byte: Optional[int] = self._tokenizer.char_byte.get(char)
            if byte is not None and not (33 <= byte <= 126):
                output += f"{RED}{char}{RESET}"
            else:
                output += f"{CYAN}{char}{RESET}"
        return output

    def _box_lines(self, perimeter_position: int) -> Tuple[str, str, str]:
        top: List[str] = list("╔" + "═" * self._box_width + "╗")
        bottom: List[str] = list("╚" + "═" * self._box_width + "╝")
        side_dot: str = f"{CYAN}●{RESET}"
        half: int = len(self._box_perimeter) // 2
        for offset in (0, half):
            side, col = self._box_perimeter[
                (perimeter_position + offset) % len(self._box_perimeter)]
            if side == "top":
                top[col] = f"{CYAN}●{RESET}"
            elif side == "bottom":
                bottom[col] = f"{CYAN}●{RESET}"
        return "".join(top), side_dot, "".join(bottom)

    def _bounce_line(self, position: int, color_index: int) -> str:
        line: List[str] = ["─"] * self._line_width
        line[position] = f"{LINE_COLORS[color_index]}●{RESET}"
        return "".join(line)

    def _draw_header(self) -> None:
        width: int = shutil.get_terminal_size().columns
        pad: str = " " * max(0, (width - (self._box_width + 2)) // 2)
        middle: str = ("║" + self._box_interior + "║").center(width)
        author: str = self._author.center(width)
        line: str = ("─" * self._line_width).center(width)
        print(pad + f"{CYAN}╔" + "═" * self._box_width + f"╗{RESET}")
        print(middle)
        print(pad + f"{CYAN}╚" + "═" * self._box_width + f"╝{RESET}")
        print(author)
        print(line)

    def _frame_header(
            self, perimeter_position: int, line_position: int,
            color_index: int) -> str:
        width: int = shutil.get_terminal_size().columns
        pad: str = " " * max(0, (width - (self._box_width + 2)) // 2)
        line_pad: str = " " * max(0, (width - self._line_width) // 2)
        top, _, bottom = self._box_lines(perimeter_position)
        middle: str = ("║" + self._box_interior + "║").center(width)
        author: str = self._author.center(width)
        line: str = line_pad + self._bounce_line(line_position, color_index)
        return (
            f"\0337\033[1;1H"
            f"\033[K{pad}{top}\n"
            f"\033[K{middle}\n"
            f"\033[K{pad}{bottom}\n"
            f"\033[K{author}\n"
            f"\033[K{line}\n"
            f"\0338"
        )

    def _animate_header(self, stop: threading.Event) -> None:
        perimeter_position: int = 0
        line_position: int = 0
        direction: int = 1
        color_index: int = 0
        while not stop.is_set():
            sys.stdout.write(
                self._frame_header(
                    perimeter_position, line_position, color_index))
            sys.stdout.flush()
            perimeter_position += 1
            line_position += direction
            if line_position in (0, self._line_width - 1):
                direction *= -1
                color_index = (color_index + 1) % len(LINE_COLORS)
            time.sleep(LED_DELAY)

    def _animated_input(self, prompt: str) -> str:
        stop: threading.Event = threading.Event()
        thread: threading.Thread = threading.Thread(
            target=self._animate_header, args=(stop,), daemon=True)
        thread.start()
        try:
            answer: str = input(prompt)
        finally:
            stop.set()
            thread.join()
        return answer

    @staticmethod
    def _clear_screen() -> None:
        sys.stdout.write("\033[2J\033[H")

    def _translate_strings(self, parameters: Dict[str, Any]) -> None:
        for key, value in parameters.items():
            if isinstance(value, str):
                raw: bytearray = bytearray(
                    self._tokenizer.char_byte[char] for char in value)
                decoded: str = raw.replace(
                    bytes([196, 160]), bytes([32])).decode("utf-8")
                sys.stdout.write(
                    f"  {YELLOW}{key}{RESET}: "
                    f"{self._highlight_disguise(value)} -> ")
                sys.stdout.flush()
                self._write_slowly(
                    decoded, color=GREEN, delay=SLOW_CHAR_DELAY)
            elif isinstance(value, dict):
                self._translate_strings(value)

    def _generate(self, user_prompt: str, guardian: Guardian) -> None:
        get_logits: Optional[Callable[[List[int]], List[float]]] = (
            self._get_logits)
        if get_logits is None:
            raise ValueError("The model hasn't been loaded yet")
        system_prompt: str = self._builder.get_prompt(user_prompt)
        guardian.start(user_prompt)
        under_limit: Callable[[], bool] = (
            lambda: len(guardian.get_written()) <= len(user_prompt))
        sys.stdout.write(guardian.get_json())
        sys.stdout.flush()
        written_up_to: int = len(guardian.get_json())
        while guardian.is_open() and under_limit():
            token_ids: List[int] = self._tokenizer.encode(
                system_prompt + guardian.get_json())
            valid_ids: List[int] = guardian.get_valid_ids()
            logits: npt.NDArray[np.float64] = np.array(
                get_logits(token_ids))
            clean_logits: npt.NDArray[np.float64] = np.full(
                len(logits), -np.inf)
            clean_logits[valid_ids] = logits[valid_ids]
            chosen: int = int(np.argmax(clean_logits))
            guardian.add_token(chosen)

            current: str = guardian.get_json()
            new_text: str = current[written_up_to:]
            written_up_to = len(current)
            sys.stdout.write(self._colorize_generation(new_text))
            sys.stdout.flush()
            time.sleep(PAUSE)

        print()
        if not under_limit():
            print("(the model entered a loop, didn't close the JSON)")
            return

        result: Dict[str, Any] = json.loads(guardian.get_json())
        if isinstance(result.get("parameters"), dict):
            print("String translation:")
            self._translate_strings(result["parameters"])

    def _generation_menu(self) -> None:
        while True:
            self._clear_screen()
            self._draw_header()
            print(f"\n{BLUE}Pick a prompt (0 to go back):{RESET}")
            for i, prompt in enumerate(self._prompts, start=1):
                print(f"  {YELLOW}{i}.{RESET} {prompt.prompt}")
            choice: str = self._animated_input("> ").strip()
            if choice == "0":
                return
            if not choice.isdigit() or not (
                    1 <= int(choice) <= len(self._prompts)):
                print(f"{RED}Invalid option.{RESET}")
                continue
            guardian: Guardian = Guardian(
                self._tokenizer.get_vocab(),
                self._tokenizer.get_reversed_vocab(), self._functions)
            self._generate(self._prompts[int(choice) - 1].prompt, guardian)
            input("\n(enter to go back to the menu)")

    @staticmethod
    def _step(number: int, title: str, value: object,
              pause: float = PAUSE) -> None:
        print(f"\n{CYAN}{number}.{RESET} {title}")
        print(f"   {value!r}")
        time.sleep(pause)

    def _tokenizer_process(self) -> None:
        self._clear_screen()
        self._draw_header()
        print(f"\n{BLUE}View generation and translation process{RESET}")
        print("(this doesn't call the model, everything else is real)\n")
        text: str = self._animated_input("Type a text: ")
        byte_char: Dict[int, str] = {
            byte: char
            for char, byte in self._tokenizer.char_byte.items()}
        self._step(1, "Input text", text, pause=TOKENIZER_PAUSE)
        utf8_bytes: List[int] = list(text.encode("utf-8"))
        self._step(
            2, "Text to UTF-8 bytes", utf8_bytes, pause=TOKENIZER_PAUSE)
        disguised_input: str = "".join(byte_char[b] for b in utf8_bytes)
        print(f"\n{CYAN}3.{RESET} Bytes to 'byte-256' "
              "(visible-character disguise)")
        print(f"   {self._highlight_disguise(disguised_input)}")
        time.sleep(TOKENIZER_PAUSE)

        ids: List[int] = self._tokenizer.encode(text)
        self._step(4, "real encode() (also includes the split and BPE "
                   "merges) -> token ids", ids, pause=TOKENIZER_PAUSE)
        sample_logits: Dict[int, float] = {
            token_id: round(random.uniform(-5, 5), 2) for token_id in ids}
        self._step(
            5, "Logits simulation", sample_logits, pause=TOKENIZER_PAUSE)
        print(f"\n{CYAN}6.{RESET} (SIMULATED) the model 'chose' to return "
              "this same full sequence of ids:")
        print(f"   {ids}")
        time.sleep(TOKENIZER_PAUSE)
        reversed_vocab: Dict[int, str] = self._tokenizer.get_reversed_vocab()
        disguised_output: str = "".join(reversed_vocab[i] for i in ids)
        print(f"\n{CYAN}7.{RESET} Token ids to disguised text "
              "(vocab, untranslated)")
        print(f"   {self._highlight_disguise(disguised_output)}")
        time.sleep(TOKENIZER_PAUSE)
        output_bytes: List[int] = [
            self._tokenizer.char_byte[char] for char in disguised_output]
        self._step(8, "Disguised text to real 'byte-256'", output_bytes,
                   pause=TOKENIZER_PAUSE)
        decoded: str = self._tokenizer.decode(ids)
        print(f"\n{CYAN}9.{RESET} Real bytes to final str "
              "(real decode(), with translation)")
        sys.stdout.write("   ")
        self._write_slowly(decoded, color=GREEN, delay=SLOW_CHAR_DELAY)
        time.sleep(TOKENIZER_PAUSE)
        input("\n(enter to go back to the menu)")

    def run(self) -> None:
        while True:
            self._clear_screen()
            self._draw_header()
            print(f"\n{YELLOW}1.{RESET} Generate response")
            print(f"{YELLOW}2.{RESET} View generation and translation "
                  "process")
            print(f"{YELLOW}0.{RESET} Exit")
            choice: str = self._animated_input("> ").strip()
            if choice == "0":
                break
            elif choice == "1":
                if self._get_logits is None:
                    print(f"\n{BLUE}Loading the model...{RESET}")
                    model: Small_LLM_Model = Small_LLM_Model()
                    self._get_logits = model.get_logits_from_input_ids
                self._generation_menu()
            elif choice == "2":
                self._tokenizer_process()
            else:
                print(f"{RED}Invalid option.{RESET}")
                time.sleep(PAUSE)
