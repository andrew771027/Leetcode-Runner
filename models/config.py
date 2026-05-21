from dataclasses import dataclass


@dataclass
class RunnerConfig:
    base_path: str
    docker: bool = False
