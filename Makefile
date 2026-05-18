SHELL := /bin/bash
POETRY := poetry
VENV := $(shell $(POETRY) env info -p)

.PHONY: test test_all

test:
	@. "$(VENV)/bin/activate" && \
	python -m runner.cli test array test_lc_001_two_sum

test_all:
	@. "$(VENV)/bin/activate" && \
	python -m runner.cli test-all
