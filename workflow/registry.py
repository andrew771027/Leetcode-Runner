class StageRegistry:

    _registry = {}

    @classmethod
    def register(cls, name):
        def decorator(stage_cls):
            cls._registry[name] = stage_cls
            return stage_cls

        return decorator

    @classmethod
    def create(cls, name, **kwargs):
        if name not in cls._registry:
            raise ValueError(f"Unknown stage: {name}. " f"Available: {cls.available()}")
        return cls._registry[name](**kwargs)

    @classmethod
    def available(cls):
        return list(cls._registry.keys())
