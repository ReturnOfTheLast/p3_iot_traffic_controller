#!/usr/bin/env python3
# https://github.com/ReturnOfTheLast/p3_iot_traffic_controller

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.cursor import Cursor
from redis import Redis
from os import environ


def restore_redis_cache():
    db_client: MongoClient = MongoClient(environ["MONGO_URI"])
    redis_client = Redis(environ["REDIS_HOST"], environ["REDIS_PORT"], 0)

    db: Database = db_client["iotwarden"]
    collection: Collection = db["whiteblacklist"]

    cursor: Cursor = collection.find({})

    for document in cursor:
        redis_client.set(document["ip"], document["allowed"])
