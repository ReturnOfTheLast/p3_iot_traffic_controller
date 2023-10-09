#!/usr/bin/env python3
# https://github.com/ReturnOfTheLast/p3_iot_traffic_controller

from sniffer.handlers import FramePublisher, FrameSubscriber
from logger import get_module_logger
from queue import Queue

logger = get_module_logger(__name__)


class FrameQueue(FrameSubscriber, Queue):
    def __init__(self, publisher: FramePublisher, maxsize=0):
        FrameSubscriber.__init__(self, publisher)
        Queue.__init__(self, maxsize)
        logger.info("Frame Queue created")

    def update(self, frame) -> None:
        self.put_nowait(frame)
        logger.info(f"Frame Queue: ~{self.qsize()} elements")
