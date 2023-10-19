#!/usr/bin//env python3
# https://github.com/ReturnOfTheLast/p3_iot_traffic_controller

from framedissect import dissect
from queuemanager.core import FrameQueue
import re


class Analyser:

    def __init__(self):
        self.frame = FrameQueue.get()

    def layer(self):
        self.framedic = dissect(self.frame[1])

    def traffic_flow(self):

        if 'IPv4' in self.framedic[1].keys():
            if re.match(r'^10\.10\.0\.[0-9]*$', self.framedic[1]['IPv4'].src):
                packet = self.frame[1][self.framedic[0]:]

        else:
            print('IPv4 is not found.')
            print(f'Packet keys are:{self.framedic[1].keys()}')
