#!/usr/bin//env python3
# https://github.com/ReturnOfTheLast/p3_iot_traffic_controller

from logger import get_logger
from framedissect import dissect
from queuemanager.core import FrameQueue
import re

ip_pattern: str = r'^10\.10\.0\.[0-9]*$'


class Analyser:

    def __init__(self, frame_queue: FrameQueue):
        self.frame_queue = frame_queue
        self.logger = get_logger(
            f"{self.__module__}.{self.__class__.__qualname__}")

    def next_frame(self):
        self.frame = self.frame_queue.get()
        self.framedic = dissect(self.frame[1])

    def analyse(self):
        if 'IPv4' in self.framedic[1].keys():
            if re.match(ip_pattern, self.framedic[1]['IPv4'].src):
                data = self.frame[1][self.framedic[0]:]
                self.logger.debug(f"Data: {data}")
            else:
                self.logger.info("Source is not from network... ignoring")

        else:
            self.logger.info("Couldn't find IPv4")
            self.logger.debug(f"The protocols were {self.framedic[1].keys()}")
