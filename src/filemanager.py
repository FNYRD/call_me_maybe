from typing import Dict, List, Optional, TYPE_CHECKING
from pathlib import Path
from pydantic import validate_call, FilePath, BaseModel
from pydantic import ConfigDict, TypeAdapter, ValidationError
import json

if TYPE_CHECKING:
    from .interface import ParamValue


class Prompt(BaseModel):
    """One entry of ``function_calling_tests.json``: a single prompt.

    Rejects any key other than ``prompt``.
    """

    model_config = ConfigDict(extra="forbid")
    prompt: str


class TypeSpec(BaseModel):
    """The type of a function parameter or return value.

    ``properties`` is only present when ``type`` describes a nested
    object, and each of its values is itself a ``TypeSpec`` — this is
    what lets a parameter be nested arbitrarily deep.
    """

    type: str
    properties: Optional[Dict[str, "TypeSpec"]] = None


class Function(BaseModel):
    """One entry of ``functions_definition.json``: a callable function.

    Its parameters are keyed by name, each with its own ``TypeSpec``.
    """

    name: str
    description: str
    parameters: Dict[str, TypeSpec]
    returns: TypeSpec


class FileManager:
    """Reads and validates the input files, and writes the output ones.

    Owns the two JSON files the subject requires (prompts and function
    catalog) as validated pydantic models, plus the logs and replies
    accumulated while the rest of the project runs.
    """

    @validate_call
    def __init__(self, functions_path: FilePath,
                 prompts_path: FilePath,
                 output_path: Path) -> None:
        """Load and validate both input files, and prepare the output path.

        Args:
            functions_path: Path to ``functions_definition.json``.
            prompts_path: Path to ``function_calling_tests.json``.
            output_path: Where ``write_replies`` will write the
                results. Must end in ``.json``.

        Raises:
            ValueError: ``output_path`` doesn't end in ``.json``, or
                either input file is missing, corrupt, empty, or has
                the wrong shape.
        """
        self._logs: Dict[str, List[Dict[str, str]]] = {
            "prompts": [], "files": []}
        self._functions: List[Function] = []
        self._prompts: List[Prompt] = []
        self._load_json(prompts_path, "prompts")
        self._load_json(functions_path, "functions")
        self._n_logs: int = 0
        self._n_replies: int = 0
        self._replies: List["Dict[str, ParamValue]"] = []
        if output_path.suffix == ".json":
            self._output_path: Path = Path(output_path)
            self._output_path.parent.mkdir(parents=True, exist_ok=True)
        else:
            raise ValueError("Empty or wrong output path in FileManager")

    def _load_json(self, path: FilePath, flag: str) -> None:
        """Load one input file into ``self._prompts`` or ``self._functions``.

        Args:
            path: Path to the JSON file to load.
            flag: Which file this is — ``"prompts"`` validates against
                ``Prompt``, ``"functions"`` against ``Function``.

        Raises:
            ValueError: The JSON is corrupt, doesn't match the
                expected shape, or (for ``"functions"``) is empty.
        """
        try:
            with open(path, "r", encoding="utf-8") as file:
                if flag == "prompts":
                    self._prompts = TypeAdapter(
                        List[Prompt]).validate_python(json.load(file))
                elif flag == "functions":
                    self._functions = TypeAdapter(
                        List[Function]).validate_python(json.load(file))
                    if not len(self._functions):
                        raise ValueError("Function's file is empty")
        except json.JSONDecodeError as error:
            raise ValueError(f"Corrupt JSON in {path}") from error
        except ValidationError:
            raise ValueError(
                "Prompt's or Function's file have a wrong format")
        except ValueError as e:
            raise ValueError(e)

    def charge_logs(self, error: str, content: str, category: str) -> None:
        """Accumulate one failure entry, to be written by ``write_logs``.

        Args:
            error: The key under which ``content`` is recorded (e.g.
                the error message).
            content: The value logged for ``error``.
            category: Which log this belongs to — must be an existing
                key of the logs (``"prompts"`` or ``"files"``).

        Raises:
            ValueError: ``category`` isn't a valid log key, or any of
                ``error``, ``content``, ``category`` is empty.
        """
        if category not in self._logs:
            raise ValueError(
                f"The category: {category} it's not a valid key log")
        if not error or not content or not category:
            raise ValueError(
                f"Empty error: {error} or content: "
                f"{content} or category: {category} it's"
                " a wrong format to write logs")
        self._logs[category].append({error: content})

    def write_logs(self) -> None:
        """Write the accumulated logs to ``logs/logs.json``, once.

        Does nothing if nothing was ever logged, or if this method
        already wrote the file.
        """
        if (self._logs["prompts"] or self._logs["files"]) and not self._n_logs:
            log_path: Path = Path("logs/logs.json")
            log_path.parent.mkdir(parents=True, exist_ok=True)
            with open(log_path, "w", encoding="utf-8") as file:
                json.dump(self._logs, file, ensure_ascii=False, indent=4)
            self._n_logs = 1

    def charge_replies(
            self, reply:
            "Dict[str, ParamValue]") -> None:
        """Accumulate one reply, to be written by ``write_replies``.

        Args:
            reply: One already-built result object for the output
                file (``prompt``, ``name`` and ``parameters``).
        """
        self._replies.append(reply)

    def write_replies(self) -> None:
        """Write the accumulated replies to the output path, once.

        Does nothing if this method already wrote the file.
        """
        if not self._n_replies:
            with open(self._output_path, "w", encoding="utf-8") as file:
                json.dump(self._replies, file, ensure_ascii=False, indent=4)
            self._n_replies = 1

    def get_logs(self) -> Dict[str, List[Dict[str, str]]]:
        """Return the logs accumulated so far, by category."""
        return self._logs

    def get_functions(self) -> List[Function]:
        """Return the validated function catalog loaded at construction."""
        return self._functions

    def get_prompts(self) -> List[Prompt]:
        """Return the validated prompts loaded at construction."""
        return self._prompts
