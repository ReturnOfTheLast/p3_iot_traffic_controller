#!/usr/bin/env python3
# https://github.com/ReturnOfTheLast/p3_iot_traffic_controller

from framedissect import dissect
from analyser.utils import from_network, get_ip_location, whiteblacklisted
from queuemanager import FrameQueue
from pubsub import Publisher
from netprotocols import Protocol
from threading import Thread, Event
from queue import Empty
import json

with open("country_codes.json", "r") as fp:
    country_codes = json.load(fp)


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
        self.frame_queue: FrameQueue = frame_queue
        self.stop_event: Event = stop_event
        self.logger.debug(f"Attached Stop Event:\n{self.stop_event}")
        self.logger.info("Analyser Initialised")

    def analyse(
        self,
        frame: tuple[int, bytes],
        framedic: tuple[int, dict[str, Protocol]]
    ) -> tuple[bool, str | None]:
        if 'IPv4' in framedic[1].keys():
            if from_network(framedic[1]['IPv4'].src):
                if whiteblacklisted(framedic[1]['IPv4'].dst):
                    return False, framedic[1]['IPv4'].dst

                data: bytes = frame[1][framedic[0]:]
                self.logger.debug(f"Data: {data}")

                iplog, exception = get_ip_location(framedic[1]['IPv4'].dst)
                if iplog is None:
                    self.logger.debug(f"IP API Exception:\n{exception}")
                    return False, framedic[1]['IPv4'].dst

                if (iplog.get("countryCode", None) and
                        iplog["countryCode"] in country_codes):
                    return True, framedic[1]['IPv4'].dst
                return False, framedic[1]['IPv4'].dst

            self.logger.info("Source is not from network... ignoring")
            return False, framedic[1]['IPv4'].dst

        self.logger.info("Couldn't find IPv4")
        self.logger.debug(f"The protocols were {framedic[1].keys()}")
        return False, None

    def run(self):
        while not self.stop_event.is_set():
            try:
                frame: tuple[int, bytes] = self.frame_queue.get(timeout=10)
                framedic: tuple[int, dict[str, Protocol]] = dissect(frame[1])
            except Empty:
                self.logger.debug("No Frame Available")
                continue

            block, ip = self.analyse(frame, framedic)
            self.logger.debug(f"Analysis result:\nblock: {block}\nip: {ip}")
            if block:
                self._notify_all(ip)
        self.logger.info("Analyser has Stopped")
