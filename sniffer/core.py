#!/usr/bin/env python3
# https://github.com/ReturnOfTheLast/p3_iot_traffic_controller

# Inspired by and burrowing from https://github.com/EONRaider/Packet-Sniffer

from logger import get_logger
from sniffer.handlers import FramePublisher
from socket import PF_PACKET, SOCK_RAW, ntohs, socket
from typing import Iterator
from logging import Logger
import itertools


class Sniffer(FramePublisher):
    """A frame-sniffer
    """

    def __init__(self, interface: str):
        """Sniffer constructor

        Args:
            interface (str): Interface to sniff on
        """
        FramePublisher.__init__(self)
        self.interface: str = interface
        self.logger:  Logger = get_logger(
            f"{self.__module__}.{self.__class__.__qualname__}")

    def _bind_interface(self, sock: socket):
        """Internal method to bind the socket to interface

        Args:
            sock (socket): socket to bind
        """
        if self.interface is not None:
            self.logger.info(f"Binding interface to {self.interface}")
            sock.bind((self.interface, 0))

    def execute(self):
        """Sniff for frames and publish them
        """
        with socket(PF_PACKET, SOCK_RAW, ntohs(0x0003)) as sock:
            self._bind_interface(sock)
            self.logger.info("Listening for frames")
            for frame_num in itertools.count(1):
                frame: bytes = sock.recv(9000)
                self.logger.info(f"Received a {len(frame)} bytes frame")
                self._notify_all((frame_num, frame))
