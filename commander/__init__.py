#!/usr/bin/env python3
# https://github.com/ReturnOfTheLast/p3_iot_traffic_controller

from queuemanager import CommandQueue
from logger import LoggingObject
from threading import Thread, Event
from queue import Empty


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
        self.logger.info("Commander Initialised")

    def run(self):
        while not self.stop_event.is_set():
            try:
                command = self.command_queue.get(timeout=10)
            except Empty:
                self.logger.debug("No Command Available")
                continue

            self.logger.info("Got a command")
            self.logger.debug(f"Command: {command}")
            # TODO: Structure of commands and how to
            # convert it into a Rule on the chain

        self.logger.info("Commander has Stopped")
