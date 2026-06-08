from collections import defaultdict

from contracts.subscriber import EventSubscriber
from events.event import Event


class EventBus:

    def __init__(self):
        self.subscribers = defaultdict(list)

    def subscribe(
        self,
        event_type,
        subscriber: EventSubscriber,
    ):
        self.subscribers[event_type].append(subscriber)

    def publish(self, event: Event):

        for subscriber in self.subscribers[event.type]:
            subscriber.handle(event)
