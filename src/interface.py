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
import re

type ParamValue = Union[str, int, float, bool, Dict[str, "ParamValue"]]

_CASE_KEYWORDS = ("uppercase", "lowercase", "capitalize",
                  "upper case", "lower case", "title case")


class Output(BaseModel):
    """The result of one ``Interface.reply`` call.

    ``log`` says what happened to the prompt (success or which way it
    failed); ``output`` is either the full ``{"prompt", "name",
    "parameters"}`` result on success, or just ``{"prompt": ...}`` on
    any failure.
    """

    log: str
    output: ParamValue


class Interface:
    """Turns one raw prompt into a validated function call, or a failure log.

    Owns the pipeline a single prompt goes through: build the chat
    prompt (``PromptBuilder``), tokenize it (``Tokenizer``), and drive
    constrained decoding (``Guardian``) token by token against the
    model's logits, then validate and clean up what the model wrote.
    """

    @validate_call
    def __init__(self, functions: List[Function],
                 vocab_path: FilePath,
                 merges_path: FilePath,
                 tokenizer_path: FilePath,
                 logits_method: Callable[[List[int]], List[float]]) -> None:
        """Build the prompt builder, tokenizer and guardian for this catalog.

        Args:
            functions: The function catalog every prompt is answered
                against.
            vocab_path: Path to ``vocab.json``, passed to ``Tokenizer``.
            merges_path: Path to ``merges.txt``, passed to ``Tokenizer``.
            tokenizer_path: Path to ``tokenizer.json``, passed to
                ``Tokenizer``.
            logits_method: The SDK's ``get_logits_from_input_ids``,
                called once per generated token in ``reply``.
        """
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

    @staticmethod
    def _apply_case_pattern(text: str, sample: str) -> str:
        """Recase ``text`` to match the case pattern of ``sample``.

        Looks only at ``sample``'s first three characters: all
        uppercase, first-upper-rest-lower, or all lowercase. Anything
        else (too short, alternating case) is left untouched, since
        the pattern can't be told apart reliably.

        Args:
            text: The literal text to recase (a quoted span pulled
                from the prompt).
            sample: The model's own generated value, whose case
                pattern ``text`` should follow.

        Returns:
            ``text`` recased to match ``sample``'s pattern, or
            unchanged if the pattern isn't recognized.
        """
        prefix: str = sample[:3]
        if len(prefix) < 3:
            return text
        if prefix.isupper():
            return text.upper()
        if prefix[0].isupper() and prefix[1:].islower():
            return text[:1].upper() + text[1:].lower()
        if prefix.islower():
            return text.lower()
        return text

    def _copy_from_prompt(
            self, value: str, user_prompt: str, description: str) -> str:
        """Restore a value the model meant to copy verbatim from the prompt.

        If ``value`` matches, ignoring case and spaces, exactly one
        quoted span in ``user_prompt``, the model was almost certainly
        copying that span and lost a separator or mangled a letter's
        case along the way. When the function's own description
        doesn't call for a case change, the literal span replaces
        ``value`` outright. When it does (an uppercase/lowercase/
        capitalize transform), the span is recased to follow whatever
        pattern the model was already writing, instead of overwriting
        an intentional transform.

        Args:
            value: The already byte-translated string leaf.
            user_prompt: The prompt this leaf was generated from.
            description: The chosen function's description, used to
                tell a literal copy from a case-changing transform.

        Returns:
            The corrected value, or ``value`` unchanged if none or
            more than one quoted span matches.
        """
        spans: List[str] = re.findall(r"'([^']*)'", user_prompt)
        target: str = value.lower().replace(" ", "")
        matches: List[str] = [
            span for span in spans
            if span.lower().replace(" ", "") == target]
        if len(matches) != 1:
            return value
        if any(keyword in description.lower()
                for keyword in _CASE_KEYWORDS):
            return self._apply_case_pattern(matches[0], value)
        return matches[0]

    def _costume_translater(
            self, parameters: Dict[str, ParamValue],
            user_prompt: str, description: str) -> Dict[str, ParamValue]:
        """Translate every string leaf from its disguised bytes to real text.

        Each character the model wrote for a string slot is a
        visible-character disguise of a raw byte (see ``Tokenizer``'s
        byte↔char table). This reverses that with ``char_byte``, folds
        the vocabulary's own space-glyph mojibake (bytes 196, 160)
        back into a real space, strips a stray leading/trailing space
        left by that same glyph at a value's edge, and restores a
        value the model meant to copy verbatim from the prompt (see
        ``_copy_from_prompt``). Recurses into nested objects so every
        leaf gets translated.

        Args:
            parameters: The ``"parameters"`` dict as parsed from the
                model's raw JSON, disguised strings included.
            user_prompt: The prompt this call's parameters were
                generated from.
            description: The chosen function's description.

        Returns:
            The same dict, with every string leaf translated in place.
        """
        for parameter, leaf in parameters.items():
            if isinstance(leaf, str):
                translated = bytearray(
                    self._tokenizer.char_byte[char]
                    for char in leaf).replace(
                        bytes([196, 160]), bytes([32])
                        ).decode("utf-8").strip()
                parameters[parameter] = self._copy_from_prompt(
                    translated, user_prompt, description)
            if isinstance(leaf, Dict):
                parameters[parameter] = self._costume_translater(
                    leaf, user_prompt, description)
        return parameters

    def _valid_parameters(
            self,
            function: Union[Function, Union[Dict[str, TypeSpec], None]],
            parameters: Dict[str, ParamValue]) -> Dict[str, ParamValue]:
        """Check each parameter's Python type against its schema.

        Recurses into nested objects (``properties``), comparing each
        one's own keys against its own ``TypeSpec`` dict.

        Args:
            function: The chosen ``Function`` (top-level call) or the
                nested ``properties`` dict of a parent parameter
                (recursive call) that ``parameters`` is checked
                against.
            parameters: The (already byte-translated) parameters to
                validate.

        Returns:
            ``parameters`` unchanged if every value's type matches its
            schema, or ``{"ERROR": ...}`` at the first mismatch —
            wrong type for number/integer/string/boolean, an object
            expected but not given, or a mismatch found while
            recursing into a nested object.
        """
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
                if function_parameters[key].type in ("number", "float"):
                    if not (isinstance(value, int)
                            or isinstance(value, float)):
                        return error_return
                    if isinstance(value, int):
                        parameters[key] = float(value)
                elif (function_parameters[key].type == "integer"
                        and not isinstance(value, int)):
                    return error_return
                elif (function_parameters[key].type == "string"
                        and not isinstance(value, str)):
                    return error_return
                elif (function_parameters[key].type == "boolean"
                        and not isinstance(value, bool)):
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
        """Answer one prompt with a validated function call.

        Runs the full constrained-decoding loop for ``user_prompt``:
        starts a ``Guardian`` session, and while it's still open and
        under the character-count safety limit, retokenizes the
        growing prompt (system prompt + JSON built so far), asks the
        model for logits, masks everything outside the current
        whitelist to ``-inf``, greedily picks the highest-scoring
        allowed token, and feeds it back to the guardian. Once the
        JSON is complete, undoes the quote/backslash markers injected
        by ``Guardian.start``, parses it, and runs the result through
        ``_costume_translater`` and ``_valid_parameters``.

        Args:
            user_prompt: The natural-language prompt to answer.

        Returns:
            An ``Output`` with the full result on success, or a
            failure ``log`` (empty prompt, the model erroring out
            mid-generation, the character limit being hit without
            closing the JSON, or a validation failure) alongside just
            the echoed prompt.
        """
        if not user_prompt or len(user_prompt) < 1:
            return Output(
                log="Empty prompt",
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
        raw_json: str = self._guardian.get_json()
        if self._guardian.quote_marker is not None:
            raw_json = raw_json.replace(
                self._guardian.quote_marker, '\\"')
            self._guardian.quote_marker = None
        if self._guardian.backslash_marker is not None:
            raw_json = raw_json.replace(
                self._guardian.backslash_marker, "\\\\")
            self._guardian.backslash_marker = None
        response_formated = json.loads(raw_json)
        if isinstance(response_formated["parameters"], Dict):
            if isinstance(response_formated["name"], str):
                function_name = response_formated["name"]
            response_formated["parameters"] = self._valid_parameters(
                self._functions[function_name],
                self._costume_translater(
                    response_formated["parameters"], user_prompt,
                    self._functions[function_name].description))
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
