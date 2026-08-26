"""Tests del Bloque 2 — `FileManager`.

Todo corre con archivos de juguete creados en un directorio temporal, salvo
un test que usa los archivos reales de `data/input/` del propio repositorio.
Ningun test necesita el modelo ni la red.
"""
import json
from pathlib import Path
from typing import Any, Dict, List

import pytest
from pydantic import ValidationError

from src.filemanager import FileManager, Function, Prompt

RAIZ = Path(__file__).resolve().parent.parent


# --------------------------------------------------------------------------
# Fabricas de archivos de juguete
# --------------------------------------------------------------------------

def escribir_json(ruta: Path, contenido: Any) -> Path:
    """Vuelca cualquier objeto a un `.json` y devuelve su ruta."""
    ruta.write_text(json.dumps(contenido), encoding="utf-8")
    return ruta


def catalogo() -> List[Dict[str, Any]]:
    """Catalogo plano, con la misma forma que el real pero mas corto."""
    return [
        {"name": "fn_add_numbers",
         "description": "Add two numbers together and return their sum.",
         "parameters": {"a": {"type": "number"}, "b": {"type": "number"}},
         "returns": {"type": "number"}},
        {"name": "fn_greet",
         "description": "Generate a greeting message for a person by name.",
         "parameters": {"name": {"type": "string"}},
         "returns": {"type": "string"}},
    ]


def prompts() -> List[Dict[str, str]]:
    """Prompts validos, con la unica clave que admite el modelo."""
    return [{"prompt": "What is the sum of 2 and 3?"},
            {"prompt": "Greet shrek"}]


@pytest.fixture
def rutas(tmp_path):
    """Las tres rutas ya escritas: catalogo, prompts y salida."""
    return (escribir_json(tmp_path / "functions.json", catalogo()),
            escribir_json(tmp_path / "prompts.json", prompts()),
            tmp_path / "salida" / "function_calling_results.json")


def construir(tmp_path, funciones=None, entradas=None,
              salida=None) -> FileManager:
    """Atajo: escribe los archivos y devuelve el `FileManager` construido."""
    return FileManager(
        escribir_json(tmp_path / "functions.json",
                      catalogo() if funciones is None else funciones),
        escribir_json(tmp_path / "prompts.json",
                      prompts() if entradas is None else entradas),
        (tmp_path / "salida" / "res.json") if salida is None else salida)


# --------------------------------------------------------------------------
# 1. Creacion correcta
# --------------------------------------------------------------------------

def test_construye_con_los_tres_archivos(rutas):
    """Con entradas validas, el constructor no lanza."""
    assert isinstance(FileManager(*rutas), FileManager)


def test_crea_la_carpeta_de_salida_si_no_existe(tmp_path):
    """Primera ejecucion: `data/output/` no existe y hay que crearla."""
    salida = tmp_path / "data" / "output" / "res.json"
    assert not salida.parent.exists()
    construir(tmp_path, salida=salida)
    assert salida.parent.is_dir()


def test_construir_dos_veces_no_falla(tmp_path):
    """Segunda ejecucion: la carpeta ya existe y no puede reventar."""
    salida = tmp_path / "data" / "output" / "res.json"
    construir(tmp_path, salida=salida)
    construir(tmp_path, salida=salida)
    assert salida.parent.is_dir()


def test_los_prompts_quedan_como_objetos_del_modelo(rutas):
    """Lo que entrega el bloque es `Prompt`, no `dict`: se lee `.prompt`."""
    manager = FileManager(*rutas)
    assert all(isinstance(p, Prompt) for p in manager.get_prompts())
    assert manager.get_prompts()[1].prompt == "Greet shrek"


def test_las_funciones_quedan_como_objetos_del_modelo(rutas):
    """Igual con el catalogo: `Function`, y los parametros son `TypeSpec`."""
    manager = FileManager(*rutas)
    assert all(isinstance(f, Function) for f in manager.get_functions())
    assert manager.get_functions()[0].name == "fn_add_numbers"
    assert manager.get_functions()[0].parameters["a"].type == "number"


def test_los_archivos_reales_del_repo_construyen(tmp_path):
    """Los de `data/input/` de verdad: 5 funciones y 11 prompts."""
    manager = FileManager(
        RAIZ / "data" / "input" / "functions_definition.json",
        RAIZ / "data" / "input" / "function_calling_tests.json",
        tmp_path / "res.json")
    assert len(manager.get_functions()) == 5
    assert len(manager.get_prompts()) == 11


