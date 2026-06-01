from middleware.registry import MiddlewareRegistry
from models.test_result import TestResult
from runner.interfaces import BaseBackend, BaseMiddleware
from runner.request_factory import ExecutionRequest


@MiddlewareRegistry.register("retry")
class RetryMiddleware(BaseMiddleware):

    def __init__(self, retries=2):
        self.wrapper = None
        self.retries = retries

    def wrap(self, backend: BaseBackend):
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
