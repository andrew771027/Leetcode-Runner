from dataclasses import dataclass

from backends.registry import BackendRegistry


@dataclass
class RunnerConfig:
    base_path: str
    backend: str = "subprocess"
    docker: bool = False
    workers: int = 4
    output_dir: str = "output"

    def validate(self, backend_registry: BackendRegistry):
        if self.backend not in backend_registry.available():
            raise ValueError(
                f"Invalid backend: {self.backend}. " f"Available: {backend_registry.available()}"
            )

        if self.workers < 1:
            raise ValueError("workers must be >= 1")
