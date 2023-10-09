#!/usr/bin/env python3
# https://github.com/ReturnOfTheLast/p3_iot_traffic_controller

from ..sniffer.handlers import FramePublisher, FrameSubscriber
from queue import Queue


class PacketQueue(FrameSubscriber, Queue):
    def __init__(self, publisher: FramePublisher, maxsize=0):
        FrameSubscriber.__init__(self, publisher)
        Queue.__init__(self, maxsize)

    def update(self, frame) -> None:
        self.put_nowait(frame)
