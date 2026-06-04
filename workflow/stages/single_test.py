from workflow.context import ExecutionContext
from workflow.stage import Stage


class SingleTestStage(Stage):

    def __init__(self, category: str, problem: str):
        self.category = category
        self.problem = problem

    def execute(self, context: ExecutionContext):
        context.files = [(self.category, f"tests/{self.category}/{self.problem}.py")]
