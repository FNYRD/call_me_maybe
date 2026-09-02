from .promptbuilder import PromptBuilder
from .tokenizer import Tokenizer
from .guardian import Guardian
from typing import List, Callable
from .filemanager import Function
from pathlib import Path
from pydantic import validate_call, FilePath
import numpy as np
import numpy.typing as npt, array

class Interface:
    @validate_call
    def __init__(self, functions: List[Function],
                 vocab_path: FilePath,
                 merges_path: FilePath,
                 tokenizer_path: FilePath,
                 logits_method: Callable[[List[int]], List[float]]) -> None:
        self._prompt_builder: PromptBuilder = PromptBuilder(functions)
        self._get_model_logits: Callable[[List[int]], List[float]] = logits_method
        self._tokenizer: Tokenizer = Tokenizer(
            Path(vocab_path),
            Path(merges_path),
            Path(tokenizer_path))
        self._guardian: Guardian = Guardian(
            self._tokenizer.get_vocab(),
            self._tokenizer.get_reversed_vocab(),
            functions)

    def reply(self, user_prompt: str) -> str:
        if not user_prompt or len(user_prompt) < 1:
            return "" # adaptar a pydantic
        system_prompt: str = (
            self._prompt_builder.get_prompt(user_prompt))
        tokenized_prompt: List[int] =  []
        self._guardian.start(user_prompt)
        whith_list: List[int] = []
        token_selected: int = 0
        while self._guardian.is_open() and len(self._guardian.get_written()) <= len(user_prompt):
            tokenized_prompt = (
                self._tokenizer.encode(system_prompt
                + self._guardian.get_json()))
            whith_list = self._guardian.get_valid_ids()
            model_logits: npt.NDArray[np.float64] = (
                np.array(self._get_model_logits(tokenized_prompt)))
            clean_logits: npt.NDArray[np.float64] = (
                np.full(len(model_logits), -np.inf))
            clean_logits[whith_list] = model_logits[whith_list]
            token_selected = int(np.argmax(clean_logits))
            self._guardian.add_token(token_selected)
        return "" #provicional
            



    
