#!/usr/bin/env python3
# https://github.com/ReturnOfTheLast/p3_iot_traffic_controller

from framedissect import dissect
from queuemanager import FrameQueue
from pubsub import Publisher
from netprotocols import Protocol
from threading import Thread, Event
from queue import Empty
import re

ip_pattern: str = r'^10\.10\.0\.[0-9]*$'


class Analyser(Publisher, Thread):

    def __init__(
        self,
        frame_queue: FrameQueue,
        stop_event: Event,
        name: str = None
    ):
        self.logger.info("Initialising Analyser...")
        Publisher.__init__(self)
        Thread.__init__(self, name=name)
        self.stop_event: Event = stop_event
        self.frame_queue: FrameQueue = frame_queue
        self.logger.info("Analyser Initialised")

    def analyse(
        self,
        frame: tuple[int, bytes],
        framedic: tuple[int, dict[str, Protocol]]
    ):
        if 'IPv4' in framedic[1].keys():
            if re.match(ip_pattern, framedic[1]['IPv4'].src):
                data: bytes = frame[1][framedic[0]:]
                self.logger.debug(f"Data: {data}")
                # TODO: Do something with the data
            else:
                self.logger.info("Source is not from network... ignoring")

        else:
            self.logger.info("Couldn't find IPv4")
            self.logger.debug(f"The protocols were {framedic[1].keys()}")

    def run(self):
        while not self.stop_event.is_set():
            try:
                frame: tuple[int, bytes] = self.frame_queue.get(timeout=10)
                framedic: tuple[int, dict[str, Protocol]] = dissect(frame[1])
            except Empty:
                self.logger.debug("No Frame Available")
                continue

            self.analyse(frame, framedic)

        self.logger.info("Analyser has Stopped")
