#!/usr/bin/env python3
# https://github.com/ReturnOfTheLast/p3_iot_traffic_controller

from threading import Lock


class Singleton(type):
    _instances: set = {}

    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super(Singleton, cls).__call__(
                    *args,
                    **kwargs)
        return cls._instances[cls]
