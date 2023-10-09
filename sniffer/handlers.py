#!/usr/bin/env python3
# https://github.com/ReturnOfTheLast/p3_iot_traffic_controller

# Inspired by and burrowing from https://github.com/EONRaider/Packet-Sniffer

from sniffer.core import Sniffer
from logger import get_module_logger
from abc import ABC, abstractmethod

logger = get_module_logger(__name__)


class FramePublisher:
    def __init__(self):
        self._subscribers = list()

    def register(self, subscriber) -> None:
        logger.info(f"Registering {subscriber}")
        self._subscribers.append(subscriber)

    def _notify_all(self, *args, **kwargs) -> None:
        logger.info("Notifying all subscribers")
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