# --------------------------------------------------------------------------
# 2. El catalogo — que acepta `Function` y que rechaza
# --------------------------------------------------------------------------

def test_catalogo_anidado_de_dos_niveles(tmp_path):
    """El bonus 7: un parametro que es un objeto con campos dentro."""
    anidado = [{"name": "fn_move",
                "description": "Move something.",
                "parameters": {"punto": {"type": "object",
                                         "properties": {
                                             "x": {"type": "number"},
                                             "y": {"type": "number"}}}},
                "returns": {"type": "string"}}]
    manager = construir(tmp_path, funciones=anidado)
    punto = manager.get_functions()[0].parameters["punto"]
    assert punto.properties["x"].type == "number"


def test_catalogo_anidado_de_tres_niveles(tmp_path):
    """`TypeSpec` se referencia a si mismo: no hay tope de profundidad."""
    anidado = [{"name": "fn_deep",
                "description": "Deep.",
                "parameters": {"a": {"type": "object", "properties": {
                    "b": {"type": "object", "properties": {
                        "c": {"type": "string"}}}}}},
                "returns": {"type": "string"}}]
    manager = construir(tmp_path, funciones=anidado)
    fondo = manager.get_functions()[0].parameters["a"]
    assert fondo.properties["b"].properties["c"].type == "string"


def test_catalogo_sin_description(tmp_path):
    """Falta un campo obligatorio del modelo: no se construye."""
    roto = [{"name": "fn_add_numbers",
             "parameters": {"a": {"type": "number"}},
             "returns": {"type": "number"}}]
    with pytest.raises(ValueError, match="wrong format"):
        construir(tmp_path, funciones=roto)


def test_catalogo_con_parametro_sin_type(tmp_path):
    """El fallo esta dentro de un `TypeSpec`, no en el primer nivel."""
    roto = [{"name": "fn_add_numbers",
             "description": "Add.",
             "parameters": {"a": {}},
             "returns": {"type": "number"}}]
    with pytest.raises(ValueError, match="wrong format"):
        construir(tmp_path, funciones=roto)


def test_catalogo_vacio(tmp_path):
    """Sin funciones no hay nada que elegir: es tu guard, no el de pydantic."""
    with pytest.raises(ValueError, match="Function's file is empty"):
        construir(tmp_path, funciones=[])


def test_catalogo_que_es_un_objeto_y_no_una_lista(tmp_path):
    """El archivo trae `{...}` donde se espera `[...]`."""
    with pytest.raises(ValueError, match="wrong format"):
        construir(tmp_path, funciones={"name": "fn_add_numbers"})


# --------------------------------------------------------------------------
# 3. Los prompts — la unica clave que admite `Prompt`
# --------------------------------------------------------------------------

def test_prompts_vacios_pasan(tmp_path):
    """0 prompts entran, 0 resultados salen: decidido sin guard."""
    manager = construir(tmp_path, entradas=[])
    assert manager.get_prompts() == []


def test_prompt_con_clave_de_mas(tmp_path):
    """`extra="forbid"`: sin el, esta entrada pasaria sin avisar."""
    with pytest.raises(ValueError, match="wrong format"):
        construir(tmp_path, entradas=[{"prompt": "ok", "extra": 1}])


def test_prompt_sin_la_clave_prompt(tmp_path):
    """Falta el unico campo que el modelo exige."""
    with pytest.raises(ValueError, match="wrong format"):
        construir(tmp_path, entradas=[{"texto": "Greet shrek"}])


def test_prompt_que_no_es_texto(tmp_path):
    """Un numero no se convierte solo en `str`."""
    with pytest.raises(ValueError, match="wrong format"):
        construir(tmp_path, entradas=[{"prompt": 42}])


# --------------------------------------------------------------------------
# 4. Archivos y rutas
# --------------------------------------------------------------------------

def test_catalogo_ausente(tmp_path):
    """Lo corta `FilePath` antes de entrar al cuerpo, no tu `except`."""
    with pytest.raises(ValidationError):
        FileManager(tmp_path / "no_existe.json",
                    escribir_json(tmp_path / "prompts.json", prompts()),
                    tmp_path / "res.json")


