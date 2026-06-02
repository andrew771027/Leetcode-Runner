class MiddlewareRegistry:

    _registry = {}

    @classmethod
    def register(cls, name):
        def decorator(middleware_cls):
            cls._registry[name] = middleware_cls
            return middleware_cls

        return decorator

    @classmethod
    def create(cls, name: str):
        if name not in cls._registry:
            raise ValueError(f"Unknown middleware: {name}."
                             f"Available: {cls.available()}"
                             )
        return cls._registry[name]()

    @classmethod
    def avaiable(cls):
        return list(cls._registry.keys())
