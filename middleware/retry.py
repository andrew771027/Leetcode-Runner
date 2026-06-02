from contracts.backend import ExecutionBackend
from contracts.middleware import ExecutionMiddleware, NextHandler
from middleware.registry import MiddlewareRegistry
from models.execution_request import ExecutionRequest
from models.test_result import TestResult


@MiddlewareRegistry.register("retry")
class RetryMiddleware(ExecutionMiddleware):

    def __init__(self, retries=2):
        self.retries = retries

    def execute(self, request: ExecutionRequest, next_handler: NextHandler) -> TestResult:

        for _ in range(self.retries):
            try:
                return next_handler(request)
            except Exception as e:
                last_error = e
                print(f"Retry failed: {e}")

        raise last_error
