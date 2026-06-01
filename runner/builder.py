from backends.registry import BackendRegistry
from middleware.benchmark import BenchmarkMiddleware
from middleware.retry import RetryMiddleware
from middleware.timeout import TimeoutMiddleware


class RunnerBuilder:
    def __init__(self):
        self.backend_name = "subprocess"
        self.middleware = []

    def with_backend(self, name):
        self.backend_name = name
        return self

    def with_middleware(self, name):
        if name not in self.middleware:
            self.middleware.append(name)
        return self

    def build_backend(self):
        backend = BackendRegistry.create(self.backend_name)

        for mw in self.middleware:
            if mw == "benchmark":
                backend = BenchmarkMiddleware(backend)
            elif mw == "timeout":
                backend = TimeoutMiddleware(backend)
            elif mw == "retry":
                backend = RetryMiddleware(backend)
            return backend
