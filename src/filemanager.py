from typing import Dict, List, Optional, Union
from pathlib import Path
from pydantic import validate_call, FilePath, BaseModel
from pydantic import ConfigDict, TypeAdapter, ValidationError
import json


class Prompt(BaseModel):
    model_config = ConfigDict(extra="forbid")
    prompt: str


class TypeSpec(BaseModel):
    type: str
    properties: Optional[Dict[str, "TypeSpec"]] = None


class Function(BaseModel):
    name: str
    description: str
    parameters: Dict[str, TypeSpec]
    returns: TypeSpec


class FileManager:
    @validate_call
    def __init__(self, functions_path: FilePath,
                 prompts_path: FilePath,
                 output_path: Path) -> None:
        self._logs: Dict[str, List[Dict[str, str]]] = {
            "prompts": [], "files": []}
        self._functions: List[Function] = []
        self._prompts: List[Prompt] = []
        self._load_json(prompts_path, "prompts")
        self._load_json(functions_path, "functions")
        self._n_logs: int = 0
        self._n_replies: int = 0
        self._replies: List[Dict[str, Union[str, Dict[str, str | float]]]] = []
        if output_path.suffix == ".json":
            self._output_path: Path = Path(output_path)
            self._output_path.parent.mkdir(parents=True, exist_ok=True)
        else:
            raise ValueError("Empty or wrong output path in FileManager")

    def _load_json(self, path: FilePath, flag: str) -> None:
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
        if (self._logs["prompts"] or self._logs["files"]) and not self._n_logs:
            log_path: Path = Path("logs/logs.json")
            log_path.parent.mkdir(parents=True, exist_ok=True)
            with open(log_path, "w", encoding="utf-8") as archivo:
                json.dump(self._logs, archivo, ensure_ascii=False, indent=4)
            self._n_logs = 1

    def charge_replies(
            self, reply:
            Dict[str, Union[str, Dict[str, str | float]]]) -> None:
        self._replies.append(reply)

    def write_replies(self) -> None:
        if not self._n_replies:
            with open(self._output_path, "w", encoding="utf-8") as archivo:
                json.dump(self._replies, archivo, ensure_ascii=False, indent=4)
            self._n_replies = 1

    def get_logs(self) -> Dict[str, List[Dict[str, str]]]:
        return self._logs

    def get_functions(self) -> List[Function]:
        return self._functions

    def get_prompts(self) -> List[Prompt]:
        return self._prompts
