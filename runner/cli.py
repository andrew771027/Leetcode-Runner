import typer

from backends.registry import BackendRegistry
from events.builder import EventBusBuilder
from events.bus import EventBus
from factories.builder import RunnerBuilder
from reporters.registry import ReporterRegistry
from runner.config import RunnerConfig
from runner.engine import Runner
from runner.runner_config import ConfigLoader
from workflow.builder import WorkflowBuilder

app = typer.Typer()


def build_event_bus(config: RunnerConfig) -> EventBus:

    return EventBusBuilder(config.output_dir).build(config.event_subscribers)


def build_backend(config: RunnerBuilder):
    return (
        RunnerBuilder()
        .with_backend(config.backend)
        # .with_middlewares("timeout")  # 暫時保留，但先不要啟用
        .with_middlewares(config.middleware)
        .build_backend()
    )


def build_runner(config: RunnerConfig, category: str = None, problem: str = None) -> Runner:
    backend = build_backend(config)

    event_bus = build_event_bus(config)

    reporters = ReporterRegistry.create_many(config.reporters)

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
def run(
    config_path: str = typer.Option("runner.yaml", "--config"),
    category: str | None = typer.Option(None, "--category"),
    problem: str | None = typer.Option(None, "--problem"),
):
    conifg = ConfigLoader.load(path=config_path)

    runner = build_runner(config=conifg, category=category, problem=problem)

    context = runner.run()

    if context.results:
        print(f"\nExecuted {len(context.results)} tests")


@app.command()
def list_backends():
    print(BackendRegistry.available())


@app.command()
def list_reporters():
    print(ReporterRegistry.available())


if __name__ == "__main__":
    app()
