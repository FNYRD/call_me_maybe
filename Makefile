.PHONY: push

mensaje ?= wip

push:
	git add .
	git commit -m "$(mensaje)"
	git push
