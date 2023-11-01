#!/usr/bin/env python3
# https://github.com/ReturnOfTheLast/p3_iot_traffic_controller

# Inspired by and burrowing from https://github.com/EONRaider/Packet-Sniffer

from __future__ import annotations
from logger import get_logger
from logging import Logger
from abc import ABC, abstractmethod


class FramePublisher:
    """A class for publishing frames
    """

    def __init__(self):
        """FramePublisher constructor
        """
        self._subscribers: list[FrameSubscriber] = list()
        self.logger: Logger = get_logger(
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
