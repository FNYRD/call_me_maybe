from pydantic import validate_call, FilePath
from pathlib import Path
from typing import List, Callable, Dict, Any
from .filemanager import FileManager, Function, TypeSpec
from .interface import Interface, Output

UNKNOWN_FUNCTION = Function(
    name="fn_unknown",
    description="Used when the prompt does not match any other function.",
    parameters={},
    returns=TypeSpec(type="string"))


class Chat:
    @validate_call
    def __init__(self, functions_path: FilePath,
                 prompts_path: FilePath,
                 output_path: Path,
                 vocab_path: FilePath,
                 merges_path: FilePath,
                 tokenizer_path: FilePath,
                 logits_method: Callable[[List[int]], List[float]]) -> None:
        self._file_manager: FileManager = FileManager(
            functions_path, prompts_path, output_path)
        functions: List[Function] = (
            self._file_manager.get_functions() + [UNKNOWN_FUNCTION])
        self._interface: Interface = Interface(
            functions, vocab_path, merges_path, tokenizer_path,
            logits_method)
        self._prompts: List[str] = [
            prompt.prompt for prompt in self._file_manager.get_prompts()]

    def chatting(self) -> None:
        answer: Output
        log_answer: str = ""
        value: Any = ""
        well_processed: Callable[
            [Output], bool] = lambda answer: isinstance(
                answer.output, Dict) and len(answer.output) == 3
        for prompt in self._prompts:
            answer = self._interface.reply(prompt)
            if answer.log == "Model failed while replying":
                for i in range(3):
                    answer = self._interface.reply(prompt)
                    if well_processed(answer):
                        break
            if isinstance(answer.output, Dict) and len(answer.output) == 3:
                self._file_manager.charge_replies(answer.output)
            else:
                if isinstance(answer.output, Dict):
                    value = next(iter(answer.output.values()))
                    if isinstance(value, str):
                        log_answer = value
                        self._file_manager.charge_logs(
                            answer.log, log_answer, "prompts")
                        self._file_manager.charge_replies(
                            {"prompt": prompt, "ERROR": answer.log})
        self._file_manager.write_logs()
        self._file_manager.write_replies()
