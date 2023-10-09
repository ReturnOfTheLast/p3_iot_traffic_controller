#!/usr/bin/env python3
# https://github.com/ReturnOfTheLast/p3_iot_traffic_controller

from sniffer.handlers import FramePublisher, FrameSubscriber
from logger import get_logger
from queue import Queue


class FrameQueue(FrameSubscriber, Queue):
    def __init__(self, publisher: FramePublisher, maxsize=0):
        FrameSubscriber.__init__(self, publisher)
        Queue.__init__(self, maxsize)
        self.logger = get_logger(
            f"{self.__module__}.{self.__class__.__qualname__}")
        self.logger.info("Frame Queue created")

    def update(self, frame) -> None:
        self.put_nowait(frame)
        self.logger.info(f"Frame Queue: ~{self.qsize()} elements")