def test_prompts_ausentes(tmp_path):
    """Igual con el segundo archivo."""
    with pytest.raises(ValidationError):
        FileManager(escribir_json(tmp_path / "functions.json", catalogo()),
                    tmp_path / "no_existe.json",
                    tmp_path / "res.json")


def test_una_carpeta_como_ruta_de_entrada(tmp_path):
    """`FilePath` exige archivo: una carpeta que existe tampoco vale."""
    carpeta = tmp_path / "carpeta"
    carpeta.mkdir()
    with pytest.raises(ValidationError):
        FileManager(carpeta,
                    escribir_json(tmp_path / "prompts.json", prompts()),
                    tmp_path / "res.json")


def test_catalogo_corrupto(tmp_path):
    """JSON mal formado: el mensaje dice cual archivo es."""
    roto = tmp_path / "functions.json"
    roto.write_text('[{"name": "fn_add_numbers",', encoding="utf-8")
    with pytest.raises(ValueError, match="Corrupt JSON"):
        FileManager(roto,
                    escribir_json(tmp_path / "prompts.json", prompts()),
                    tmp_path / "res.json")


def test_archivo_de_cero_bytes(tmp_path):
    """Un archivo existente pero vacio no es JSON valido."""
    vacio = tmp_path / "prompts.json"
    vacio.write_text("", encoding="utf-8")
    with pytest.raises(ValueError, match="Corrupt JSON"):
        FileManager(escribir_json(tmp_path / "functions.json", catalogo()),
                    vacio,
                    tmp_path / "res.json")


def test_cada_archivo_se_valida_contra_su_modelo(tmp_path):
    """Los prompts pasados como catalogo: JSON valido, modelo equivocado."""
    de_prompts = escribir_json(tmp_path / "prompts.json", prompts())
    with pytest.raises(ValueError, match="wrong format"):
        FileManager(de_prompts, de_prompts, tmp_path / "res.json")


def test_ruta_de_salida_sin_json(tmp_path):
    """La salida tiene que ser un archivo `.json`, no una carpeta."""
    with pytest.raises(ValueError):
        construir(tmp_path, salida=tmp_path / "salida")


# --------------------------------------------------------------------------
# 5. `charge_logs` — acumular en memoria
# --------------------------------------------------------------------------

def test_charge_logs_carga_un_fallo_de_prompt(rutas):
    """El indice del prompt es la clave; el mensaje, el valor."""
    manager = FileManager(*rutas)
    manager.charge_logs("3", "Text: Ġlow is not a valid token id", "prompts")
    assert manager.get_logs()["prompts"] == [
        {"3": "Text: Ġlow is not a valid token id"}]
    assert manager.get_logs()["files"] == []


def test_charge_logs_carga_un_fallo_de_archivo(rutas):
    """Los fallos sin indice van por nombre de archivo, en la otra familia."""
    manager = FileManager(*rutas)
    manager.charge_logs("vocab.json", "Vocabulary's file empty", "files")
    assert manager.get_logs()["files"] == [
        {"vocab.json": "Vocabulary's file empty"}]


def test_charge_logs_dos_indices_distintos_conviven(rutas):
    """Dos prompts fallidos: los dos quedan, en orden de llegada."""
    manager = FileManager(*rutas)
    manager.charge_logs("3", "primero", "prompts")
    manager.charge_logs("7", "segundo", "prompts")
    assert manager.get_logs()["prompts"] == [{"3": "primero"},
                                             {"7": "segundo"}]


def test_charge_logs_mismo_indice_dos_veces_no_se_pisa(rutas):
    """Con lista, el segundo fallo del prompt 3 no borra al primero."""
    manager = FileManager(*rutas)
    manager.charge_logs("3", "primero", "prompts")
    manager.charge_logs("3", "segundo", "prompts")
    assert manager.get_logs()["prompts"] == [{"3": "primero"},
                                             {"3": "segundo"}]


def test_charge_logs_con_categoria_inventada(rutas):
    """Solo existen dos familias de fallo."""
    manager = FileManager(*rutas)
    with pytest.raises(ValueError):
        manager.charge_logs("3", "mensaje", "prompt")


