from workflow.context import ExecutionContext
from workflow.pipeline import WorkflowPipeline


class Runner:
    def __init__(self, pipeline: WorkflowPipeline):
        self.pipeline = pipeline

    def run(self):
        context = ExecutionContext()
        self.pipeline.run(context)
        return context
