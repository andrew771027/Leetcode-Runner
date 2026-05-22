import os

import typer

from analytics.metrics import Metrics
from backends.docker_backend import DockerBackend
from backends.subprocess_backend import SubprocessBackend
from models.test_result import TestResult
from reporters.printer import Printer
from runner.config import RunnerConfig
from runner.core import Runner
from runner.logger import EventLogger
from utils.discovery import Discovery

DEFAULT_BASE_PATH = os.getenv("LEETCODE_BASE_PATH", "/Users/poyuan/Desktop/andrew771027/LeetCode")


app = typer.Typer()
backend = SubprocessBackend()
logger = EventLogger()
metrics = Metrics()


@app.command()
def test(
    category: str = typer.Option(..., "--category", help="Category name"),
    problem: str = typer.Option(..., "--problem", help="Problem name"),
    base_path: str = typer.Option(DEFAULT_BASE_PATH, "--base-path", help="Base path for tests"),
):
    "Run tests for a single problem."
    config = RunnerConfig(base_path, False)

    runner = Runner(
        config=config, backend=backend, discovery=Discovery(config.base_path), logger=logger
    )

    results: TestResult = runner.run_test(category, problem)

    Printer.print([results])
    Printer.to_json([results])


@app.command()
def test_all(
    base_path: str = typer.Option(DEFAULT_BASE_PATH, "--base-path", help="Base path for tests"),
    docker: bool = typer.Option(False, "--docker/--no-docker", help="Use Docker backend"),
):
    "Run all problems"

    config = RunnerConfig(base_path, docker)

    backend = DockerBackend() if config.docker else SubprocessBackend()

    runner = Runner(
        config=config,
        backend=backend,
        discovery=Discovery(config.base_path),
        logger=logger,
    )

    results = runner.run_all_tests()

    ranked = metrics.rank(results)
    short_summary = metrics.short_summary(results)

    precise_summary = metrics.precise_summary(results)

    Printer.print_rank(ranked)

    print("\n📊 Short Summary")
    Printer.print_summary(short_summary)

    print("\n📊 Precise Summary")
    Printer.print_summary(precise_summary)


if __name__ == "__main__":
    app()
