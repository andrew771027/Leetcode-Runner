from workflow.context import ExecutionContext
from workflow.stage import Stage


class MetricsStage(Stage):

    def __init__(self, metrics):
        self.metrics = metrics

    def execute(self, context: ExecutionContext):
        context.summary = self.metrics.summary(context.results)
