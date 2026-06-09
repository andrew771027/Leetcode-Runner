import os

import typer

import events.subscribers
import workflow.stages
from backends.registry import BackendRegistry
from events.bus import EventBus
from events.subscribers.file_logger import FileLoggerSubscriber
from events.subscribers.metrics_collector import MetricsSubscriber
from factories.builder import RunnerBuilder
from reporters.registry import ReporterRegistry
from runner.config import RunnerConfig
from runner.engine import Runner
from workflow.builder import WorkflowBuilder

DEFAULT_BASE_PATH = os.getenv("LEETCODE_BASE_PATH", "/Users/poyuan/Desktop/andrew771027/LeetCode")

app = typer.Typer()


def build_event_bus(config: RunnerConfig) -> EventBus:

    event_bus = EventBus()

    file_logger = FileLoggerSubscriber(path=f"{config.output_dir}/event.jsonl")

    event_bus.subscribe("test_started", file_logger)
    event_bus.subscribe("test_finished", file_logger)
    event_bus.subscribe("test_failed", file_logger)

    event_bus.subscribe("test_finished", MetricsSubscriber())

    return event_bus


def build_backend(config: RunnerBuilder):

    backend = (
        RunnerBuilder()
        .with_backend(config.backend)
        .with_middleware("retry")
        # .with_middleware("timeout")  # 暫時保留，但先不要啟用
        .with_middleware("benchmark")
        .build_backend()
    )

    return backend


def build_runner(
    config: RunnerConfig, reporters, category: str = None, problem: str = None
) -> Runner:
    backend = build_backend(config)

    event_bus = build_event_bus(config)

    pipeline = WorkflowBuilder(
        config=config,
        backend=backend,
        reporters=reporters,
        event_bus=event_bus,
        category=category,
        problem=problem,
    ).build()

    return Runner(pipeline)


@app.command()
def test(
    category: str = typer.Option(..., "--category", help="Category name"),
    problem: str = typer.Option(..., "--problem", help="Problem name"),
    base_path: str = typer.Option(DEFAULT_BASE_PATH, "--base-path", help="Base path for tests"),
    backend: str = typer.Option("subprocess", "--backend", help="User specific backend"),
    reporter: str = typer.Option("console", "--reporter", help="Use specific reporter"),
):

    config = RunnerConfig(base_path=base_path, backend=backend, docker=False, workers=1)

    reporters = ReporterRegistry.create_many(reporter.split(","))

    runner = build_runner(config=config, reporters=reporters, category=category, problem=problem)

    context = runner.run()

    if context.results:
        result = context.results[0]
        print(f"{result.name} -> {'PASS' if result.success else 'FAIL'}")


@app.command()
def test_all(
    base_path: str = typer.Option(DEFAULT_BASE_PATH, "--base-path", help="Base path for tests"),
    backend: str = typer.Option("subprocess", "--backend", help="Use specific backend"),
    workers: int = typer.Option(4, "--worker", help="User specific number of worker"),
    reporter: str = typer.Option("console", "--reporter", help="Use specific reporter"),
):
    config = RunnerConfig(base_path=base_path, backend=backend, workers=workers)

    reporters = ReporterRegistry.create_many(reporter.split(","))

    runner = build_runner(config=config, reporters=reporters)

    context = runner.run()

    for r in reporters:
        r.report(context.results)


@app.command()
def list_backends():
    print(BackendRegistry.available())


@app.command()
def list_reporters():
    print(ReporterRegistry.available())


if __name__ == "__main__":
    app()
