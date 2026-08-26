from src.promptbuilder import Function
from typing import List, Dict

class Guardian:
    def __init__(self, vocab: Dict[str, int],
    reversed_vocab: Dict[int, str], functions: List[Function]) -> None:
        self._vocab: Dict[str, int] = vocab
        self._reversed_vocab: Dict[str, int] = reversed_vocab
        self._functions: Dict[str, Function] = {f.name: f for f in functions}
        self._state: str = ""
        self._stack: List[str] = []

    def get_valid_ids()


    