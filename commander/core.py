#!/usr/bin/env python3
# https://github.com/ReturnOfTheLast/p3_iot_traffic_controller

from queuemanager.core import CommandQueue
from logger import LoggingObject
from iptc import Chain, Table, Target, Rule


class Commander(LoggingObject):
    def __init__(self, command_queue: CommandQueue):
        self.command_queue: CommandQueue = command_queue
        self.logger.info("Commander initiating...")

        self.logger.info("Creating custom chain")
        self.table = Table(Table.FILTER)
        self.logger.debug(f"Table: \n{self.table}")
        self.sec_chain = self.table.create_chain("SEC-CHAIN")
        self.logger.debug(f"Chain: \n{self.sec_chain}")
        self.logger.info("Making the FORWARD chain check our chain first")
        jump_rule = Rule()
        sec_chain_target = Target(jump_rule, self.sec_chain.name)
        jump_rule.target = sec_chain_target
        forward_chain = Chain(self.table, "FORWARD")
        forward_chain.insert_rule(jump_rule)

    def run(self):
        while True:
            command = self.command_queue.get()
            self.logger.info("Got a command")
            self.logger.debug(f"Command: {command}")
            # TODO: Structure of commands and how to
            # convert it into a Rule on the chain
