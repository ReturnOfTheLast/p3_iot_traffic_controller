from netprotocols import Ethernet, IPv4, TCP, UDP, Protocol


def dissect(frame: bytes) -> dict[str, Protocol]:
    output = {}
    output['Ethernet'] = Ethernet.decode(frame)

    def get_next_layer(current: str, rhl: int) -> tuple[str, int] | None:
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
