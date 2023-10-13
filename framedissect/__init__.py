from netprotocols import Ethernet, IPv4, TCP, UDP, Protocol


def dissect(frame: bytes) -> dict[str, Protocol]:
    """Dissect a frame

    Args:
        frame (bytes): Frame to dissect

    Returns:
        dict[str, Protocol]: Dictionary of protocols
    """
    output = {}
    output['Ethernet'] = Ethernet.decode(frame)

    def get_next_layer(current: str, rhl: int) -> tuple[str, int] | None:
        """Unwrap the next layer of the frame

        Args:
            current (str): Name of current protocol
            rhl (int): Running header length

        Returns:
            tuple[str, int] | None: Name of the next protocol \
            and header_len thereof
        """
        c_proto: Protocol = output[current]
        if hasattr(c_proto, 'encapsulated_proto'):
            next = c_proto.encapsulated_proto
            hl = c_proto.ihl if hasattr(c_proto, 'ihl') else c_proto.header_len
            output[next] = globals()[next].decode(frame[hl+rhl:])
            return next, hl
        return None

    rhl: int = 0
    current: str = 'Ethernet'
    while True:
        out = get_next_layer(current, rhl)

        if out is None:
            break

        current: str = out[0]
        rhl += out[1]

    return output
