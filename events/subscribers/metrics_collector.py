from contracts.subscriber import EventSubscriber
from events.event import Event


class MetricsSubscriber(EventSubscriber):
    def __init__(self):
        self.total = 0

    def handle(self, event: Event):
        if event.type == "test_finished":
            self.total += 1
