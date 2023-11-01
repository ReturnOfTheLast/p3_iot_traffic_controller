#!/usr/bin/env python3
# https://github.com/ReturnOfTheLast/p3_iot_traffic_controller

# Inspired by and burrowing from https://github.com/EONRaider/Packet-Sniffer

from __future__ import annotations
from logger import get_logger
from logging import Logger
from abc import ABC, abstractmethod


class Publisher:
    """A class for publishing
    """

    def __init__(self):
        """Publisher constructor
        """
        self._subscribers: list[Subscriber] = list()
        self.logger:  Logger = get_logger(
            f"{self.__module__}.{self.__class__.__qualname__}")

    def register(self, subscriber: Subscriber):
        """Register subscriber

        Args:
            subscriber (Subscriber): Subscriber
        """
        self.logger.info(f"Registering {subscriber}")
        self._subscribers.append(subscriber)

    def _notify_all(self, *args, **kwargs):
        """Internal method to notify all subscribers

        Args:
            args: Arguments
            kwargs: Keyword Arguments
        """
        self.logger.info("Notifying all subscribers")
        self.logger.debug(f"Notification: \n{args}\n{kwargs}")
        [subscriber.update(*args, **kwargs)
            for subscriber in self._subscribers]


class Subscriber(ABC):
    """Abstract class to subscribe to Publishers
    """

    def __init__(self, publishers: list[Publisher]):
        """Subscriber constructor

        Args:
            publishers (list[Publisher]): Publishers to subscribe to
        """
        self.logger:  Logger = get_logger(
            f"{self.__module__}.{self.__class__.__qualname__}")

        for publisher in publishers:
            publisher.register(self)

    @abstractmethod
    def update(self, *args, **kwargs):
        """Update method to get new data

        Args:
            args: Arguments
            kwargs: Keyword Argument
        """
        ...
