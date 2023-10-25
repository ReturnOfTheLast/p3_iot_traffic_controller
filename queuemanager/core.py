#!/usr/bin/env python3
# https://github.com/ReturnOfTheLast/p3_iot_traffic_controller

from sniffer.handlers import FramePublisher, FrameSubscriber
from commander.handlers import CommandPublisher, CommandSubscriber
from logger import get_logger
from queue import Queue


class FrameQueue(FrameSubscriber, Queue):
    """Queue object to hold frame from a sniffer
    """

    def __init__(self, publisher: FramePublisher, maxsize: int = 0):
        """FrameQueue constructor

        Args:
            publisher (FramePublisher): Publisher to subscribe to
            maxsize (int): Max size of the queue
        """
        FrameSubscriber.__init__(self, publisher)
        Queue.__init__(self, maxsize)
        self.logger = get_logger(
            f"{self.__module__}.{self.__class__.__qualname__}")
        self.logger.info("Frame Queue created")

    def update(self, frame: tuple[int, bytes]):
        """Update method called by publisher

        Args:
            frame (tuple[int, bytes]): Frame to add to queue
        """
        self.put_nowait(frame)
        self.logger.info(f"Frame Queue: ~{self.qsize()} elements")


class CommandQueue(CommandSubscriber, Queue):
    def __init__(self, publishers: list[CommandPublisher], maxsize: int = 0):
        CommandSubscriber.__init__(self, publishers)
        Queue.__init__(self, maxsize)
        self.logger = get_logger(
            f"{self.__module__}.{self.__class__.__qualname__}")
        self.logger.info("Command Queue created")

    def update(self, command: dict[str, str | int | bool]):
        self.put_nowait(command)
        self.logger.info(f"Command Queue: ~{self.qsize()} elements")
