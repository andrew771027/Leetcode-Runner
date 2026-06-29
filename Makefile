SHELL := /bin/bash
POETRY := poetry
PYTHON := $(POETRY) run python
CONFIG ?= runner.yaml
BASE_PATH ?= /Users/poyuan/Desktop/andrew771027/LeetCode

.PHONY: run

run:
	@$(PYTHON) -m runner.cli run --config "$(CONFIG)"
