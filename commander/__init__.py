#!/usr/bin/env python3
# https://github.com/ReturnOfTheLast/p3_iot_traffic_controller

from queuemanager import CommandQueue
from logger import LoggingObject
from threading import Thread


class Commander(LoggingObject, Thread):
    def __init__(self, command_queue: CommandQueue):
        Thread.__init__(self)
        self.command_queue: CommandQueue = command_queue
        self.logger.info("Commander initiating...")

    def run(self):
        while True:
            command = self.command_queue.get()
            self.logger.info("Got a command")
            self.logger.debug(f"Command: {command}")
            # TODO: Structure of commands and how to
            # convert it into a Rule on the chain
