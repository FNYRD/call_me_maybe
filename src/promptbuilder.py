from src.filemanager import Function
from typing import List
from pydantic import TypeAdapter, validate_call

TEMPLATE_QWEN: str = (
    "<|im_start|>system\nYou have access to the following functions: "
    "{FUNCTION} and must answer to the prompt in the user section, "
    "in json format with the keys \"name\" for function's name and"
    " \"parameters\" for the expected parameters to execute the function"
    "<|im_end|>\n<|im_start|>user\n{PREGUNTA}<|im_end|>\n"
    "<|im_start|>assistant\n")


class PromptBuilder:
    @validate_call
    def __init__(self, functions: List[Function]) -> None:
        self._functions: List[Function] = functions
        self._functions_template: str = TypeAdapter(
            List[Function]).dump_json(
                self._functions, exclude_none=True).decode("utf-8")

    def get_prompt(self, prompt: str) -> str:
        return TEMPLATE_QWEN.format(
            FUNCTION=self._functions_template,
            PREGUNTA=prompt)
