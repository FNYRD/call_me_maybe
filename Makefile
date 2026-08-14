.PHONY: push

mensaje ?= wip

push:
	git add .
	git commit -m "$(mensaje)"
	git push

venv:
	python3 -m venv callme
	pip3 install regex
