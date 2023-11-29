#!/usr/bin/env python3
# https://github.com/ReturnOfTheLast/p3_iot_traffic_controller

import requests
import re


def from_network(ip_address: str) -> bool:
    return re.match(r'^10\.10\.0\.[0-9]*$', ip_address)


def get_ip_location(ip_address: str) -> dict[str, str | int] | None:
    r = requests.get(f'https://geolocation-db.com/json/{ip_address}')
    if r.status_code != 200:
        return None

    return r.json()
