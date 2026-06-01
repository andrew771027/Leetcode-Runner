SHELL := /bin/bash
POETRY := poetry
VENV := $(shell $(POETRY) env info -p)

.PHONY: test test_all

test:
	@. "$(VENV)/bin/activate" && \
	python -m runner.cli test --base-path "/Users/poyuan/Desktop/andrew771027/LeetCode" --category array --problem test_lc_001_two_sum --backend subprocess

test_all_local:
	@. "$(VENV)/bin/activate" && \
	python -m runner.cli test-all --base-path "/Users/poyuan/Desktop/andrew771027/LeetCode" --backend subprocess --worker 4 --reporter console

test_all_docker:
	@. "$(VENV)/bin/activate" && \
	python -m runner.cli test-all --base-path "/Users/poyuan/Desktop/andrew771027/LeetCode" --backend docker --worker 4 --reporter console
