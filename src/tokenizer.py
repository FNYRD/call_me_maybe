from typing import Dict, Tuple, List, Callable, Any
import json
import regex
from pydantic import validate_call, FilePath


class Tokenizer:
    @validate_call
    def __init__(self, vocab_path: FilePath, merges_path: FilePath,
                 tokenizer_path: FilePath) -> None:
        self._special_ids: Dict[str, int] = {}
        self._vocab: Dict[str, int] = self._load_vocab(vocab_path)
        self._merge_board: Dict[Tuple[str, str],
                                int] = self._load_mergeboard(merges_path)
        self._tokenizer_pattern_compiler: regex.Pattern[str] = regex.compile(
            self._load_tokenizer(tokenizer_path))
        self._specials_pattern_compiler: regex.Pattern[str] = regex.compile(
            '(' + '|'.join(regex.escape(t) for t in self._special_ids) + ')')
        self._reversed_special_ids: Dict[int, str] = {
            id: word for word, id in self._special_ids.items()}
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

    def _load_tokenizer(self, tokenizer_path: FilePath) -> str:
        pattern: str = ""
        tokenizer_file: Dict[Any, Any] = {}
        try:
            with open(tokenizer_path, "r", encoding="utf-8") as file:
                tokenizer_file = json.load(file)
                self._special_ids = {content["content"]: content["id"]
                                     for content in tokenizer_file[
                                     "added_tokens"]}
                pattern = (
                    tokenizer_file["pre_tokenizer"]
                    ["pretokenizers"][0]["pattern"]["Regex"])
                if not pattern:
                    raise ValueError
                return pattern
        except KeyError:
            raise KeyError(
                "ERROR: An error occurred reading the tokenizer file")
        except FileNotFoundError:
            raise FileNotFoundError(
                f"This route {tokenizer_path} doesn't take to an "
                "existing file")
        except json.JSONDecodeError as error:
            raise ValueError(f"Corrupt JSON in {tokenizer_path}") from error
        except ValueError:
            raise ValueError("Tokenizer's file empty")

    def get_special_id(self, pattern: str) -> int:
        if pattern in self._special_ids:
            return self._special_ids[pattern]
        else:
            return 0

    @staticmethod
    def _load_vocab(vocab_path: FilePath) -> Dict[str, int]:
        vocab: Dict[str, int] = {}
        try:
            with open(vocab_path, "r", encoding="utf-8") as file:
                vocab = json.load(file)
                if not vocab:
                    raise ValueError
                return vocab
        except FileNotFoundError:
            raise FileNotFoundError(
                f"This route {vocab_path} doesn't take to an existing file")
        except json.JSONDecodeError as error:
            raise ValueError(f"Corrupt JSON in {vocab_path}") from error
        except ValueError:
            raise ValueError("Vocabulary's file empty")

    @staticmethod
    def _load_mergeboard(merges_path: FilePath) -> Dict[Tuple[str, str], int]:
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
                if not merge_board:
                    raise ValueError
                return merge_board
        except FileNotFoundError:
            raise FileNotFoundError(
                f"This route {merges_path} doesn't take to an existing file")
        except ValueError:
            raise ValueError("Merge board is empty")

    def get_vocab(self) -> Dict[str, int]:
        return self._vocab

    def encode(self, text: str) -> List[int]:
        id: int = 0
        token_ids: List[int] = []
        pattern_bytes: List[int] = []
        bytes_to_char: str = ""
        index_2_merge: Tuple[int, int] = (0, 0)
        chars_2_merge: List[str] = []
        no_merge_found: int = 999999999999
        loop_start: int = 9999999999999
        priority_bpe: int = loop_start
        priority_eval: int = 0
        split_by_specials: List[str] = [
            valid_token for valid_token in
            self._specials_pattern_compiler.split(text) if valid_token != ""]
        for chunk in split_by_specials:
            if id := self.get_special_id(chunk):
                token_ids.append(id)
            else:
                for pattern in self._tokenizer_pattern_compiler.findall(
                        chunk):
                    pattern_bytes = list(pattern.encode("utf-8"))
                    bytes_to_char = ""
                    for byte in pattern_bytes:
                        bytes_to_char += self._byte_char[byte]
                    chars_2_merge = list(bytes_to_char)
                    while priority_bpe != no_merge_found:
                        priority_bpe = no_merge_found
                        for index in range(len(chars_2_merge) - 1):
                            priority_eval = self._merge_board.get(
                                (chars_2_merge[index],
                                 chars_2_merge[index + 1]),
                                no_merge_found)
                            if priority_eval < priority_bpe:
                                priority_bpe = priority_eval
                                index_2_merge = (index, index + 1)
                        if priority_bpe != no_merge_found:
                            chars_2_merge[index_2_merge[0]] = (
                                chars_2_merge[index_2_merge[0]]
                                + chars_2_merge[index_2_merge[1]])
                            del chars_2_merge[index_2_merge[1]]
                    for token in chars_2_merge:
                        if self._vocab.get(token) is None:
                            raise ValueError(
                                f"Text: {token} is not a valid token id")
                        token_ids.append(self._vocab[token])
                    priority_bpe = loop_start
        return token_ids

    def decode(self, token_ids: List[int]) -> str:
        text: str = ""
        bytearr: bytearray = bytearray()
        if len(token_ids) <= 0:
            return ""
        for token_id in token_ids:
            if token_id in self._reversed_vocab:
                text += self._reversed_vocab[token_id]
            elif token_id in self._reversed_special_ids:
                pass
            else:
                raise ValueError(
                    "Error decoding token ids. "
                    f"{token_id} it isn't a valid id")
        bytearr = bytearray(self._char_byte[char] for char in text)
        return bytearr.decode("utf-8")
