from typing import Dict, List, Union, Optional
from pathlib import Path
from pydantic import validate_call, FilePath, BaseModel, ConfigDict, TypeAdapter, ValidationError
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
        self._logs: Dict[str, Dict[str, str]] = {"prompts": {}, "files": {}}
        self._functions: List[Function] = []
        self._prompts: List[Prompt] = []
        self._load_json(prompts_path, "prompts")
        self._load_json(functions_path, "functions")
        if output_path: #REVISAR ESTO PORQUE SOLO SE CREA EN CASO DE ERROR NO SIEMPRE
            self._output_path: Path = Path(output_path)
            self._output_path.parent.mkdir(parents=True, exist_ok=True)
        else:
            raise ValueError("Empty output path in FileManager")

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
