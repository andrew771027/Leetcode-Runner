from contracts.subscriber import EventSubscriber
from events.event import Event
from events.registry import SubscriberRegistry


@SubscriberRegistry.register("metrics")
class MetricsSubscriber(EventSubscriber):
    def __init__(self):
        self.finished_count = 0
        self.failed_count = 0

    def handle(self, event: Event):
        if event.type == "test_finished":
            self.finished_count += 1

            if not event.payload.get("success"):
                self.failed_count += 1
