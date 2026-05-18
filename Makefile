SHELL := /bin/bash
POETRY := poetry
VENV := $(shell $(POETRY) env info -p)

.PHONY: test test_all

test:
	@. "$(VENV)/bin/activate" && \
	python ./runner/cli.py test array test_lc_001_two_sum

test_all:
	@. "$(VENV)/bin/activate" && \
	python3 ./runner/cli.py test-all
