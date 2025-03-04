from typing import MutableMapping, Type, Any


class ThreadUnsafeSingletonMeta(type):
    _instances: MutableMapping[Type, Any] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
