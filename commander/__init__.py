#!/usr/bin/env python3
# https://github.com/ReturnOfTheLast/p3_iot_traffic_controller

from queuemanager import CommandQueue
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
        nft_command = {
            "nftables": [
                {
                    "add": {
                        "chain": {
                            "table": "filter",
                            "name": "SEC-CHAIN"
                        }
                    }
                },
                {
                    "insert": {
                        "rule": {
                            "table": "filter",
                            "chain": "FORWARD",
                            "index": 0,
                            "expr": [
                                {
                                    "jump": {
                                        "target": "SEC-CHAIN"
                                    }
                                }
                            ]
                        }
                    }
                }
            ]
        }
        self.logger.info("Setting up our chain and rules on NFTables...")
        self.logger.debug(
            f"NFTables command: \n{json.dumps(nft_command, indent=2)}")
        rc, output, error = self.nft.json_cmd(nft_command)
        self.logger.debug(f"Return code: {rc}")
        self.logger.debug(f"Output: \n{json.dumps(output, indent=2)}")
        self.logger.debug(f"Error: \n{json.dumps(error, indent=2)}")
        if rc != 0:
            self.logger.info("NFTables command failed (see debug.log)")
            exit(1)
        self.logger.info("Configured NFTables")

    def run(self):
        while True:
            command = self.command_queue.get()
            self.logger.info("Got a command")
            self.logger.debug(f"Command: {command}")
            # TODO: Structure of commands and how to
            # convert it into a Rule on the chain
