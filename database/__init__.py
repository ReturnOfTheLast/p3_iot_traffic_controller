#!/usr/bin/env python3
# https://github.com/ReturnOfTheLast/p3_iot_traffic_controller

from pubsub import Publisher, Subscriber
from redis import Redis
from os import environ


class DatabaseWriter(Subscriber, Redis):

    def __init__(
        self,
        publishers: Publisher
    ):
        self.logger.info("Initialising Database Writer")
        Subscriber.__init__(self, publishers)
        Redis.__init__(self, environ["REDIS_HOST"], environ["REDIS_PORT"])
        self.logger.debug(f"Attached Stop Event:\n{self.stop_event}")
        self.logger.info("Database Writer Initialised")

    def update(self, key):
        self.set(f"list_{key}", True)
