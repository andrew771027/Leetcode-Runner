class ReporterRegistry:

    _registry = {}

    @classmethod
    def register(cls, name):
        def decorator(reporter_cls):
            cls._registry[name] = reporter_cls
            return reporter_cls

        return decorator

    @classmethod
    def create(cls, name):
        if name not in cls._registry:
            raise ValueError(f"Unknown reporter: {name}")
        return cls._registry[name]()

    @classmethod
    def create_many(cls, names: str):
        return [cls._registry[name]() for name in names]

    @classmethod
    def avaiable(cls):
        return list(cls._registry.keys())
