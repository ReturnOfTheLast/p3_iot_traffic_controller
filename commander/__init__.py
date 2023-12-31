#!/usr/bin/env python3
# https://github.com/ReturnOfTheLast/p3_iot_traffic_controller

from queuemanager import CommandQueue
from logger import LoggingObject
from utils import notify
from threading import Thread, Event
from queue import Empty
from os import environ
import dbus


class Commander(LoggingObject, Thread):
    def __init__(
        self,
        command_queue: CommandQueue,
        stop_event: Event,
        name: str = None
    ):
        self.logger.info("Initialising Commander...")
        Thread.__init__(self, name=name)
        self.command_queue: CommandQueue = command_queue
        self.stop_event: Event = stop_event
        self.logger.debug(f"Attached Stop Event:\n{self.stop_event}")
        bus = dbus.SystemBus()
        self.firewalld = bus.get_object(
            'org.fedoraproject.FirewallD1',
            '/org/fedoraproject/FirewallD1'
        )
        self.logger.debug(f"Connected to firewalld dbus:\n{self.firewalld}")
        self.logger.info("Commander Initialised")

    def run(self):
        while not self.stop_event.is_set():
            try:
                ip: str = self.command_queue.get(timeout=10)
            except Empty:
                self.logger.debug("No Command Available")
                continue

            self.logger.info("Got a command")
            self.logger.debug(f"Command: {ip}")

            orig_policy = self.firewalld.get_dbus_method("getPolicySettings")(
                environ["FIREWALLD_POLICY"]
            )
            self.logger.debug(f"Current Settings for Policy:\n{orig_policy}")

            rich_rules = []
            if orig_policy.get('rich_rules', None):
                rich_rules.extend(
                    [str(x) for x in list(orig_policy['rich_rules'])])

            self.logger.debug(f"rich_rules:\n{rich_rules}")

            new_rule = f'rule family="ipv4" destination address="{ip}" drop'
            self.logger.debug(f"new_rule:\n{new_rule}")

            if new_rule in rich_rules:
                self.logger.info("Rule already exists")
                continue

            rich_rules.append(new_rule)

            self.logger.debug(f"rich_rules:\n{rich_rules}")

            change_policy = {
                'rich_rules': rich_rules
            }

            self.logger.debug(f"New Policy Settings:\n{change_policy}")
            self.firewalld.get_dbus_method("setPolicySettings")(
                environ["FIREWALLD_POLICY"],
                change_policy
            )
            self.logger.info("Added new rule")

            self.logger.info("Sending notification to users")
            notify(ip)

        self.logger.info("Commander has Stopped")
