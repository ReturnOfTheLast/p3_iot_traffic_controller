#!/usr/bin/env python3
# https://github.com/ReturnOfTheLast/p3_iot_traffic_controller

from queuemanager.core import CommandQueue
from logger import get_logger
from logging import Logger


class Commander:
    def __init__(self, command_queue: CommandQueue):
        self.command_queue: CommandQueue = command_queue
        self.logger: Logger = get_logger(
            f"{self.__module__}.{self.__class__.__qualname__}")

        self.logger.info("Commander initiating...")
        # TODO: Add custom chain to IPTables

    def run(self):
        while True:
            command = self.command_queue.get()
            self.logger.info("Got a command")
            self.logger.debug(f"Command: {command}")
            # TODO: Structure of commands and how to
            # convert it into a Rule on the chain
