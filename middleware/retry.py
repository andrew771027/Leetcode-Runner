from contracts.backend import ExecutionBackend
from contracts.middleware import ExecutionMiddleware
from middleware.registry import MiddlewareRegistry
from models.execution_request import ExecutionRequest
from models.test_result import TestResult


@MiddlewareRegistry.register("retry")
class RetryMiddleware(ExecutionMiddleware):

    def __init__(self, retries=2):
        self.wrapper = None
        self.retries = retries

    def wrap(self, backend: ExecutionBackend):
        self.backend = backend
        return self

    def execute(self, request: ExecutionRequest) -> TestResult:
        if not hasattr(self, "backend"):
            raise RuntimeError("Middleware not wrapped with backend")

        for _ in range(self.retries):
            try:
                return self.backend.execute(request)
            except Exception as e:
                last_error = e
                print(f"Retry failed: {e}")

        raise last_error
