from src.callme_files_loader import CallMeFilesLoader
from src.decoder import Decoder

FUNCTIONS = [{
    "name": "fn_write_log_entry",
    "description": "Write a raw log message exactly as given.",
    "parameters": {"message": {"type": "string"}},
    "returns": {"type": "string"},
}]

PROMPT = 'Log the message: He said "hi" from C:\\tmp'

loader = CallMeFilesLoader()
loader.load_functions(FUNCTIONS)

decoder = Decoder()
func_name = decoder.decode_func_name(
    PROMPT, loader.func_names, loader.func_definitions)
print("func_name elegido:", func_name)

params = decoder.decode_func_params(
    PROMPT, loader.func_definitions[func_name])
print("params:", params)
