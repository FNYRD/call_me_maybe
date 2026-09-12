*This project has been created as part of the 42 curriculum by jericard.*

# call me maybe

## Description

`call me maybe` translates natural language prompts into structured function calls, using a small local LLM (**Qwen/Qwen3-0.6B**, 0.6B parameters). Given `"What is the sum of 40 and 2?"`, it does not compute `42` — it outputs:

```json
{
  "name": "fn_add_numbers",
  "parameters": {"a": 40.0, "b": 2.0}
}
```

Small models fail at producing valid, schema-conformant JSON from prompting alone (~30% success rate in practice). The core of this project is **constrained decoding**: the model's logits are modified at every generation step so it can only pick tokens that keep the output valid JSON, conformant with the target function's schema — never letting invalid structure through, and never letting a heuristic or `if/else` pick the function instead of the model.

## Instructions

Dependencies are managed with [`uv`](https://docs.astral.sh/uv/):

```bash
uv sync
```

Run the program:

```bash
uv run python -m src [--functions_definition <path>] [--input <path>] [--output <path>]
```

Defaults, if the flags are omitted:

| Flag | Default |
|---|---|
| `--functions_definition` | `data/input/functions_definition.json` |
| `--input` | `data/input/function_calling_tests.json` |
| `--output` | `data/output/function_calling_results.json` |

Example with explicit paths:

```bash
uv run python -m src \
  --functions_definition data/input/functions_definition.json \
  --input data/input/function_calling_tests.json \
  --output data/output/function_calling_results.json
```

Run the test suite:

```bash
make test          # all blocks
make testN test=N  # one block where N=number of the file test
make view          # interactive terminal demo of the generation pipeline (src/view.py)
```

## Resources

- [Qwen3 model card](https://huggingface.co/Qwen/Qwen3-0.6B) — the model this project targets
- [Byte-Pair Encoding (BPE) explained](https://huggingface.co/learn/nlp-course/chapter6/5) — the tokenization scheme behind `llm_sdk`'s vocabulary
- [Constrained decoding / structured generation](https://arxiv.org/abs/2307.09702) — background on masking logits to force grammar-conformant output
- [Pydantic documentation](https://docs.pydantic.dev/) — validation library required by the subject for every class

**How AI was used:** an AI assistant (Claude, via Claude Code) acted as a tutor throughout the project — discussing designs, asking questions to surface gaps, and verifying each step by running it, but never writing the project's implementation code. It was used to: stress-test design proposals and write the block contracts along with the author, which were then consumed by a separate blind testing agent. All source code in `src/` was written by the author.

## Algorithm explanation

The pipeline, prompt to output:

```text
                              ┌────────┐
                              │ Prompt │
                              └────────┘
                                   │
                                   ▼
                            ┌───────────────────┐
                            │ Build chat prompt │
                            │ (system + user)   │
                            └───────────────────┘
                                      │
                                      ▼
    ┌──────────────────────────────────────────┐
    │ 1. Tokenize: prompt + JSON built so far  │◄──┐
    │ 2. get_logits_from_input_ids             │   │
    │ 3. Mask: keep only ids Guardian says are │   │
    │    valid for the current slot            │   │
    │ 4. Pick the highest surviving logit      │   │
    │ 5. Append that token to the JSON         │   │
    └──────────────────────────────────────────┘   │
                          ▼                        │
                 JSON object closed? ── no ────────┘
                          │ yes
                          ▼
  ┌───────────────────────────────────────────────┐
  │ Undo escape markers -> json.loads -> validate │
  └───────────────────────────────────────────────┘
```

Step 3, the mask, is where constrained decoding actually lives:

1. At each step, the current partial JSON string (`written`) and the current position in the schema (`slot`: which function, which parameter, what type) determine which characters can legally come next.
2. Every token in the vocabulary is checked against that rule (`Guardian._char_ok`) — the ones that would break JSON syntax or violate the parameter's declared type get their logit set to `-inf`.
3. The token is sampled greedily from what remains valid.
4. A small fixed skeleton (`{"name": "`, `", "parameters": {`, closing braces) is injected literally instead of generated — the model only ever writes the two things it actually needs to decide: **which function**, and **the values of its parameters**. This was a deliberate simplification: the JSON structure is already known in full before generation starts, so making the model spell out punctuation it can't get wrong wastes generation steps for no benefit.

**Escape handling:** function-argument strings that themselves contain a `"` or a `\` (e.g. `"the string 'hello'"` inside a JSON string) confuse a byte-by-byte generator, because the model has to reproduce a two-character escape sequence (`\"`, `\\`) exactly. This project masks the echoed prompt fragment with a single dynamically-chosen marker character per escape type, lets the model copy that one character instead of the two-character escape, and translates it back before `json.loads` — verified against the model, not just reasoned about.

## Design decisions

- **All classes are `pydantic` models**, as required by the subject — parsing, validation, and the final generation result (`Output`, with its three possible states: written normally, cut at the character cap, or failed) are all typed models, not raw dicts.
- **The result of `Interface.reply()` is an already-translated, already-validated `dict`**, not a raw string. Earlier in the project this lived split between `Interface` and `Chat`; it was consolidated into `Interface` because that class already holds both pieces needed to finish the job (the tokenizer's byte↔char table and the function catalog), while `Chat` would have had to look the function back up by name to do the same work.
- **The character-validity check has a cache** (bonus 4): the same `(slot, flag, closing-char)` state is looked up instead of re-scanning ~151,000 vocabulary entries on every call — measured at ~1.2s for a cold lookup vs ~0.00s once cached.
- **Function selection is made entirely by the model**, never by keyword matching or an `if/else` router — explicitly forbidden by the subject.
- **A blind testing agent writes the tests**, from a contract (PDF) written only after the class exists and runs — never from the source code itself, so a green test can't just be confirming what the code already (possibly wrongly) does.

## Performance analysis

| Metric | Result |
| --- | --- |
| Precision (own stress suite, 9 prompts covering nesting, negatives, mixed types, quote/backslash escapes) | 8/9 — one documented model limitation (see Challenges faced), not a code bug |
| Precision (independent test set from a peer's project, 11 prompts) | 10/11 — one documented model limitation (mojibake glyph, see below) |
| Comparative suite against a peer's independent implementation (regex-based candidate extraction, `tests/test_bloque_2.py`, 20 prompts) | 17/20 this project vs. 14/20 the peer's — the peer's implementation scores 11/11 on its own exam but loses most of the 9 added stress cases (nesting, shared type parameters) |
| Full run of the reference test data | completes in well under the 5-minute budget the subject sets, on standard hardware |
| Crashes | none — every entry point is wrapped so a malformed file or model failure is logged, never an unhandled exception |

## Challenges faced

- **Negative numbers occasionally lost** (e.g. `"went from -12.5 to 3"` → drops the `-`). The `-` token is confirmed present and legal in the whitelist at that position (checked directly against `get_valid_ids()`); the model itself simply doesn't always pick it. Four different fix strategies were tried and measured — a system instruction (no effect), blind sign inversion (unsafe, breaks other prompts), inversion gated by a keyword heuristic (has gaps), and reordering the injected numbers (breaks a case that previously worked from the model's own semantic reasoning). None improved the metric enough to justify its cost, so this is left as a known model limitation rather than patched.
- **A mojibake glyph occasionally replaces an apostrophe.** Blocking that glyph in the whitelist fixes that one case but breaks a different, legitimate case where the same glyph is a real space — net gain zero, so it was not applied.
- **Combined quote+backslash escapes caused a generation loop.** Two two-character escapes together in the same string value made the model repeat the same token indefinitely. Five approaches were tried; what worked was masking the echoed prompt fragment behind a single dynamically chosen one-character marker per escape type (instead of asking the model to copy two literal characters), then translating it back before parsing. Verified against the real model across the full stress suite, not just the case that motivated it.
- **A trailing space glued to the edge of a string value**, caused by the model copying a vocabulary token that itself starts with a space marker. Fixed with a `.strip()` at the point where a raw leaf value is decoded back to text, verified to cause no regressions elsewhere.

## Findings — model limitations

Measured directly against the real model, stress-testing beyond the official example set:

- **Sustained exact-copy window: ~36 characters.** Copying text letter by letter into a `string` value stays clean up to roughly 36 copied characters; past that, whole words start gluing together in camelCase (`"theLazyDogAndRanAway"`) or get dropped outright. This is not a context-window limit — the model has 40960 tokens available against ~13 used in the cases that trigger it — it's a capacity limit of a 0.6B model on sustained exact copying, unrelated to escaping.
- **Escaped characters count double against that same budget.** A quote or backslash that needs escaping (`\"`, `\\`) costs two characters of the copy budget instead of one, so a string with two such escapes hits the ~36-character wall roughly twice as fast as plain text of the same length. This is why the quote+backslash generation loop (see Challenges faced) and the copy-length limit are the same underlying constraint, not two separate bugs.
- **Missing word separator + wrong capitalization on long verbatim copies (fixed).** Copying a full sentence out of the prompt (e.g. `"...the mat with another cat"`) occasionally dropped the space between two words and capitalized both (`"withAnotherCat"`) — the model choosing to concatenate rather than emit a real separator token. Fixed by detecting, after generation, that a value normalizes (case- and space-insensitive) to exactly one quoted span in the prompt, and replacing it with that literal span — or, when the function's own description calls for a case transform, with the span recased to match the pattern the model was already writing, so an intentional `UPPERCASE`/`Capitalize` output isn't overwritten. Verified against the real model with no regressions on either test suite.

## Testing strategy

Every block (`src/tokenizer.py`, `src/filemanager.py`, `src/promptbuilder.py`, `src/guardian.py`, `src/interface.py`, `src/chat.py`) is covered by its own `pytest` file in `tests/`, written by an agent that never reads `src/` — only a contract PDF describing what the class is required to accept, reject, and produce from the outside. This keeps a green test from just confirming whatever the implementation happens to do.

Each block's suite covers, at minimum: correct construction across parameter combinations, the expected normal flow, a valid boundary value, stress past that boundary, and invalid input handled without crashing or leaving invalid state. Each test suite per block was used by the author before moving to the next project block. 
This project includes only a minimal test suite to verify the project as a whole (non-block-specific) with a defined objective.

On top of the per-block suites:

- `tests/stress_data/` — a 9-prompt suite designed specifically to stress edge cases found while building the project (nesting, shared-prefix function names, negative numbers, floats, booleans, escaped quotes/backslashes).
- `tests/new_data/` — an independent test set from a classmate's project, used as a second, unbiased accuracy check.
- `tests/test_bloque_2.py` — a comparative suite that runs the same prompts through this project and through a peer's independent implementation, to catch cases where one design's blind spots are hidden by its own test data.

`flake8` and `mypy --strict` are enforced on all of `src/`; per a deliberate project decision, they are not run against `tests/` — the bar there is that a test actually exercises what it claims to, with correct typing.

## Example usage

Input, `functions_definition.json`:

```json
[
  {
    "name": "fn_add_numbers",
    "description": "Add two numbers together and return their sum.",
    "parameters": {"a": {"type": "number"}, "b": {"type": "number"}},
    "returns": {"type": "number"}
  }
]
```

Input, `function_calling_tests.json`:

```json
[
  {"prompt": "What is the sum of 40 and 2?"}
]
```

Run:

```bash
uv run python -m src \
  --functions_definition functions_definition.json \
  --input function_calling_tests.json \
  --output result.json
```

Output, `result.json`:

```json
[
  {
    "prompt": "What is the sum of 40 and 2?",
    "name": "fn_add_numbers",
    "parameters": {"a": 40.0, "b": 2.0}
  }
]
```
