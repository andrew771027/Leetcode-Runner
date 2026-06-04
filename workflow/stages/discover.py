from workflow.context import ExecutionContext
from workflow.stage import Stage


class DiscoverStage(Stage):

    def __init__(self, discovery):
        self.discovery = discovery

    def execute(self, context: ExecutionContext):
        context.files = self.discovery.find_all()
