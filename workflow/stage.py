from abc import ABC, abstractmethod

from workflow.context import ExecutionContext


class Stage(ABC):

    @abstractmethod
    def execute(self, context: ExecutionContext):
        pass
