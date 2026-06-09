from analytics.metrics import Metrics
from factories.request_factory import RequestFactory
from infra.parallel import ParallelExecutor
from runner.config import RunnerConfig
from services.artifact_store import ArtifactStore
from services.discovery import Discovery
from services.history_store import HistoryStore
from workflow.pipeline import WorkflowPipeline
from workflow.registry import StageRegistry


class WorkflowBuilder:

    def __init__(
        self,
        config: RunnerConfig,
        backend,
        reporters: list,
        event_bus,
        category: str = None,
        problem: str = None,
    ):
        self.config = config
        self.backend = backend
        self.reporters = reporters
        self.event_bus = event_bus
        self.category = category
        self.problem = problem

    def build(self):

        pipeline = WorkflowPipeline()

        for stage_name in self.config.workflow:
            stage = self._create_stage(stage_name)
            pipeline.add_stage(stage)

        return pipeline

    def _create_stage(self, name: str):
        common = {
            "discover": dict(
                discovery=Discovery(self.config.base_path),
                category=self.category,
                problem=self.problem,
            ),
            "execute": dict(
                executor=ParallelExecutor(),
                request_factory=RequestFactory(self.config.base_path),
                backend=self.backend,
                workers=self.config.workers,
                event_bus=self.event_bus,
            ),
            "artifact": dict(
                store=ArtifactStore(self.config.output_dir),
            ),
            "history": dict(store=HistoryStore(self.config.output_dir)),
            "metrics": dict(metrics=Metrics()),
            "report": dict(
                reporters=self.reporters,
            ),
        }

        return StageRegistry.create(name, **common[name])
