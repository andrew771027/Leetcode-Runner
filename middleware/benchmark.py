import time

from middleware.registry import MiddlewareRegistry
from models.test_result import TestResult
from runner.interfaces import BaseBackend, BaseMiddleware
from runner.request_factory import ExecutionRequest


@MiddlewareRegistry.register("benchmark")
class BenchmarkMiddleware(BaseMiddleware):

    def wrap(self, backend: BaseBackend):
        self.backend = backend
        return self

    def execute(self, request: ExecutionRequest) -> TestResult:
        start = time.perf_counter()

        result = self.backend.execute(request)

        result.duration = time.perf_counter() - start

        return result
