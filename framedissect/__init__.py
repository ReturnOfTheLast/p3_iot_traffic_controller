#!/usr/bin/env python3
# https://github.com/ReturnOfTheLast/p3_iot_traffic_controller

from netprotocols import (
    Protocol,
    Ethernet,
    IPv4,
    IPv6,
    ICMPv4,
    ICMPv6,
    TCP,
    UDP,
    ARP
)


def dissect(frame: bytes) -> tuple[int, dict[str, Protocol]]:
    """Dissect a frame

    Args:
        frame (bytes): Frame to dissect

    Returns:
        dict[str, Protocol]: Dictionary of protocols
    """
    output: dict[str, Protocol] = dict()
    output['Ethernet']: Protocol = Ethernet.decode(frame)

    def get_next_layer(current: str, rhl: int) -> tuple[int, str] | None:
        """Unwrap the next layer of the frame

        Args:
            current (str): Name of current protocol
            rhl (int): Running header length

        Returns:
            tuple[str, int] | None: Name of the next protocol \
            and header_len thereof
        """
        c_proto: Protocol = output[current]
        if c_proto.encapsulated_proto in (None, "undefined"):
            return None
        next: str = c_proto.encapsulated_proto
        if hasattr(c_proto, 'ihl'):
            hl: int = c_proto.ihl
        else:
            hl: int = c_proto.header_len

        try:
            output[next]: Protocol = globals()[next].decode(frame[hl+rhl:])
        except KeyError:
            # Dont know the next layer
            return None

        return hl, next

    rhl: int = 0
    current: str = 'Ethernet'
    while True:
        out: tuple[str, int] = get_next_layer(current, rhl)

        if out is None:
            break

        rhl += out[0] 
        current: str = out[1]

    return rhl, output


def __fthelinter__():
    IPv4
    IPv6
    ICMPv4
    ICMPv6
    TCP
    UDP
    ARP
