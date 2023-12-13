#!/usr/bin/env python3
# https://github.com/ReturnOfTheLast/p3_iot_traffic_controller

from redis import Redis
from os import environ
from datetime import datetime
import requests
import re


def from_network(ip_address: str) -> bool:
    return re.match(r'^10\.10\.0\.[0-9]*$', ip_address)


def get_ip_location(ip_address: str):
    try:
        r = requests.get(
            f"https://freeipapi.com/api/json/{ip_address}")
    except Exception as e:
        return None, e

    if r.status_code != 200:
        return None, Exception(f"Failed Status code: {r.status_code}")

    return r.json(), None


def whiteblacklisted(ip_address: str) -> bool:
    redis = Redis(environ['REDIS_HOST'], environ['REDIS_PORT'])
    if redis.get(f'list_{ip_address}'):
        return True
    return False


def notify(ip_address: str):
    date: str = datetime.now().strftime("%c")
    requests.post("http://localhost:8080/api/notify", json={
        'message': f'{ip_address} has been banned at {date}',
        'priority': 10
    })
