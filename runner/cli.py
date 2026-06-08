import os

import typer

from analytics.metrics import Metrics
from backends.registry import BackendRegistry
from events.bus import EventBus
from events.subscribers.file_logger import FileLoggerSubscriber
from events.subscribers.metrics_collector import MetricsSubscriber
from factories.builder import RunnerBuilder
from factories.request_factory import RequestFactory
from infra.parallel import ParallelExecutor
from reporters.registry import ReporterRegistry
from runner.config import RunnerConfig
from runner.engine import Runner
from services.artifact_store import ArtifactStore
from services.discovery import Discovery
from services.history_store import HistoryStore
from workflow.pipeline import WorkflowPipeline
from workflow.stages.artifact import ArtifactStage
from workflow.stages.discover import DiscoverStage
from workflow.stages.execute import ExecuteStage
from workflow.stages.history import HistoryStage
from workflow.stages.metrics import MetricsStage
from workflow.stages.report import ReportStage
from workflow.stages.single_test import SingleTestStage

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


def build_test_runner(config: RunnerConfig, category: str, problem: str, reporters):
    backend = build_backend(config)

    event_bus = build_event_bus(config)

    request_factory = RequestFactory(config.base_path)

    pipeline = WorkflowPipeline()

    pipeline.add_stage(SingleTestStage(category, problem))
    pipeline.add_stage(
        ExecuteStage(
            executor=ParallelExecutor(),
            request_factory=request_factory,
            backend=backend,
            workers=1,
            event_bus=event_bus,
        )
    )
    pipeline.add_stage(ArtifactStage(ArtifactStore(config.output_dir)))
    pipeline.add_stage(ReportStage(reporters))

    return Runner(pipeline)


def build_test_all_runner(config: RunnerConfig, reporters):
    backend = build_backend(config)

    event_bus = build_event_bus(config)

    request_factory = RequestFactory(config.base_path)

    pipeline = WorkflowPipeline()

    pipeline.add_stage(DiscoverStage(Discovery(config.base_path)))
    pipeline.add_stage(
        ExecuteStage(
            executor=ParallelExecutor(),
            request_factory=request_factory,
            backend=backend,
            workers=config.workers,
            event_bus=event_bus,
        )
    )
    pipeline.add_stage(ArtifactStage(ArtifactStore(config.output_dir)))
    pipeline.add_stage(HistoryStage(HistoryStore(config.output_dir)))
    pipeline.add_stage(MetricsStage(Metrics()))
    pipeline.add_stage(ReportStage(reporters))

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

    runner = build_test_runner(config, category, problem, reporters)

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

    runner = build_test_all_runner(config, reporters)

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
