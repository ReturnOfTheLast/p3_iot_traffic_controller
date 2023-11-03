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
        Subscriber.__init__(self, [publisher])
        Queue.__init__(self, maxsize)
        self.logger.info("Frame Queue created")

    def update(self, frame: tuple[int, bytes]):
        """Update method called by publisher

        Args:
            frame (tuple[int, bytes]): Frame to add to queue
        """
        self.put_nowait(frame)
        self.logger.info(f"Frame Queue: ~{self.qsize()} elements")


class CommandQueue(Subscriber, Queue):
    def __init__(self, publishers: list[Publisher], maxsize: int = 0):
        Subscriber.__init__(self, publishers)
        Queue.__init__(self, maxsize)
        self.logger.info("Command Queue created")

    def update(self, command: dict[str, str | int | bool]):
        self.put_nowait(command)
        self.logger.info(f"Command Queue: ~{self.qsize()} elements")
