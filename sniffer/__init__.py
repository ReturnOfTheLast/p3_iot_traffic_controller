#!/usr/bin/env python3
# https://github.com/ReturnOfTheLast/p3_iot_traffic_controller

# Inspired by and burrowing from https://github.com/EONRaider/Packet-Sniffer

from pubsub import Publisher
from threading import Thread, Event
from socket import PF_PACKET, SOCK_RAW, ntohs, socket
import itertools


class Sniffer(Publisher, Thread):
    """A frame-sniffer
    """

    def __init__(
        self,
        interface: str,
        stop_event: Event,
        name: str = None
    ):
        """Sniffer constructor

        Args:
            interface (str): Interface to sniff on
        """
        Publisher.__init__(self)
        Thread.__init__(self, name=name)
        self.interface: str = interface
        self.stop_event: Event = stop_event

    def _bind_interface(self, sock: socket):
        """Internal method to bind the socket to interface

        Args:
            sock (socket): socket to bind
        """
        if self.interface is not None:
            self.logger.info(f"Binding interface to {self.interface}")
            sock.bind((self.interface, 0))

    def run(self):
        """Sniff for frames and publish them
        """
        with socket(PF_PACKET, SOCK_RAW, ntohs(0x0003)) as sock:
            self._bind_interface(sock)
            self.logger.info("Listening for frames")
            for frame_num in itertools.count(1):
                if self.stop_event.is_set():
                    break
                frame: bytes = sock.recv(9000)
                self.logger.info(f"Received a {len(frame)} bytes frame")
                self._notify_all((frame_num, frame))

        self.logger.info("Sniffer has stopped")
