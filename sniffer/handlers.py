#!/usr/bin/env python3
# https://github.com/ReturnOfTheLast/p3_iot_traffic_controller

# Inspired by and burrowing from https://github.com/EONRaider/Packet-Sniffer

from __future__ import annotations
from sniffer.core import Sniffer
from logger import get_logger
from abc import ABC, abstractmethod


class FramePublisher:
    """Handle sniffer and publish frames
    """

    def __init__(self, sniffer: Sniffer):
        """FramePublisher constructor

        Args:
            sniffer (Sniffer): Sniffer to use
        """
        self._subscribers = list()
        self._sniffer = sniffer
        self.logger = get_logger(
            f"{self.__module__}.{self.__class__.__qualname__}")

    def register(self, subscriber: FrameSubscriber):
        """Register subscriber

        Args:
            subscriber (FrameSubscriber): Subscriber
        """
        self.logger.info(f"Registering {subscriber}")
        self._subscribers.append(subscriber)

    def _notify_all(self, *args, **kwargs):
        """Internal method to notify all subscribers

        Args:
            args: List of arguments
            kwargs: Dictionary of keyword arguments
        """
        self.logger.info("Notifying all subscribers")
        [subscriber.update(*args, **kwargs)
            for subscriber in self._subscribers]

    def start(self):
        """Start the sniffer and publish its frames
        """
        for frame in self._sniffer.execute():
            self._notify_all(frame)


class FrameSubscriber(ABC):
    """Abstract class to subscribe to a FramePublisher
    """

    def __init__(self, publisher: FramePublisher):
        """FrameSubscriber constructor

        Args:
            publisher (FramePublisher): Publisher to subscribe to
        """
        publisher.register(self)

    @abstractmethod
    def update(self, *args, **kwargs):
        """Update method to get new data

        Args:
            args: List of arguments
            kwargs: Dictionary of keyword argument
        """
        ...
