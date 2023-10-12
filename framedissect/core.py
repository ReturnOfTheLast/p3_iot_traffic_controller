from netprotocols import Ethernet, IPv4, TCP, UDP, Protocol

def dissect(frame: bytes) -> dict[str, Protocol]:
    output = {}
    output['Ethernet'] = Ethernet.decode(frame)

    def get_next_layer(current: str, rhl: int) -> tuple[str, int] | None:
        if hasattr(output[current], 'encapsulated_proto'):
            next = output[current].encapsulated_proto
            hl = output[current].ihl if hasattr(output[current], 'ihl') else output[current].header_len
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
