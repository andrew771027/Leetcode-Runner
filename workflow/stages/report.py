from workflow.context import ExecutionContext
from workflow.stage import Stage


class ReportStage(Stage):

    def __init__(self, reporters):
        self.reporters = reporters

    def execute(self, context: ExecutionContext):
        for reporter in self.reporters:
            reporter.report(context.results)
