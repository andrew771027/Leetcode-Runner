from workflow.context import ExecutionContext
from workflow.registry import StageRegistry
from workflow.stage import Stage


@StageRegistry.register("artifact")
class ArtifactStage(Stage):

    def __init__(self, store):
        self.store = store

    def execute(self, content: ExecutionContext):
        self.store.save_report(content.results)
