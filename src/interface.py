from .promptbuilder import PromptBuilder
from .tokenizer import Tokenizer
from .guardian import Guardian
from typing import List, Callable, Dict, Union
from .filemanager import Function
from pathlib import Path
from .filemanager import TypeSpec
from pydantic import validate_call, FilePath, BaseModel
import numpy as np
import numpy.typing as npt
import json

type ParamValue = Union[str, float, Dict[str, "ParamValue"]]


class Output(BaseModel):
    log: str
    output: ParamValue


class Interface:
    @validate_call
    def __init__(self, functions: List[Function],
                 vocab_path: FilePath,
                 merges_path: FilePath,
                 tokenizer_path: FilePath,
                 logits_method: Callable[[List[int]], List[float]]) -> None:
        self._functions: Dict[str, Function] = {f.name: f for f in functions}
        self._prompt_builder: PromptBuilder = PromptBuilder(functions)
        self._get_model_logits: Callable[
            [List[int]], List[float]] = logits_method
        self._tokenizer: Tokenizer = Tokenizer(
            Path(vocab_path),
            Path(merges_path),
            Path(tokenizer_path))
        self._guardian: Guardian = Guardian(
            self._tokenizer.get_vocab(),
            self._tokenizer.get_reversed_vocab(),
            functions)

    def _costume_translater(
            self, parameters:
            Dict[str, ParamValue]) -> Dict[str, ParamValue]:
        for parameter, leaf in parameters.items():
            if isinstance(leaf, str):
                parameters[parameter] = bytearray(
                    self._tokenizer.char_byte[char]
                    for char in leaf).decode("utf-8")
            if isinstance(leaf, Dict):
                parameters[parameter] = self._costume_translater(leaf)
        return parameters

    def _valid_parameters(
            self,
            function: Union[Function, Union[Dict[str, TypeSpec], None]],
            parameters: Dict[str, ParamValue]) -> Dict[str, ParamValue]:
        error_return: Dict[str, ParamValue] = {
            "ERROR": "processed function doesn't match "
            "the function parameters"}
        function_parameters: Union[Function,
                                   Union[Dict[str, TypeSpec], None]] = {}
        if isinstance(function, Function):
            function_parameters = function.parameters
        else:
            function_parameters = function
        if function_parameters is not None:
            for key, value in parameters.items():
                if function_parameters[key].type == "number":
                    if not (isinstance(value, int)
                            or isinstance(value, float)):
                        return error_return
                elif (function_parameters[key].type == "string"
                        and not isinstance(value, str)):
                    return error_return
                elif (function_parameters[key].properties
                        and isinstance(value, Dict)):
                    nested_result = self._valid_parameters(
                        function_parameters[key].properties, value)
                    if "ERROR" in nested_result:
                        return error_return
                elif (function_parameters[key].properties
                        and not isinstance(value, Dict)):
                    return error_return
        return parameters

    @validate_call
    def reply(self, user_prompt: str) -> Output:
        if not user_prompt or len(user_prompt) < 1:
            return Output(
                log="The prompt was empty",
                output={"prompt": user_prompt})
        function_name: str = ""
        response_formated: Dict[str, ParamValue] = {}
        system_prompt: str = (
            self._prompt_builder.get_prompt(user_prompt))
        tokenized_prompt: List[int] = []
        self._guardian.start(user_prompt)
        whith_list: List[int] = []
        token_selected: int = 0
        limit: Callable[[], bool] = (
            lambda: len(self._guardian.get_written())
            <= len(user_prompt))
        while self._guardian.is_open() and limit():
            tokenized_prompt = (
                self._tokenizer.encode(
                    system_prompt + self._guardian.get_json()))
            whith_list = self._guardian.get_valid_ids()
            try:
                model_logits: npt.NDArray[np.float64] = (
                    np.array(self._get_model_logits(tokenized_prompt)))
            except Exception:
                return Output(
                    log="Model failed while replying",
                    output={"prompt": user_prompt})
            clean_logits: npt.NDArray[np.float64] = (
                np.full(len(model_logits), -np.inf))
            clean_logits[whith_list] = model_logits[whith_list]
            token_selected = int(np.argmax(clean_logits))
            self._guardian.add_token(token_selected)
        if not limit():
            return Output(
                log="Model entered an loop",
                output={"prompt": user_prompt})
        response_formated = json.loads(self._guardian.get_json())
        if isinstance(response_formated["parameters"], Dict):
            if isinstance(response_formated["name"], str):
                function_name = response_formated["name"]
            response_formated["parameters"] = self._valid_parameters(
                self._functions[function_name],
                self._costume_translater(
                    response_formated["parameters"]))
            if "ERROR" in response_formated["parameters"]:
                return Output(
                    log=str(response_formated["parameters"]["ERROR"]),
                    output={"prompt": user_prompt})
            return Output(
                log="The prompt was replied correctly",
                output=response_formated)
        else:
            return Output(
                log="Model produced malformed parameters",
                output={"prompt": user_prompt})
