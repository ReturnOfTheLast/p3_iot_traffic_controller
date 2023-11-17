#!/usr/bin/env python3
# https://github.com/ReturnOfTheLast/p3_iot_traffic_controller

# Inspired by and burrowing from https://github.com/EONRaider/Packet-Sniffer

from __future__ import annotations
from logger import LoggingObject
from abc import abstractmethod


class Publisher(LoggingObject):
    """A class for publishing
    """

    def __init__(self):
        """Publisher constructor
        """
        self._subscribers: list[Subscriber] = list()

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


class Subscriber(LoggingObject):
    """Abstract class to subscribe to Publishers
    """

    def __init__(self, publishers: list[Publisher]):
        """Subscriber constructor

        Args:
            publishers (list[Publisher]): Publishers to subscribe to
        """

        self.logger.info("Registering to publishers")
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