def test_charge_logs_con_mensaje_vacio(rutas):
    """Una entrada sin mensaje no dice nada al que lea el log."""
    manager = FileManager(*rutas)
    with pytest.raises(ValueError):
        manager.charge_logs("3", "", "prompts")


def test_charge_logs_con_clave_vacia(rutas):
    """Sin clave no se sabe a que prompt pertenece el fallo."""
    manager = FileManager(*rutas)
    with pytest.raises(ValueError):
        manager.charge_logs("", "mensaje", "prompts")


# --------------------------------------------------------------------------
# 6. `write_logs` — una sola apertura, y solo si hay algo
# --------------------------------------------------------------------------

def test_write_logs_sin_fallos_no_crea_el_archivo(rutas, tmp_path,
                                                  monkeypatch):
    """La existencia del archivo es la señal: si no hay fallos, no existe."""
    manager = FileManager(*rutas)
    monkeypatch.chdir(tmp_path)
    manager.write_logs()
    assert not (tmp_path / "logs" / "logs.json").exists()


def test_write_logs_crea_la_carpeta_y_el_archivo(rutas, tmp_path,
                                                 monkeypatch):
    """`logs/` no existe la primera vez y hay que crearla."""
    manager = FileManager(*rutas)
    manager.charge_logs("3", "mensaje", "prompts")
    monkeypatch.chdir(tmp_path)
    manager.write_logs()
    assert (tmp_path / "logs" / "logs.json").is_file()


def test_write_logs_escribe_lo_mismo_que_tiene_en_memoria(rutas, tmp_path,
                                                          monkeypatch):
    """Releido con `json.load`, el archivo es igual al dict de dentro."""
    manager = FileManager(*rutas)
    manager.charge_logs("3", "primero", "prompts")
    manager.charge_logs("vocab.json", "segundo", "files")
    monkeypatch.chdir(tmp_path)
    manager.write_logs()
    with open(tmp_path / "logs" / "logs.json", encoding="utf-8") as archivo:
        assert json.load(archivo) == manager.get_logs()


def test_write_logs_una_sola_apertura(rutas, tmp_path, monkeypatch):
    """Dos fallos y una sola llamada: un archivo con las dos entradas."""
    manager = FileManager(*rutas)
    manager.charge_logs("3", "primero", "prompts")
    manager.charge_logs("7", "segundo", "prompts")
    monkeypatch.chdir(tmp_path)
    manager.write_logs()
    with open(tmp_path / "logs" / "logs.json", encoding="utf-8") as archivo:
        assert len(json.load(archivo)["prompts"]) == 2


def test_write_logs_llamado_dos_veces_no_reescribe(rutas, tmp_path,
                                                   monkeypatch):
    """Tu guard `_n_logs`: lo que llegue despues se queda fuera."""
    manager = FileManager(*rutas)
    manager.charge_logs("3", "primero", "prompts")
    monkeypatch.chdir(tmp_path)
    manager.write_logs()
    manager.charge_logs("7", "segundo", "prompts")
    manager.write_logs()
    with open(tmp_path / "logs" / "logs.json", encoding="utf-8") as archivo:
        assert len(json.load(archivo)["prompts"]) == 1


# --------------------------------------------------------------------------
# 7. Limite y stress
# --------------------------------------------------------------------------

def test_quinientos_fallos_se_escriben(rutas, tmp_path, monkeypatch):
    """Que fallen todos los prompts no puede romper la escritura del log."""
    manager = FileManager(*rutas)
    for indice in range(500):
        manager.charge_logs(str(indice), f"fallo {indice}", "prompts")
    monkeypatch.chdir(tmp_path)
    manager.write_logs()
    with open(tmp_path / "logs" / "logs.json", encoding="utf-8") as archivo:
        assert len(json.load(archivo)["prompts"]) == 500


def test_mensaje_con_acentos_y_comillas_sobrevive(rutas, tmp_path,
                                                  monkeypatch):
    """`ensure_ascii=False`: el mensaje se relee tal cual se escribio."""
    mensaje = 'Texto: "José" ñandú \\ no válido'
    manager = FileManager(*rutas)
    manager.charge_logs("0", mensaje, "prompts")
    monkeypatch.chdir(tmp_path)
    manager.write_logs()
    with open(tmp_path / "logs" / "logs.json", encoding="utf-8") as archivo:
        assert json.load(archivo)["prompts"][0]["0"] == mensaje


