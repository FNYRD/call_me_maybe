from pydantic import validate_call, FilePath, ValidationError
from pathlib import Path
from typing import List, Callable
from .filemanager import FileManager

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



    # Lista de requisitos - cerrada el 2026-09-03, actualizada el 2026-09-05
    # PROJECT.md#Bloque 6 - `Chat` orquestador
    #
    # Que debe hacer
    # - [X] Recibir las tres rutas de datos de src/__main__.py. Chat no hace argparse
    # - [X] Recibir las tres rutas del modelo y la funcion de logits ya
    #       extraidas de src/__main__.py - Chat ya no construye el SDK
    # - [X] Construir FileManager con ellas
    # - [ ] Construir Interface con el catalogo, las rutas y esa funcion
    # - [ ] Recorrer los N prompts, uno por llamada a reply
    # - [ ] Acumular con charge_replies y escribir con write_replies
    # - [ ] Registrar los fallos con charge_logs y escribir con write_logs
    #
    # Que debe rechazar
    # - [ ] FileManager lanza al construirse (ruta ausente, JSON corrupto,
    #       catalogo vacio) -> revertido el 09-05: NO lo atrapa Chat, lo
    #       atrapa src/__main__.py alrededor de la construccion de Chat.
    #       Chat deja pasar la excepcion sin try/except propio
    # - [ ] Un prompt vuelve con un log de fallo (incluido cualquier fallo de
    #       json.loads o de validacion, que ocurren dentro de Interface) ->
    #       el objeto de salida es {"prompt": "...", "ERROR": "<el log>"} y
    #       se registra en prompts con su indice. El ERROR es el log de
    #       Interface, copiado tal cual
    #
    # Que NO es suyo
    # - argparse -> src/__main__.py
    # - Construir Small_LLM_Model y sacarle las rutas y la funcion de logits
    #   -> src/__main__.py
    # - Atrapar el fallo de FileManager al construirse y escribir logs.json
    #   -> src/__main__.py, revertido el 09-05
    # - Generar, traducir las hojas y validar tipos -> Interface, Bloque 5
    # - Las reglas de formato JSON -> Guardian, Bloque 4
    # - Abrir archivos, salvo el log de rutas fallidas -> FileManager, Bloque 2
