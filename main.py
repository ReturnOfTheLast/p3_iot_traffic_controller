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
    raise Exception("Importing this file is not allowed")
    exit(1)

import os

if os.getuid() != 0:
    raise Exception("Script need to be run as root, please do so")
    exit(1)

from queuemanager.core import FrameQueue
from sniffer.handlers import FramePublisher
from logger import get_logger
import argparse

logger = get_logger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--interface', type=str, default=None, dest='iface')
args = parser.parse_args()

sniffer = FramePublisher()
frame_queue = FrameQueue(sniffer)

logger.info("Starting sniffer")
sniffer.listen(args.iface)
