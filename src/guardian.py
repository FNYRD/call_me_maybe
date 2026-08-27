from src.filemanager import Function, TypeSpec
from typing import List, Dict, Tuple, Optional
from pydantic import validate_call
import json

class Guardian:
    @validate_call
    def __init__(self, vocab: Dict[str, int],
    reversed_vocab: Dict[int, str], functions: List[Function]) -> None:
        self._vocab: Dict[str, int] = vocab
        self._reversed_vocab: Dict[int, str] = reversed_vocab
        self._functions: Dict[str, Function] = {f.name: f for f in functions}
        self._json_str: str = ""
        self._stack: List[Tuple[Dict[str, TypeSpec], int]] = []
        self._slot: Optional[str] = None
        self._written: str = ""
        self._done: bool = True

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
                    function_name.startswith(candidate2add)
                    for function_name in self._functions
                    ):
                        return True
                return False
            
        return True #mypy

    
    