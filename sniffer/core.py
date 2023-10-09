#!/usr/bin/env python3
# https://github.com/ReturnOfTheLast/p3_iot_traffic_controller

# Inspired by and burrowing from https://github.com/EONRaider/Packet-Sniffer

import itertools
import logging
from socket import PF_PACKET, SOCK_RAW, ntohs, socket
from typing import Iterator


class Sniffer:
    def __init__(self, interface: str):
        self.interface = interface

    def _bind_interface(self, sock: socket):
        if self.interface is not None:
            sock.bind((self.interface, 0))

    def execute(self) -> Iterator:
        with socket(PF_PACKET, SOCK_RAW, ntohs(0x0003)) as sock:
            self._bind_interface(sock)
            logging.info("Listening for frames")
            for frame_num in itertools.count(1):
                frame = sock.recv(9000)
                logging.info(f"Received a {len(frame)} bytes frame")
                yield (frame_num, frame)
