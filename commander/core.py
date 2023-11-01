#!/usr/bin/env python3
# https://github.com/ReturnOfTheLast/p3_iot_traffic_controller

from queuemanager.core import CommandQueue
from logger import get_logger
from pyptables import default_tables, Tables, UserChain
from pyptables.rules import Jump
from logging import Logger


class Commander:
    def __init__(self, command_queue: CommandQueue):
        self.command_queue: CommandQueue = command_queue
        self.logger: Logger = get_logger(
            f"{self.__module__}.{self.__class__.__qualname__}")

        self.logger.info("Commander initiating...")
        self.logger.info("Creating custom chain...")
        self.tables: Tables = default_tables()
        self.sec_chain: UserChain = UserChain(
            "sec_chain",
            comment="Security Chain for Filtering"
        )
        self.tables["filter"].append(self.sec_chain)
        self.logger.info("Attaching chain to FORWARD...")
        self.tables["filter"]["FORWARD"].insert(0, Jump(self.sec_chain))

    def run(self):
        while True:
            command = self.command_queue.get()
            self.logger.info("Got a command")
            # TODO: Structure of commands and how to
            # convert it into a Rule on the chain
