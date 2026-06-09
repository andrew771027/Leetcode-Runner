from dataclasses import dataclass, field

from backends.registry import BackendRegistry


@dataclass
class RunnerConfig:
    base_path: str
    backend: str = "subprocess"
    docker: bool = False
    workers: int = 4
    output_dir: str = "output"

    workflow: list[str] = field(
        default_factory=lambda: [
            "discover",
            "execute",
            "artifact",
            "history",
            "metrics",
            "report",
        ]
    )

    event_subscribers: dict = field(
        default_factory=lambda: {
            "test_started": ["file_logger"],
            "test_finished": ["file_logger", "metrics"],
            "test_failed": ["file_logger"],
        }
    )

    def validate(self, backend_registry: BackendRegistry):
        if self.backend not in backend_registry.available():
            raise ValueError(
                f"Invalid backend: {self.backend}. " f"Available: {backend_registry.available()}"
            )

        if self.workers < 1:
            raise ValueError("workers must be >= 1")
