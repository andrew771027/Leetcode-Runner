import time

from contracts.backend import ExecutionBackend
from contracts.middleware import ExecutionMiddleware
from middleware.registry import MiddlewareRegistry
from models.execution_request import ExecutionRequest
from models.test_result import TestResult


@MiddlewareRegistry.register("benchmark")
class BenchmarkMiddleware(ExecutionMiddleware):

    def wrap(self, backend: ExecutionBackend):
        self.backend = backend
        return self

    def execute(self, request: ExecutionRequest) -> TestResult:
        start = time.perf_counter()

        result = self.backend.execute(request)

        result.duration = time.perf_counter() - start

        return result
