#!/usr/bin/env python3
# https://github.com/ReturnOfTheLast/p3_iot_traffic_controller

__author__ = "Akse0402 (Aksel), Benjo (Benjamin), Kayeon (Jonathan), and \
ReturnOfTheLast (Marcus)"
__credits__ = ["Akse0402 (Aksel)",
               "Benjo (Benjamin)",
               "Kayeon (Jonathan)",
               "ReturnOfTheLast (Marcus)"]
__version__ = "0.1-dev"
__status__ = "Development"

if __name__ != "__main__":
    raise ImportError("Importing this file is not allowed")

import os

if os.getuid() != 0:
    raise PermissionError("Script need to be run as root, please do so")

from queuemanager.core import FrameQueue
from sniffer.core import Sniffer
from argparse import ArgumentParser

parser: ArgumentParser = ArgumentParser()
parser.add_argument('-i', '--interface', type=str, default=None, dest='iface')
args = parser.parse_args()

sniffer: Sniffer = Sniffer(args.iface)
frame_queue: FrameQueue = FrameQueue(sniffer)

sniffer.execute()
