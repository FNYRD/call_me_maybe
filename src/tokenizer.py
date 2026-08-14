from typing import Dict, Tuple, List, Callable, Any
import json
import regex


class Tokenizer:
    def __init__(self, vocab_path: str, merges_path: str, tokenizer_path: str):
        self.special_ids: Dict[str, int] = {}
        self._vocab: Dict[str, int] = self._load_vocab(vocab_path)
        self._merge_board: Dict[Tuple[str, str],
                                int] = self._load_mergeboard(merges_path)
        self._tokenizer_pattern_compiler: regex.Pattern = regex.compile(
            self._load_tokenizer(tokenizer_path))
        self._specials_pattern_compiler: regex.Pattern = regex.compile(
            '(' + '|'.join(regex.escape(t) for t in self.special_ids) + ')')
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

    def _load_tokenizer(self, tokenizer_path: str) -> str:
        pattern: str = ""
        tokenizer_file: Dict[Any, Any] = {}
        try:
            with open(tokenizer_path, "r", encoding="utf-8") as file:
                tokenizer_file = json.load(file)
                self.special_ids = {content["content"]: content["id"]
                                    for content in tokenizer_file["added_tokens"][:3]}
                pattern = tokenizer_file["pre_tokenizer"]["pretokenizers"][0]["pattern"]["Regex"]
                if not pattern:
                    raise ValueError
                return pattern
        except KeyError:
            raise KeyError(
                "ERROR: An error occurred reading the tokenizer file")
        except FileNotFoundError:
            raise FileNotFoundError(
                f"This route {tokenizer_path} doesn't take to an existing file")
        except json.JSONDecodeError as error:
            raise ValueError(f"Corrupt JSON in {tokenizer_path}") from error
        except ValueError:
            raise ValueError("Tokenizer's file empty")

    def get_special_id(self, pattern: str) -> int:
        if pattern in self.special_ids:
            return self.special_ids[pattern]
        else:
            return 0

    @staticmethod
    def _load_vocab(vocab_path: str) -> Dict[str, int]:
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
    def _load_mergeboard(merges_path: str) -> Dict[Tuple[str, str], int]:
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
        pattern_bytes: list[int] = []
        bytes_to_char: str = ""
        split_by_specials: list[str] = [
            valid_token for valid_token in
            self._specials_pattern_compiler.split(text) if valid_token != ""]
        for chunck in split_by_specials:
            if id := self.get_special_id(chunck):
                token_ids.append(id)
            else:
                for pattern in self._tokenizer_pattern_compiler.findall(chunck):
                    pattern_bytes = list(pattern.encode("utf-8"))
                    bytes_to_char = ""
                    for byte in pattern_bytes:
                        bytes_to_char += self._byte_char[byte]
        # HASTA ESTE PUNTO, YA FUERON PARTIDOS LOS PROMPTS (TEXTO) EN
        # TRAMOS ESPECIALES O NO. LOS TRAMOS ESPECIALES TIENEN SU ID EN 
        # UN JSON Y NO EN EL VOCABULARIO, POR ESO SE TRATAN POR SEPARADO
        # CUANDO NO ES ESPECIAL, SE PASA PRIMERO POR UNA SEPARACION EN PATRONES
        # QUE EL MODELO USA POR DEFECTO, ESTOS SON TRAMOS DE TEXTO EN EL QUE EXISTE UN
        # PATRON REGEX PARA DEFINIR COMO EL MODELO APRENDIO A LEER LOS BYTES Y PASARLOS
        # PARA SU ID. (ESTO LO TENGO QUE REFORZAR UN MONTON). LUEGO DE HABERLO SEPARADO
        # CADA TRAMO SE DIVIDE EN BYTES Y TENIENDO LOS BYTES SE PASA A MI TRABLA DE CHAR
        # PARA OBTENER EN TEXTO EN BASE 256. LO SIGUIENTE AL TENER EL TEXTO EN ES BASE
        # ES COMENZAR A DIVIDIR CADA TRAMO EN TOKENS USANDO LA MERGE TABLE QUE ES EL PUNTO
        # DONDE SE COMENZARA EN LA SIGUIENTE SESION

        
        return [0]

    def decode(self, token_ids: List[int]) -> str:
        return ""
