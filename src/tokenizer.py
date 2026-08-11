from typing import Dict, Tuple, List, Callable
import json


class Tokenizer:
    def __init__(self, vocab_path: str, merges_path: str):
        self._vocab_path: str = vocab_path
        self._merges_path: str = merges_path
        self._vocab: Dict[str, int] = {}
        with open(self._vocab_path, "r", encoding="utf-8") as file:
            self._vocab = json.load(file)
        if not self._vocab:
            raise ValueError("There was an error loading the vocabulary")
        self._merge_board: Dict[Tuple[str, str], int] = {}
        with open(self._merges_path, "r", encoding="utf-8") as file:
            counter: int = 0
            tokens: List[str] = []
            for line in file:
                if counter != 0:
                    tokens = line.strip().split()
                    self._merge_board[(tokens[0], tokens[1])] = counter
                counter += 1
        if not self._merge_board:
            raise ValueError("There was an error loading the merge board")
        self._reversed_vocab: Dict[int, str] = {
            id: word for word, id in self._vocab.items()}
        self._visible_bytes: set[int] = set(range(33, 127)) | set(
            range(161, 173)) | set(range(174, 256))
        self._invisible_bytes: List[int] = [byte for byte in range(
            0, 256) if byte not in self._visible_bytes]
        self._in_visible: Callable[[
            int], int] = (lambda byte: byte if byte in
                          self._visible_bytes else 256
                          + self._invisible_bytes.index(byte))
        self._byte_char: Dict[int, str] = {
            byte: chr(self._in_visible(byte)) for byte in range(0, 256)}
        self._char_byte: Dict[str, int] = {
            char: byte for byte, char in self._byte_char.items()}

    def get_vocab(self) -> Dict[str, int]:
        return self._vocab

    def encode(self, text: str) -> List[int]:
        return [0]

    def decode(self, token_ids: List[int]) -> str:
        return ""
