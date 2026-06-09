from workflow.registry import StageRegistry
from workflow.stage import Stage


@StageRegistry.register("history")
class HistoryStage(Stage):

    def __init__(self, store):
        self.store = store

    def execute(self, context):
        self.store.append(context.results)
