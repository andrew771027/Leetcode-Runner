from backends.docker import DockerBackend
from backends.subprocess import SubprocessBackend


class BackendRegistry:

    _registry = {
        "subprocess": SubprocessBackend,
        "docker": DockerBackend,
    }

    @classmethod
    def create(cls, name: str):
        if name not in cls._registry:
            raise ValueError(f"Unknown backend: {name}")
        return cls._registry[name]()
