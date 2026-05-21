from abc import ABC, abstractmethod
from typing import List


class ExecutionBackend(ABC):
    @abstractmethod
    def run(self, cmd: List[str]) -> int:
        pass
