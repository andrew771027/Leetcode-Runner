from workflow.context import ExecutionContext
from workflow.registry import StageRegistry
from workflow.stage import Stage


@StageRegistry.register("discover")
class DiscoverStage(Stage):

    def __init__(self, discovery, category: str = None, problem: str = None):
        self.discovery = discovery
        self.category = category
        self.problem = problem

    def execute(self, context: ExecutionContext):
        if self.category and self.problem:
            context.files = [
                (
                    self.category,
                    f"tests/{self.category}/{self.problem}.py",
                )
            ]
            return

        context.files = self.discovery.find_all()
