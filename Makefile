mensaje ?= wip
test ?= wip

export UV_CACHE_DIR ?= $(HOME)/sgoinfre/.cache/uv
export HF_HOME ?= $(HOME)/sgoinfre/.cache/huggingface

install:
	uv sync

run:
	uv run python -m src

debug:
	uv run python -m pdb -m src

lint:
	uv run flake8 .
	uv run mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	uv run flake8 .
	uv run mypy . --strict

view:
	uv run python -m src.view

test:
	uv run pytest -v

testN:
	uv run pytest tests/test_bloque_"$(test)".py -v

clean:
	rm -rf data/output logs
	rm -rf .pytest_cache .mypy_cache .claude .mypy_cache
	find . -type d -name __pycache__ -not -path "./.venv/*" -exec rm -rf {} +
	find . -type f -name tempCodeRunnerFile.py -not -path "./.venv/*" -exec rm -f {} +

clean-venv:
	rm -rf .venv

clean-cache:
	rm -rf $(UV_CACHE_DIR) $(HF_HOME)

push:
	git add .
	git commit -m "$(mensaje)"
	git push

.PHONY: install run debug lint lint-strict view test testN push clean clean-venv clean-cache
