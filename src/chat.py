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
    """Orchestrates the whole run: every prompt through, results and logs out.

    Builds the ``FileManager`` (I/O) and ``Interface`` (per-prompt
    generation) from the files and callable the SDK provides, then
    ``chatting`` drives all of them through the pipeline in one pass.
    """

    @validate_call
    def __init__(self, functions_path: FilePath,
                 prompts_path: FilePath,
                 output_path: Path,
                 vocab_path: FilePath,
                 merges_path: FilePath,
                 tokenizer_path: FilePath,
                 logits_method: Callable[[List[int]], List[float]]) -> None:
        """Load the inputs and build the pieces ``chatting`` will drive.

        Adds ``UNKNOWN_FUNCTION`` to the loaded catalog before it
        reaches ``Interface``, so the model has an escape hatch when
        no real function fits a prompt.

        Args:
            functions_path: Path to ``functions_definition.json``,
                passed to ``FileManager``.
            prompts_path: Path to ``function_calling_tests.json``,
                passed to ``FileManager``.
            output_path: Where the results will be written, passed to
                ``FileManager``.
            vocab_path: Path to ``vocab.json``, passed to ``Interface``.
            merges_path: Path to ``merges.txt``, passed to ``Interface``.
            tokenizer_path: Path to ``tokenizer.json``, passed to
                ``Interface``.
            logits_method: The SDK's ``get_logits_from_input_ids``,
                passed to ``Interface``.
        """
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
        """Run every loaded prompt through ``Interface`` and write the results.

        For each prompt: gets a reply, and if the SDK itself failed
        (``"Model failed while replying"``), retries up to 3 more
        times looking for a well-formed one (bonus 3's error
        recovery). A well-formed reply (``prompt``, ``name`` and
        ``parameters``) is queued for the output file; any other
        outcome is queued both as a ``"prompts"`` log entry and as an
        ``{"prompt", "ERROR"}`` reply, so every input prompt still
        gets one output entry. Writes the logs and the replies once
        the whole pass is done.
        """
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
