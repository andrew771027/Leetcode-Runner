SHELL := /bin/bash
POETRY := poetry
VENV := $(shell $(POETRY) env info -p)

.PHONY: test test_all

test:
	@. "$(VENV)/bin/activate" && \
	python -m runner.cli test --base-path "/Users/poyuan/Desktop/andrew771027/LeetCode/tests" --category array --problem test_lc_001_two_sum

test_all_local:
	@. "$(VENV)/bin/activate" && \
	python -m runner.cli test-all --base-path "/Users/poyuan/Desktop/andrew771027/LeetCode/tests"

test_all_docker:
	@. "$(VENV)/bin/activate" && \
	python -m runner.cli test-all --base-path "/Users/poyuan/Desktop/andrew771027/LeetCode/tests" --docker
