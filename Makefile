mensaje ?= wip
test ?= wip

test:
	./callme/bin/python -m pytest -v

testN:
	./callme/bin/python -m pytest tests/test_bloque_"$(test)".py -v 

install-model:
	./callme/bin/pip install -e llm_sdk

push:
	git add .
	git commit -m "$(mensaje)"
	git push

venv:2
	python3 -m venv callme
	pip3 install regex

.PHONY: push test testN install-model push venv
