from backends.registry import BackendRegistry
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

        for mw in self._middlewares:
            backend = MiddlewareRegistry.create(mw).wrap(backend)

        return backend
