from backends.registry import BackendRegistry
from middleware.pipeline import MiddlewarePipeline
from middleware.registry import MiddlewareRegistry


class RunnerBuilder:
    def __init__(self):
        self._backend = None
        self._middlewares = []

    def with_backend(self, name):
        self._backend = name
        return self

    def with_middleware(self, name):
        if name not in self._middlewares:
            self._middlewares.append(name)
        return self

    def build_backend(self):
        if self._backend is None:
            raise RuntimeError("Backend not configured")

        backend = BackendRegistry.create(self._backend)

        middlewares = [MiddlewareRegistry.create(name) for name in self._middlewares]

        if not middlewares:
            return backend

        return MiddlewarePipeline(backend=backend, middlewares=middlewares)
