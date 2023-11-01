#!/usr/bin/env python3
# https://github.com/ReturnOfTheLast/p3_iot_traffic_controller

from queuemanager.core import CommandQueue
from logger import get_logger
from pyptables.tables import Tables, Table
from pyptables.chains import UserChain, BuiltinChain
from pyptables.rules import Jump
from logging import Logger
from subprocess import Popen, PIPE


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

        self.logger.info("Generating our IPTables config...")
        iptables_custom_conf: str = self.tables.to_iptables()
        self.logger.debug(f"IPTables config: \n{iptables_custom_conf}")

        self.logger.info("Getting the Original config...")
        iptables_save_proc: Popen = Popen(
            ["iptables-save"],
            stdin=None,
            stdout=PIPE,
            stderr=PIPE
        )
        iptables_orig_conf, stderr = iptables_save_proc.communicate()
        iptables_orig_conf: str = iptables_orig_conf.decode()
        self.logger.debug(f"Original config: \n{iptables_orig_conf}")
        self.logger.debug(f"STDERR: \n{stderr}")

        self.logger.info("Saving Original config to original_iptables.conf...")
        with open("original_iptables.conf", "w") as fp:
            fp.write(iptables_orig_conf)

        self.logger.info("Generating new config...")
        iptables_new_conf: str = iptables_orig_conf \
            + "\n" + iptables_custom_conf
        self.logger.debug(f"New config: \n{iptables_new_conf}")

        self.logger.info("Applying the config...")
        iptables_restore_proc: Popen = Popen(
            ["iptables-restore"],
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE
        )
        stdout, stderr = iptables_restore_proc.communicate(
            input=iptables_new_conf.encode()
        )
        self.logger.debug(f"STDOUT: \n{stdout}")
        self.logger.debug(f"STDERR: \n{stderr}")

    def run(self):
        while True:
            command = self.command_queue.get()
            self.logger.info("Got a command")
            self.logger.debug(f"Command: {command}")
            # TODO: Structure of commands and how to
            # convert it into a Rule on the chain
