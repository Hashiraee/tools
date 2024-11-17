SHELL := /bin/bash
VIRTUALENV ?= .venv

.PHONY: help install freeze clean prompt install-aider aider clean-aider

help:
	@echo "Make targets:"
	@echo "  - code:		Convert all code to a prompt"
	@echo "  - install:		Install all dependencies"
	@echo "  - freeze:		Freeze al dependencies"
	@echo "  - clean:		Clean all cache files"
	@echo "  - prompt:		Convert current project to a prompt"
	@echo "Check the Makefile for more details"

tree:
	@tree --gitignore

install:
	@python3 -m venv $(VIRTUALENV)
	@. $(VIRTUALENV)/bin/activate; pip3 install --upgrade pip; pip3 install -r requirements.txt

freeze:
	@. $(VIRTUALENV)/bin/activate; pip3 freeze > requirements.txt

clean:
	@find . -name "*.pyc" -delete
	@find . -name "__pycache__" -type d -exec rm -rf {} \+
	@find . -name ".ipynb_checkpoints" -type d -exec rm -rf {} \+

prompt:
	@python3 tools/concat_files.py --folder . --output misc/code.txt
	@python3 tools/tokens.py misc/code.txt
	@pbcopy < misc/code.txt && echo "Copied to clipboard!"

install-aider:
	@python3 -m venv .aidervenv
	@. .aidervenv/bin/activate; python3 -m pip install -U aider-chat

aider:
	@. .aidervenv/bin/activate; aider

clean-aider:
	@rm -rf .aider.chat.history.md .aider.input.history .aider.tags.cache.v3

run:
	@. $(VIRTUALENV)/bin/activate; python3 src/main.py
