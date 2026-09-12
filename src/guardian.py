from src.filemanager import Function, TypeSpec
from typing import List, Dict, Tuple, Optional, Union
from pydantic import validate_call
import json

DIGITS = "0123456789"
QUOTE_MARKERS = ["~", "`", "_"]
BACKSLASH_MARKERS = ["^", "|", "<"]


class Guardian:
    """Constrained decoding for one function-call JSON reply.

    Injects the parts of the JSON skeleton that are already known
    (keys, punctuation, the prompt echo) and, for the parts the model
    has to write itself (the function name and each leaf value), tells
    the caller which token ids keep the result valid JSON conforming
    to the chosen function's schema — one prompt per session, started
    with ``start`` and driven with ``get_valid_ids``/``add_token``.
    """

    @validate_call
    def __init__(self, vocab: Dict[str, int],
                 reversed_vocab: Dict[int, str],
                 functions: List[Function]) -> None:
        """Set up an idle Guardian, with no session open yet.

        Args:
            vocab: Token string to id, from ``Tokenizer.get_vocab``.
            reversed_vocab: Token id to string, from
                ``Tokenizer.get_reversed_vocab``.
            functions: The function catalog whose schemas constrain
                every session's ``"parameters"``.
        """
        self._vocab: Dict[str, int] = vocab
        self._reversed_vocab: Dict[int, str] = reversed_vocab
        self._functions: Dict[str, Function] = {f.name: f for f in functions}
        self._json_str: str = ""
        self._stack: List[Tuple[Dict[str, TypeSpec], int]] = []
        self._slot: Optional[str] = None
        self._written: str = ""
        self._done: bool = True
        self._cache: Dict[Tuple[Optional[str],
                                Union[str, int], str], List[int]] = {}
        self.quote_marker: Union[str, None] = None
        self.backslash_marker: Union[str, None] = None

    @validate_call
    def start(self, prompt: str) -> None:
        """Open a new session for one prompt, resetting all state.

        Injects the fixed skeleton up to the opening of ``"name"``:
        the echoed prompt (with any ``"`` or ``\\`` it contains
        replaced by a one-character marker picked from
        ``QUOTE_MARKERS``/``BACKSLASH_MARKERS`` so the model never has
        to reproduce an escape sequence) and the start of the
        ``"name"`` value.

        Args:
            prompt: The raw user prompt for this session, as it will
                be echoed back in the reply's ``"prompt"`` field.
        """
        self.quote_marker = None
        self.backslash_marker = None
        masked_prompt = prompt
        if '"' in prompt:
            self.quote_marker = next(
                c for c in QUOTE_MARKERS if c not in prompt)
            masked_prompt = masked_prompt.replace('"', self.quote_marker)
        if "\\" in prompt:
            self.backslash_marker = next(
                c for c in BACKSLASH_MARKERS if c not in prompt)
            masked_prompt = masked_prompt.replace(
                "\\", self.backslash_marker)
        self._json_str = (
            '{"prompt":' +
            f"{json.dumps(masked_prompt)}"
            + ', "name": "')
        self._slot = "name"
        self._written = ""
        self._stack = []
        self._done = False

    def is_open(self) -> bool:
        """Return whether a session is running.

        True from ``start`` until the JSON it began is complete.
        """
        return not self._done

    def get_json(self) -> str:
        """Return the JSON built so far for the current session."""
        return self._json_str

    def get_written(self) -> str:
        """Return the raw text written by the model for the current slot."""
        return self._written

    def _closing_char(self) -> str:
        """Return the punctuation that closes the current stack level.

        Returns:
            ``","`` if the object on top of ``self._stack`` still has
            keys after the current one, ``"}"`` if it's the last key.
        """
        current_object: Dict[str, TypeSpec] = {}
        current_index: int = 0
        current_object, current_index = self._stack[-1]
        if current_index != len(current_object) - 1:
            return ","
        return "}"

    @staticmethod
    def _has_closing_quote(text: str) -> bool:
        """Return whether a string slot's value is already closed.

        Scans for a ``"`` not preceded by an odd number of
        backslashes — an escaped ``\\"`` doesn't count as closing.

        Args:
            text: The raw text written so far for a string slot.

        Returns:
            Whether ``text`` already contains its closing quote.
        """
        backslashes: int = 0
        for char in text:
            if char == "\\":
                backslashes += 1
                continue
            if char == '"' and backslashes % 2 == 0:
                return True
            backslashes = 0
        return False

    def _char_ok(self, text: str, candidate2add: str) -> bool:
        """Whitelist a single character against the current slot's grammar.

        The rule depends on ``self._slot``: a function name only
        grows towards a real catalog name (or closes with ``"`` once
        it already is one); a number/integer/float accepts an
        optional leading ``-``, its digits, at most one ``.`` after a
        digit (only for ``number``/``float``), and closes on the
        stack's closing char once a digit was written; a boolean only
        grows towards ``"true"``/``"false"`` and closes the same way;
        any other slot is a plain string — anything above byte 31 is
        allowed while unclosed, ``"`` closes it (if not already
        closed by an earlier unescaped quote), and the stack's closing
        char is only valid once it's closed.

        Args:
            text: The raw text written so far for the current slot.
            candidate2add: The single character being considered as
                the next one.

        Returns:
            Whether appending ``candidate2add`` to ``text`` keeps the
            value a valid, in-progress instance of the current slot.
        """
        match self._slot:
            case "name":
                if any(
                    function_name.startswith(text + candidate2add)
                    for function_name in self._functions
                ):
                    return True
                elif any(
                    function_name == text
                    for function_name in self._functions
                ) and candidate2add == '"':
                    return True
            case "number" | "integer" | "float":
                digits_part = text[1:] if text.startswith("-") else text
                if (self._slot in ("number", "float") and digits_part
                        and all(c in DIGITS for c in digits_part)
                        and candidate2add == "."):
                    return True
                elif not text and candidate2add == "-":
                    return True
                elif candidate2add in DIGITS and text not in ("0", "-0"):
                    return True
                elif (candidate2add == self._closing_char()
                      and (text and text[-1] in DIGITS)):
                    return True
            case "boolean":
                if ("true".startswith(text + candidate2add)
                        or "false".startswith(text + candidate2add)):
                    return True
                elif (text in ("true", "false")
                        and candidate2add == self._closing_char()):
                    return True
            case _:
                closed: bool = self._has_closing_quote(text)
                if candidate2add == '"' and not closed:
                    return True
                elif closed and self._closing_char() == candidate2add:
                    return True
                elif not closed and ord(candidate2add) > 31:
                    return True
        return False

    def _slot_closed(self, text: str) -> bool:
        """Return whether the current slot's value is already complete.

        Args:
            text: The raw text written so far for the current slot.

        Returns:
            Whether ``text`` is a finished value for ``self._slot``:
            an ending quote for ``"name"``, the stack's closing char
            for a number/integer/boolean/float, or an unescaped
            closing quote followed by that same closing char for any
            other (string) slot.
        """
        if not text:
            return False
        if self._slot == "name":
            return text.endswith('"')
        if self._slot in ("number", "integer", "boolean", "float"):
            return text[-1] == self._closing_char()
        return (self._has_closing_quote(text)
                and text[-1] == self._closing_char())

    def _token_ok(self, token_text: str) -> bool:
        """Whitelist a whole candidate token against the current slot.

        Replays ``_char_ok`` character by character over a draft that
        starts at ``self._written``, rejecting the token as soon as
        the slot would already be closed or a character would break
        the grammar.

        Args:
            token_text: The vocabulary string of the candidate token.

        Returns:
            Whether adding ``token_text`` in full keeps the current
            slot's value valid.
        """
        draft: str = self._written
        for char in token_text:
            if self._slot_closed(draft):
                return False
            if not self._char_ok(draft, char):
                return False
            draft += char
        return True

    def _cache_flags(self) -> int:
        """Bucket ``self._written`` into the states that share a whitelist.

        Used to build the cache key in ``get_valid_ids`` for
        number/integer/float and string slots, where the exact text
        written so far doesn't matter for which ids are valid next —
        only which bucket it falls in (nothing written yet, ``"0"``/
        ``"-0"``, ends in a digit with or without a ``.`` already
        seen, ends in ``.``, or — for a string — already has its
        closing quote).

        Returns:
            The bucket number for the current ``self._written``, or
            ``0`` if none of the buckets apply.
        """
        match self._slot:
            case "number" | "integer" | "float":
                if not self._written:
                    return 1
                elif self._written in ("0", "-0"):
                    return 2
                elif "." in self._written and self._written[-1].isdigit():
                    return 3
                elif self._written[-1].isdigit():
                    return 4
                elif self._written[-1].endswith("."):
                    return 5
            case _:
                if self._has_closing_quote(self._written):
                    return 1
        return 0

    def get_valid_ids(self) -> List[int]:
        """Return the token ids valid as the current slot's next piece.

        Consults ``self._cache`` first, keyed by slot, its
        ``_cache_flags``/``self._written`` bucket, and the stack's
        closing char — every id in the vocabulary is only ever
        checked with ``_token_ok`` once per distinct state.

        Returns:
            The token ids whose text keeps the current slot's value
            valid.

        Raises:
            ValueError: No session is open (``start`` wasn't called,
                or the previous one already finished).
        """
        if self._done:
            raise ValueError("Guardian has no open session. Call start first")
        close: str = ('"' if self._slot == "name" else self._closing_char())
        flag: Union[str, int] = (
            self._written if self._slot in ("name", "boolean")
            else self._cache_flags())
        current_state: Tuple[Optional[str], Union[str, int], str] = (
            self._slot, flag, close)
        if posible_cache := self._cache.get(current_state, []):
            return posible_cache
        else:
            self._cache[current_state] = [
                token_id
                for token_text, token_id in self._vocab.items()
                if self._token_ok(token_text)
            ]
        return self._cache[current_state]

    def _open_key(self) -> None:
        """Inject the next parameter key and open its value.

        Writes ``"key": `` for the key at the current index of the
        object on top of ``self._stack``. If that key's type is a
        nested object, opens its ``{`` and recurses into it with a
        fresh stack level starting at index 0. Otherwise sets
        ``self._slot`` to the key's type and, unless it's a bare
        literal type (number/integer/boolean/float), opens the
        leading ``"`` of a string value.
        """
        node, index = self._stack[-1]
        key: str = list(node)[index]
        spec: TypeSpec = node[key]
        self._json_str += f'"{key}": '
        if spec.properties:
            self._json_str += "{"
            self._stack.append((spec.properties, 0))
            self._open_key()
            return
        self._slot = spec.type
        self._written = ""
        if spec.type not in ("number", "integer", "boolean", "float"):
            self._json_str += '"'

    def _close_level(self) -> None:
        """Close the current nesting level and move to what's next.

        Pops ``self._stack``. If that was the last level, closes the
        whole ``"parameters"`` object and marks the session done.
        Otherwise advances the parent level's index: if it still has
        keys left, injects ``, `` and opens the next one; if not,
        closes that level's ``}`` too and recurses up.
        """
        self._stack.pop()
        self._written = ""
        if not self._stack:
            self._json_str += "}"
            self._slot = None
            self._done = True
            return
        node, index = self._stack[-1]
        index += 1
        self._stack[-1] = (node, index)
        if index < len(node):
            self._json_str += ", "
            self._open_key()
            return
        self._json_str += "}"
        self._close_level()

    def _close_name(self) -> None:
        """Move from the resolved function name into its parameters.

        Looks up the now-closed name in ``self._functions``, injects
        ``, "parameters": {``, and either closes it right away (no
        parameters) or pushes the first stack level and opens its
        first key.
        """
        name: str = self._written[:-1]
        parameters: Dict[str, TypeSpec] = self._functions[name].parameters
        self._json_str += ', "parameters": {'
        self._written = ""
        if not parameters:
            self._json_str += "}}"
            self._slot = None
            self._done = True
            return
        self._stack.append((parameters, 0))
        self._open_key()

    @validate_call
    def add_token(self, token_id: int) -> None:
        """Feed the model's chosen token into the current session.

        Appends the token's text to the JSON and to the current
        slot's written text. While filling the function name, closes
        it and moves on to its parameters as soon as ``self._written``
        ends in ``"`` — with a shortcut that auto-completes the name
        as soon as only one catalog candidate still matches, injecting
        the rest of it directly. For any other slot, once
        ``_slot_closed`` says the value is complete, either advances
        to the next key (when it closed on a comma) or closes the
        current nesting level.

        Args:
            token_id: The id the model chose from the ids returned by
                the last ``get_valid_ids`` call.

        Raises:
            ValueError: No session is open, or ``token_id`` isn't in
                the vocabulary.
        """
        if self._done:
            raise ValueError("Guardian has no open session. Call start first")
        if token_id not in self._reversed_vocab:
            raise ValueError(f"Token id {token_id} is not in the vocabulary")
        token_text: str = self._reversed_vocab[token_id]
        self._json_str += token_text
        self._written += token_text
        if self._slot == "name":
            if self._written.endswith('"'):
                self._close_name()
                return
            candidates = [
                name for name in self._functions
                if name.startswith(self._written)
            ]
            if self._written and len(candidates) == 1:
                remainder = candidates[0][len(self._written):]
                self._json_str += remainder + '"'
                self._written = candidates[0] + '"'
                self._close_name()
            return
        if not self._slot_closed(self._written):
            return
        if self._written[-1] == ",":
            node, index = self._stack[-1]
            self._stack[-1] = (node, index + 1)
            self._open_key()
        else:
            self._close_level()
