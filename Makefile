mensaje ?= wip
test ?= wip

test:
	./callme/bin/python -m pytest -v

testN:
	./callme/bin/python -m pytest tests/test_bloque_"$(test)".py -v 

install-model:
	./callme/bin/pip install -e llm_sdk

clean-files:
	rm -rf data/output logs
	rm -rf .pytest_cache .mypy_cache
	find . -type d -name __pycache__ -not -path "./callme/*" -exec rm -rf {} +

push:
	git add .
	git commit -m "$(mensaje)"
	git push

venv:
	python3 -m venv callme
	pip3 install regex

.PHONY: push test testN install-model push venv clean-files