def test_catalogo_de_cien_funciones(tmp_path):
    """El catalogo del peer review puede ser mucho mayor que el del ejemplo."""
    grande = [{"name": f"fn_{i}",
               "description": f"Funcion numero {i}.",
               "parameters": {"a": {"type": "number"}},
               "returns": {"type": "number"}} for i in range(100)]
    manager = construir(tmp_path, funciones=grande)
    assert len(manager.get_functions()) == 100


# --------------------------------------------------------------------------
# 8. `charge_replies` / `write_replies` — la salida que exige el subject
# --------------------------------------------------------------------------

def respuesta(indice: int) -> Dict[str, Any]:
    """Un resultado ya generado, con las tres claves exactas del subject."""
    return {"prompt": f"What is the sum of {indice} and 2?",
            "name": "fn_add_numbers",
            "parameters": {"a": float(indice), "b": 2.0}}


def leer_salida(ruta: Path) -> Any:
    """Relee el archivo de resultados tal como lo hara el corrector."""
    with open(ruta, encoding="utf-8") as archivo:
        return json.load(archivo)


def test_write_replies_crea_el_archivo(tmp_path):
    """La salida se escribe en la ruta que entro por `--output`."""
    salida = tmp_path / "data" / "output" / "function_calling_results.json"
    manager = construir(tmp_path, salida=salida)
    manager.charge_replies(respuesta(0))
    manager.write_replies()
    assert salida.is_file()


def test_la_salida_es_un_array_de_objetos(tmp_path):
    """Array, no dict: es lo que fija el subject y compara el corrector."""
    salida = tmp_path / "res.json"
    manager = construir(tmp_path, salida=salida)
    manager.charge_replies(respuesta(0))
    manager.write_replies()
    assert isinstance(leer_salida(salida), list)


def test_cada_objeto_tiene_las_tres_claves_exactas(tmp_path):
    """Ni una clave de mas ni una de menos: `prompt`, `name`, `parameters`."""
    salida = tmp_path / "res.json"
    manager = construir(tmp_path, salida=salida)
    manager.charge_replies(respuesta(0))
    manager.write_replies()
    assert set(leer_salida(salida)[0]) == {"prompt", "name", "parameters"}


def test_las_respuestas_conservan_el_orden(tmp_path):
    """El objeto 3 responde al prompt 3: el orden es la correspondencia."""
    salida = tmp_path / "res.json"
    manager = construir(tmp_path, salida=salida)
    for indice in range(3):
        manager.charge_replies(respuesta(indice))
    manager.write_replies()
    escrito = leer_salida(salida)
    assert [objeto["parameters"]["a"] for objeto in escrito] == [0.0, 1.0, 2.0]


def test_sin_respuestas_el_archivo_existe_igual(tmp_path):
    """0 prompts entran, 0 resultados salen, pero el archivo se escribe."""
    salida = tmp_path / "res.json"
    manager = construir(tmp_path, entradas=[], salida=salida)
    manager.write_replies()
    assert leer_salida(salida) == []


def test_la_salida_relee_igual_a_lo_cargado(tmp_path):
    """Ida y vuelta: lo que se carga es lo que el corrector lee."""
    salida = tmp_path / "res.json"
    manager = construir(tmp_path, salida=salida)
    cargadas = [respuesta(0), respuesta(1)]
    for una in cargadas:
        manager.charge_replies(una)
    manager.write_replies()
    assert leer_salida(salida) == cargadas


def test_los_numeros_siguen_siendo_numeros(tmp_path):
    """Un `number` del schema se escribe `2.0`, no `"2.0"`."""
    salida = tmp_path / "res.json"
    manager = construir(tmp_path, salida=salida)
    manager.charge_replies(respuesta(40))
    manager.write_replies()
    assert leer_salida(salida)[0]["parameters"]["a"] == 40.0


def test_la_salida_conserva_los_acentos(tmp_path):
    """`ensure_ascii=False`: el prompt vuelve tal cual entro."""
    salida = tmp_path / "res.json"
    manager = construir(tmp_path, salida=salida)
    manager.charge_replies({"prompt": "Greet José",
                            "name": "fn_greet",
                            "parameters": {"name": "José"}})
    manager.write_replies()
    assert leer_salida(salida)[0]["parameters"]["name"] == "José"
