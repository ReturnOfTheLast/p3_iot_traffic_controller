#!/usr/bin/env python3
# https://github.com/ReturnOfTheLast/p3_iot_traffic_controller

# Inspired by and burrowing from https://github.com/EONRaider/Packet-Sniffer

from core import Sniffer
from abc import ABC, abstractmethod


class FramePublisher:
    def __init__(self):
        self._observers = list()

    def register(self, observer) -> None:
        self._observers.append(observer)

    def _notify_all(self, *args, **kwargs) -> None:
        [observer.update(*args, **kwargs) for observer in self._observers]

    def listen(self, interface: str) -> None:
        for frame in Sniffer(interface).execute():
            self._notify_all(frame)


class FrameSubscriber(ABC):
    def __init__(self, publisher: FramePublisher):
        publisher.register(self)

    @abstractmethod
    def update(self, *args, **kwargs):
        ...
