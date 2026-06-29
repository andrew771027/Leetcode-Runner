class SubscriberRegistry:

    _registry = {}

    @classmethod
    def register(cls, name: str):
        def decorator(subscriber_cls):
            cls._registry[name] = subscriber_cls
            return subscriber_cls

        return decorator

    @classmethod
    def create(cls, name: str, **kwargs):
        if name not in cls._registry:
            raise ValueError(f"Unknown subscriber: {name}. " f"Available: {cls.available()}")

        return cls._registry[name](**kwargs)

    @classmethod
    def available(cls):
        return list(cls._registry.keys())
