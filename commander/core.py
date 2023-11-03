#!/usr/bin/env python3
# https://github.com/ReturnOfTheLast/p3_iot_traffic_controller

from queuemanager.core import CommandQueue
from logger import LoggingObject
from nftables import Nftables
import json


class Commander(LoggingObject):
    def __init__(self, command_queue: CommandQueue):
        self.command_queue: CommandQueue = command_queue
        self.logger.info("Commander initiating...")
        self.nft = Nftables()
        self.nft.set_json_output(True)
        self.chain_name = "SEC-CHAIN"
        self.nft.cmd(f"add chain inet filter {self.chain_name}")
        self.nft.cmd(f"insert rule filter FORWARD 0 jump {self.chain_name}")

    def run(self):
        while True:
            command = self.command_queue.get()
            self.logger.info("Got a command")
            self.logger.debug(f"Command: {command}")
            # TODO: Structure of commands and how to
            # convert it into a Rule on the chain
