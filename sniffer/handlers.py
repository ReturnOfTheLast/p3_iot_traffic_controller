#!/usr/bin/env python3
# https://github.com/ReturnOfTheLast/p3_iot_traffic_controller

# Inspired by and burrowing from https://github.com/EONRaider/Packet-Sniffer

from sniffer.core import Sniffer
from logger import get_logger
from abc import ABC, abstractmethod


class FramePublisher:
    def __init__(self):
        self._subscribers = list()
        self.logger = get_logger(
            f"{self.__module__}.{self.__class__.__qualname__}")

    def register(self, subscriber) -> None:
        self.logger.info(f"Registering {subscriber}")
        self._subscribers.append(subscriber)

    def _notify_all(self, *args, **kwargs) -> None:
        self.logger.info("Notifying all subscribers")
        [subscriber.update(*args, **kwargs)
            for subscriber in self._subscribers]

    def listen(self, interface: str) -> None:
        for frame in Sniffer(interface).execute():
            self._notify_all(frame)


class FrameSubscriber(ABC):
    def __init__(self, publisher: FramePublisher):
        publisher.register(self)

    @abstractmethod
    def update(self, *args, **kwargs):
        ...
