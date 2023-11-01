#!/usr/bin/env python3
# https://github.com/ReturnOfTheLast/p3_iot_traffic_controller

from framedissect import dissect
from queuemanager.core import FrameQueue
from pubsub.core import Publisher
from netprotocols import Protocol
import re

ip_pattern: str = r'^10\.10\.0\.[0-9]*$'


class Analyser(Publisher):

    def __init__(self, frame_queue: FrameQueue):
        Publisher.__init__(self)
        self.frame_queue: FrameQueue = frame_queue

    def next_frame(self):
        self.frame: tuple[int, bytes] = self.frame_queue.get()
        self.framedic: tuple[int, dict[str, Protocol]] = dissect(self.frame[1])

    def analyse(self):
        if 'IPv4' in self.framedic[1].keys():
            if re.match(ip_pattern, self.framedic[1]['IPv4'].src):
                data: bytes = self.frame[1][self.framedic[0]:]
                self.logger.debug(f"Data: {data}")
                # TODO: Do something with the data
            else:
                self.logger.info("Source is not from network... ignoring")

        else:
            self.logger.info("Couldn't find IPv4")
            self.logger.debug(f"The protocols were {self.framedic[1].keys()}")
