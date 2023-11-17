#!/usr/bin/env python3
# https://github.com/ReturnOfTheLast/p3_iot_traffic_controller

from pubsub import Publisher, Subscriber
from queue import Queue


class FrameQueue(Subscriber, Queue):
    """Queue object to hold frame from a sniffer
    """

    def __init__(self, publisher: Publisher, maxsize: int = 0):
        """FrameQueue constructor

        Args:
            publisher (FramePublisher): Publisher to subscribe to
            maxsize (int): Max size of the queue
        """
        self.logger.info("Initialising Frame Queue...")
        Subscriber.__init__(self, [publisher])
        Queue.__init__(self, maxsize)
        self.logger.info("Frame Queue Initialised")

    def update(self, frame: tuple[int, bytes]):
        """Update method called by publisher

        Args:
            frame (tuple[int, bytes]): Frame to add to queue
        """
        self.put_nowait(frame)
        self.logger.info(f"~{self.qsize()} elements in the queue")


class CommandQueue(Subscriber, Queue):
    def __init__(self, publishers: list[Publisher], maxsize: int = 0):
        self.logger.info("Initialising Command Queue...")
        Subscriber.__init__(self, publishers)
        Queue.__init__(self, maxsize)
        self.logger.info("Command Queue Initialised")

    def update(self, command: dict[str, str | int | bool]):
        self.put_nowait(command)
        self.logger.info(f"~{self.qsize()} elements in the queue")
