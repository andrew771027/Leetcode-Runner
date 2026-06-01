import os

import typer

from infra.parallel import ParallelExecutor
from reporters.registry import ReporterRegistry
from runner.builder import RunnerBuilder
from runner.config import RunnerConfig
from runner.core import Runner
from runner.request_factory import RequestFactory
from utils.discovery import Discovery

DEFAULT_BASE_PATH = os.getenv("LEETCODE_BASE_PATH", "/Users/poyuan/Desktop/andrew771027/LeetCode")

app = typer.Typer()


def build_runner(config: RunnerConfig) -> Runner:
    backend = (
        RunnerBuilder().with_backend(config.backend).with_middleware("benchmark").build_backend()
    )

    return Runner(
        config=config,
        backend=backend,
        discovery=Discovery(config.base_path),
        executor=ParallelExecutor(),
        request_factory=RequestFactory(config.base_path),
    )


@app.command()
def test(
    category: str = typer.Option(..., "--category", help="Category name"),
    problem: str = typer.Option(..., "--problem", help="Problem name"),
    base_path: str = typer.Option(DEFAULT_BASE_PATH, "--base-path", help="Base path for tests"),
    backend: str = typer.Option("subprocess", "--backend", help="User specific backend"),
):
    "Run tests for a single problem."
    config = RunnerConfig(base_path=base_path, backend=backend, docker=False, workers=1)

    runner = build_runner(config)

    result = runner.run_test(category, problem)

    print(f"{result.name} -> {'PASS' if result.success else 'FAIL'}")


@app.command()
def test_all(
    base_path: str = typer.Option(DEFAULT_BASE_PATH, "--base-path", help="Base path for tests"),
    backend: str = typer.Option("subprocess", "--backend", help="Use specific backend"),
    workers: int = typer.Option(4, "--worker", help="User specific number of worker"),
    reporter: str = typer.Option("console", "--reporter", help="Use specific reporter"),
):
    "Run all problems"

    config = RunnerConfig(base_path=base_path, backend=backend, workers=workers)

    runner = build_runner(config)

    reporters = ReporterRegistry.create_many(reporter.split(","))

    results = runner.run_all_tests()

    for r in reporters:
        r.report(results)


if __name__ == "__main__":
    app()
