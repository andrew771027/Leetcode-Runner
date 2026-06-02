from abc import ABC, abstractmethod


class ExecutionReporter(ABC):
    @abstractmethod
    def report(self, results):
        pass
