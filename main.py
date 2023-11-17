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

from queuemanager import FrameQueue, CommandQueue
from sniffer import Sniffer
from analyser import Analyser
from commander import Commander
from logger import LoggingObject
from argparse import ArgumentParser
from threading import Event
from time import sleep
from dotenv import load_dotenv


class MainLogger(LoggingObject):
    ...


logger = MainLogger().logger

load_dotenv()

parser: ArgumentParser = ArgumentParser()
parser.add_argument('-i', '--interface', type=str, default=None, dest='iface')
parser.add_argument('-a', '--analysers', type=int, default=4, dest='analysers')
args = parser.parse_args()

logger.debug(f"CLI Args: \n{args}")

stop_event = Event()
logger.debug(f"Created stop event: \n{stop_event}")


logger.info("Initialising Modules...")

sniffer: Sniffer = Sniffer(args.iface, stop_event, "Sniffer")

frame_queue: FrameQueue = FrameQueue(sniffer)

analysers: list[Analyser] = list()
for i in range(args.analysers):
    analysers.append(Analyser(frame_queue, stop_event, f"Analyser_{i}"))


command_queue: CommandQueue = CommandQueue(analysers)

commander: Commander = Commander(command_queue, stop_event, "Commander")

logger.info("All Modules Initialised")

logger.info("Starting all Threads...")
sniffer.start()

for analyser in analysers:
    analyser.start()

commander.start()
logger.info("All Threads Started")

try:
    while True:
        sleep(.1)
except KeyboardInterrupt:
    logger.info("Caught Keyboard Interrupt, Stopping all services...")
    stop_event.set()

    sniffer.join()

    for analyser in analysers:
        analyser.join()

    commander.join()
