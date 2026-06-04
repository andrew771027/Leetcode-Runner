from workflow.context import ExecutionContext
from workflow.stage import Stage


class WorkflowPipeline:

    def __init__(self):
        self.stages = []

    def add_stage(self, stage: Stage):
        self.stages.append(stage)

    def run(self, context: ExecutionContext):
        for stage in self.stages:
            stage.execute(context)
        return context
