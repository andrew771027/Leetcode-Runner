import time

from contracts.backend import ExecutionBackend
from contracts.middleware import ExecutionMiddleware, NextHandler
from middleware.registry import MiddlewareRegistry
from models.execution_request import ExecutionRequest
from models.test_result import TestResult


@MiddlewareRegistry.register("benchmark")
class BenchmarkMiddleware(ExecutionMiddleware):

    def execute(self, request: ExecutionRequest, next_handler: NextHandler) -> TestResult:

        start = time.perf_counter()

        result = next_handler(request)

        result.duration = time.perf_counter() - start

        return result
