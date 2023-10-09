#!/usr/bin/env python3
# https://github.com/ReturnOfTheLast/p3_iot_traffic_controller

# Inspired by and burrowing from https://github.com/EONRaider/Packet-Sniffer

__author__ = "Akse0402 (Aksel), Benjo (Benjamin), Kayeon (Jonathan), and \
ReturnOfTheLast (Marcus)"
__credits__ = ["Akse0402 (Aksel)",
               "Benjo (Benjamin)",
               "Kayeon (Jonathan)",
               "ReturnOfTheLast (Marcus)"]
__version__ = "0.1-dev"
__status__ = "Development"

from sniffer.core import PacketQueueHandler
import os
import logging
import queue

logging.basicConfig(filename="traffic_controller.log", level=logging.ERROR)

packet_queue = queue.Queue()
snifferHandler = PacketQueueHandler()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser
    parser.add_argument("-i", "--interface", type=str, default=None)
    args = parser.parse_args()

    if os.getuid != 0:
        logging.error("Invalid permissions, please run as root")
        exit(1)
