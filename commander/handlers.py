#!/usr/bin/env python3
# https://github.com/ReturnOfTheLast/p3_iot_traffic_controller

# Inspired by and burrowing from https://github.com/EONRaider/Packet-Sniffer

from __future__ import annotations
from logger import get_logger
from abc import ABC, abstractmethod


class CommandPublisher:
    """Handle sniffer and publish frames
    """

    def __init__(self):
        """CommandPublisher constructor
        """
        self._subscribers = list()
        self.logger = get_logger(
            f"{self.__module__}.{self.__class__.__qualname__}")

    def register(self, subscriber: CommandSubscriber):
        """Register subscriber

        Args:
            subscriber (CommandSubscriber): Subscriber
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


class CommandSubscriber(ABC):
    """Abstract class to subscribe to a CommandPublisher
    """

    def __init__(self, publishers: list[CommandPublisher]):
        """CommandSubscriber constructor

        Args:
            publishers (list[CommandPublisher]): Publisher to subscribe to
        """
        for publisher in publishers:
            publisher.register(self)

    @abstractmethod
    def update(self, *args, **kwargs):
        """Update method to get new data

        Args:
            args: List of arguments
            kwargs: Dictionary of keyword argument
        """
        ...
