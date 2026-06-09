from workflow.context import ExecutionContext
from workflow.registry import StageRegistry
from workflow.stage import Stage


@StageRegistry.register("metrics")
class MetricsStage(Stage):

    def __init__(self, metrics):
        self.metrics = metrics

    def execute(self, context: ExecutionContext):
        context.summary = self.metrics.summary(context.results)
