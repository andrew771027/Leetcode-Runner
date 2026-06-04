from pathlib import Path

from infra.event_logger import EventLogger
from workflow.context import ExecutionContext
from workflow.stage import Stage


class ExecuteStage(Stage):

    def __init__(
        self, executor, request_factory, backend, workers: int = 1, event_logger: EventLogger = None
    ):
        self.executor = executor
        self.request_factory = request_factory
        self.backend = backend
        self.workers = workers
        self.event_logger = event_logger

    def execute(self, context: ExecutionContext):
        context.results = self.executor.run(
            self._execute_one,
            context.files,
            max_workers=self.workers,
        )

    def _execute_one(self, test_file):
        category, path = test_file
        problem = Path(path).stem

        request = self.request_factory.create(
            category=category,
            problem=problem,
        )

        if self.event_logger:
            self.event_logger.emit(
                "test_start",
                {"name": request.name, "category": request.category},
            )

        try:
            result = self.backend.execute(request)

            if self.event_logger:
                self.event_logger.emit(
                    "test_finished",
                    {
                        "name": result.name,
                        "category": result.category,
                        "success": result.success,
                        "duration": result.duration,
                    },
                )

            return result
        except Exception as e:
            if self.event_logger:
                self.event_logger.emit(
                    "test_failed",
                    {
                        "name": request.name,
                        "category": request.category,
                        "error": str(e),
                    },
                )
            raise
