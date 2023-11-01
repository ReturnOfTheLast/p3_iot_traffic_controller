#!/usr/bin/env python3
# https://github.com/ReturnOfTheLast/p3_iot_traffic_controller

from queuemanager.core import CommandQueue
from logger import get_logger
from pyptables.tables import Tables, Table
from pyptables.chains import UserChain, BuiltinChain
from pyptables.rules import Jump
from logging import Logger


class Commander:
    def __init__(self, command_queue: CommandQueue):
        self.command_queue: CommandQueue = command_queue
        self.logger: Logger = get_logger(
            f"{self.__module__}.{self.__class__.__qualname__}")

        self.logger.info("Commander initiating...")
        self.logger.info("Creating tables object...")
        self.tables: Tables = Tables(
            Table('filter', BuiltinChain('FORWARD', 'ACCEPT')))

        self.logger.debug(f"Tables: {self.tables}")

        self.logger.info("Creating custom chain...")
        self.sec_chain: UserChain = UserChain(
            'sec_chain',
            comment="Security Chain for Filtering"
        )
        self.logger.debug(f"Chain: {self.sec_chain}")

        self.logger.info("Adding sec_chain to the filter table...")
        self.tables['filter'].append(self.sec_chain)

        self.logger.info("Adding a Jump from FORWARD to our chain...")
        self.tables['filter']["FORWARD"].insert(0, Jump(self.sec_chain))

        self.logger.debug(f"Finished tables: {self.tables}")

        self.logger.info("Generating IPTables command...")
        iptables_command: bytes = self.tables.to_iptables().encode('UTF-8')
        self.logger.debug(f"IPTables command: {iptables_command}")

    def run(self):
        while True:
            command = self.command_queue.get()
            self.logger.info("Got a command")
            self.logger.debug(f"Command: {command}")
            # TODO: Structure of commands and how to
            # convert it into a Rule on the chain
