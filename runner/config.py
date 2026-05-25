from dataclasses import dataclass


@dataclass
class RunnerConfig:
    base_path: str
    backend: str = "subprocess"
    docker: bool = False
    workers: int = 4    
