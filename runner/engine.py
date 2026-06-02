from pathlib import Path
from typing import List

from analytics.metrics import Metrics
from contracts.backend import ExecutionBackend
from factories.request_factory import RequestFactory
from infra.event_logger import EventLogger
from models.test_result import TestResult
from runner.config import RunnerConfig
from services.artifact_store import ArtifactStore
from services.history_store import HistoryStore


class Runner:

    def __init__(
        self,
        config: RunnerConfig,
        backend: ExecutionBackend,
        discovery,
        executor,
        request_factory: RequestFactory,
        artifact_store: ArtifactStore = None,
        history_store: HistoryStore = None,
        metrics: Metrics = None,
        event_logger: EventLogger = None,
    ):
        self.config = config
        self.backend = backend
        self.discovery = discovery
        self.executor = executor
        self.request_factory = request_factory
        self.artifact_store = artifact_store
        self.history_store = history_store
        self.metrics = (metrics,)
        self.event_logger = event_logger

    def run_test(self, category: str, problem: str) -> TestResult:

        request = self.request_factory.create(category=category, problem=problem)

        if self.event_logger:
            self.event_logger.emit("test_started", {"name": request.name})

        result = self.backend.execute(request)

        if self.event_logger:
            self.event_logger.emit(
                "test_finished",
                {
                    "name": result.name,
                    "success": result.success,
                    "duration": result.duration,
                },
            )

        return result

    def run_all_tests(self) -> List[TestResult]:
        files = self.discovery.find_all()

        if self.event_logger:
            self.event_logger.emit("test_suite_started", {"count": len(files)})

        previous_results = self.history_store.load_latest() if self.history_store else []

        results = self.executor.run(
            self._execute,
            files,
            max_workers=self.config.workers,
        )

        if self.artifact_store:
            self.artifact_store.save_report(results)

        if self.history_store:
            self.history_store.append(results)

        if self.metrics and previous_results:
            regressions = self.metrics.detect_regression(previous_results, results)

            if self.event_logger:
                self.event_logger.emit(
                    "regression_detected",
                    {"regressions": regressions},
                )

        if self.event_logger:
            self.event_logger.emit("test_suite_finished", {"count": len(results)})

        return results

    def _execute(self, test_file) -> TestResult:
        category, path = test_file
        problem = Path(path).stem

        request = self.request_factory.create(category=category, problem=problem)

        if self.event_logger:
            self.event_logger.emit("test_started", {"name": request.name})

        result = self.backend.execute(request)

        if self.event_logger:
            self.event_logger.emit(
                "test_finished",
                {
                    "name": result.name,
                    "success": result.success,
                    "duration": result.duration,
                },
            )

        return result
