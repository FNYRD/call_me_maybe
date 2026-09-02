from src.filemanager import Function, TypeSpec
from typing import List, Dict, Tuple, Optional, Union
from pydantic import validate_call
import json

DIGITS = "0123456789"


class Guardian:
    @validate_call
    def __init__(self, vocab: Dict[str, int],
                 reversed_vocab: Dict[int, str],
                 functions: List[Function]) -> None:
        self._vocab: Dict[str, int] = vocab
        self._reversed_vocab: Dict[int, str] = reversed_vocab
        self._functions: Dict[str, Function] = {f.name: f for f in functions}
        self._json_str: str = ""
        self._stack: List[Tuple[Dict[str, TypeSpec], int]] = []
        self._slot: Optional[str] = None
        self._written: str = ""
        self._done: bool = True
        self._cache: Dict[Tuple[Optional[str],
                                Union[str, int], str], List[int]] = {}

    @validate_call
    def start(self, prompt: str) -> None:
        self._json_str = (
            '{"prompt":' +
            f"{json.dumps(prompt)}"
            + ', "name": "')
        self._slot = "name"
        self._written = ""
        self._stack = []
        self._done = False

    def is_open(self) -> bool:
        return not self._done

    def get_json(self) -> str:
        return self._json_str

    def get_written(self) -> str:
        return self._written
    
    def _closing_char(self) -> str:
        current_object: Dict[str, TypeSpec] = {}
        current_index: int = 0
        current_object, current_index = self._stack[-1]
        if current_index != len(current_object) - 1:
            return ","
        return "}"

    def _char_ok(self, text: str, candidate2add: str) -> bool:
        match self._slot:
            case "name":
                if any(
                    function_name.startswith(text + candidate2add)
                    for function_name in self._functions
                ):
                    return True
                elif any(
                    function_name == text
                    for function_name in self._functions
                ) and candidate2add == '"':
                    return True
            case "number":
                if (text and all(c in DIGITS for c in text)
                        and candidate2add == "."):
                    return True
                elif candidate2add in DIGITS and text != "0":
                    return True
                elif (candidate2add == self._closing_char()
                      and (text and text[-1] in DIGITS)):
                    return True
            case "string":
                if candidate2add == '"' and '"' not in text:
                    return True
                elif '"' in text and self._closing_char() == candidate2add:
                    return True
                elif '"' not in text and 92 != ord(candidate2add) > 31:
                    return True
        return False

    def _slot_closed(self, text: str) -> bool:
        if not text:
            return False
        if self._slot == "name":
            return text.endswith('"')
        if self._slot == "string":
            return '"' in text and text[-1] == self._closing_char()
        if self._slot == "number":
            return text[-1] == self._closing_char()
        return False

    def _token_ok(self, token_text: str) -> bool:
        draft: str = self._written
        for char in token_text:
            if self._slot_closed(draft):
                return False
            if not self._char_ok(draft, char):
                return False
            draft += char
        return True

    def _cache_flags(self) -> int:
        match self._slot:
            case "number":
                if not self._written:
                    return 1
                elif self._written == "0":
                    return 2
                elif "." in self._written and self._written[-1].isdigit():
                    return 3
                elif self._written[-1].isdigit():
                    return 4
                elif self._written[-1].endswith("."):
                    return 5
            case "string":
                if '"' in self._written:
                    return 1
        return 0

    def get_valid_ids(self) -> List[int]:
        if self._done:
            raise ValueError("Guardian has no open session. Call start first")
        close: str = ('"' if self._slot == "name" else self._closing_char())
        flag: Union[str, int] = (
            self._written if self._slot ==
            "name" else self._cache_flags())
        current_state: Tuple[Optional[str], Union[str, int], str] = (
            self._slot, flag, close)
        if posible_cache := self._cache.get(current_state, []):
            return posible_cache
        else:
            self._cache[current_state] = [
                token_id
                for token_text, token_id in self._vocab.items()
                if self._token_ok(token_text)
            ]
        return self._cache[current_state]

    def _open_key(self) -> None:
        node, index = self._stack[-1]
        key: str = list(node)[index]
        spec: TypeSpec = node[key]
        self._json_str += f'"{key}": '
        if spec.properties:
            self._json_str += "{"
            self._stack.append((spec.properties, 0))
            self._open_key()
            return
        self._slot = spec.type
        self._written = ""
        if spec.type == "string":
            self._json_str += '"'

    def _close_level(self) -> None:
        self._stack.pop()
        self._written = ""
        if not self._stack:
            self._json_str += "}"
            self._slot = None
            self._done = True
            return
        node, index = self._stack[-1]
        index += 1
        self._stack[-1] = (node, index)
        if index < len(node):
            self._json_str += ", "
            self._open_key()
            return
        self._json_str += "}"
        self._close_level()

    def _close_name(self) -> None:
        name: str = self._written[:-1]
        parameters: Dict[str, TypeSpec] = self._functions[name].parameters
        self._json_str += ', "parameters": {'
        self._written = ""
        if not parameters:
            self._json_str += "}}"
            self._slot = None
            self._done = True
            return
        self._stack.append((parameters, 0))
        self._open_key()

    @validate_call
    def add_token(self, token_id: int) -> None:
        if self._done:
            raise ValueError("Guardian has no open session. Call start first")
        if token_id not in self._reversed_vocab:
            raise ValueError(f"Token id {token_id} is not in the vocabulary")
        token_text: str = self._reversed_vocab[token_id]
        self._json_str += token_text
        self._written += token_text
        if self._slot == "name":
            if self._written.endswith('"'):
                self._close_name()
                return
            candidates = [
                name for name in self._functions
                if name.startswith(self._written)
            ]
            if self._written and len(candidates) == 1:
                remainder = candidates[0][len(self._written):]
                self._json_str += remainder + '"'
                self._written = candidates[0] + '"'
                self._close_name()
            return
        if not self._slot_closed(self._written):
            return
        if self._written[-1] == ",":
            node, index = self._stack[-1]
            self._stack[-1] = (node, index + 1)
            self._open_key()
        else:
            self._close_level()
