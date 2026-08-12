from typing import Dict, Tuple, List, Callable, Optional
import json


class Tokenizer:
    def __init__(self, vocab_path: str, merges_path: str):
        self._vocab: Optional[Dict[str, int]] = self._load_vocab(vocab_path)
        self._merge_board: Optional[Dict[Tuple[str, str],
                                         int]] = self._load_mergeboard(merges_path)
        if not self._merge_board:
            raise ValueError("There was an error loading the merge board")
        if self._vocab:
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

    @staticmethod
    def _load_vocab(vocab_path: str) -> Optional[Dict[str, int]]:
        vocab: Dict[str, int] = {}
        try:
            with open(vocab_path, "r", encoding="utf-8") as file:
                vocab = json.load(file)
                if vocab and len(vocab) <= 0:
                    raise ValueError("Vocabulary's file empty")
                return vocab
        except:
            raise FileNotFoundError(
                f"This route {vocab_path} doesn't take to an existing file")

    @staticmethod
    def _load_mergeboard(merges_path: str) -> Optional[Dict[Tuple[str, str], int]]:
        merge_board: Dict[Tuple[str, str], int] = {}
        try:
            with open(merges_path, "r", encoding="utf-8") as file:
                counter: int = 0
                tokens: List[str] = []
                for line in file:
                    if counter != 0:
                        tokens = line.strip().split()
                        if len(tokens) == 2:
                            merge_board[(tokens[0], tokens[1])] = counter
                    counter += 1
                if merge_board and len(merge_board):
                    raise ValueError("Merge board is empty")
                return merge_board
        except:
            raise FileNotFoundError(
                f"This route {merges_path} doesn't take to an existing file")

    def get_vocab(self) -> Optional[Dict[str, int]]:
        if self._vocab and len(self._vocab) > 0:
            return self._vocab
        return None

    def encode(self, text: str) -> List[int]:
        return [0]

    def decode(self, token_ids: List[int]) -> str:
        return ""
