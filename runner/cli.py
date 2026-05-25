import os

import typer

from analytics.output.storage import Storage
from backends.docker import DockerBackend
from backends.subprocess import SubprocessBackend

from runner.config import RunnerConfig
from runner.core import Runner
from infra.logger import Logger
from infra.parallel import ParallelExecutor
from utils.discovery import Discovery
from backends.benchmark import BenchmarkBackend

from reporters.composite import CompositeReporter
from reporters.storage import StorageReporter
from reporters.json_reporter import JsonReporter
from reporters.logger import LoggerReporter
from reporters.console import ConsoleReporter

from runner.request_factory import RequestFactory

DEFAULT_BASE_PATH = os.getenv("LEETCODE_BASE_PATH", "/Users/poyuan/Desktop/andrew771027/LeetCode")

app = typer.Typer()

@app.command()
def test(
    category: str = typer.Option(..., "--category", help="Category name"),
    problem: str = typer.Option(..., "--problem", help="Problem name"),
    base_path: str = typer.Option(DEFAULT_BASE_PATH, "--base-path", help="Base path for tests"),
):
    "Run tests for a single problem."
    config = RunnerConfig(base_path=base_path, 
                          backend="subprocess",
                          docker=False)
    
    backend = BenchmarkBackend(SubprocessBackend())

    runner = Runner(
        config=config,
        backend=backend,
        discovery=None,
        executor=ParallelExecutor(),
        request_factory=RequestFactory(config.base_path)
    )

    result = runner.run_test(category, problem)

    print(f"{result.name} -> {'PASS' if result.success else 'FAIL'}")


@app.command()
def test_all(
    base_path: str = typer.Option(DEFAULT_BASE_PATH, "--base-path", help="Base path for tests"),
    docker: bool = typer.Option(False, "--docker/--no-docker", help="Use Docker backend"),
):
    "Run all problems"

    config = RunnerConfig(base_path=base_path, 
                          backend="docker", 
                          docker=docker, 
                          workers=4)

    
    backend = BenchmarkBackend(DockerBackend() if config.docker else SubprocessBackend())

    reporter = CompositeReporter([
        ConsoleReporter(),
        JsonReporter(),
        StorageReporter(Storage()),
        LoggerReporter(Logger())
    ])


    runner = Runner(
        config=config,
        backend=backend,
        discovery=Discovery(config.base_path),
        executor=ParallelExecutor(),
        request_factory=RequestFactory(config.base_path)
    )

    results = runner.run_all_tests()

    reporter.report(results)


if __name__ == "__main__":
    app()
