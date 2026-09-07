import argparse
from llm_sdk import Small_LLM_Model
from .chat import Chat
from typing import Callable
from pathlib import Path
from typing import Dict, List
import json
import sys


def write_logs(reason: str) -> None:
    logs: Dict[str, List[Dict[str, str]]] = {
            "prompts": [], "files": []}
    log_path: Path = Path("logs/logs.json")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logs["files"].append(
        {"An error occurred while reading and processing project files":
         reason})
    with open(log_path, "w", encoding="utf-8") as file:
        json.dump(logs, file, ensure_ascii=False, indent=4)


try:
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument(
        "--functions_definition",
        default="data/input/functions_definition.json")
    parser.add_argument(
        "--input", default="data/input/function_calling_tests.json")
    parser.add_argument(
        "--output", default="data/output/function_calling_results.json")

    args: argparse.Namespace = parser.parse_args()
    model: Small_LLM_Model = Small_LLM_Model()
    logits_function: Callable[[list[int]], list[float]] = (
        model.get_logits_from_input_ids)
    merge: str = model.get_path_to_merges_file()
    tokenizer: str = model.get_path_to_tokenizer_file()
    vocab: str = model.get_path_to_vocab_file()
    chat: Chat = Chat(
        args.functions_definition,
        args.input,
        args.output,
        Path(vocab),
        Path(merge),
        Path(tokenizer),
        logits_function)
    chat.chatting()
except Exception as e:
    try:
        write_logs(str(e))
    except Exception as e:
        print(
            f"An unexpected error occurs out of our scope: {e}",
            file=sys.stderr)
