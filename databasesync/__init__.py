#!/usr/bin/env python3
# https://github.com/ReturnOfTheLast/p3_iot_traffic_controller

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.cursor import Cursor
from redis import Redis
from os import environ


def restore_redis_cache():
    db_client = MongoClient(environ['MONGO_URI'])
    redis_client = Redis(environ['REDIS_HOST'], environ['REDIS_PORT'], 0)

    db: Database = db_client['iotwarden']
    collection: Collection = db['whiteblacklist']

    cursor: Cursor = collection.find()

    for document in cursor:
        redis_client.set(f"list_{document['ip']}", document['allowed'])


def sync_redis_to_mongo():
    db_client = MongoClient(environ['MONGO_URI'])
    redis_client = Redis(environ['REDIS_HOST'], environ['REDIS_PORT'], 0)

    db: Database = db_client['iotwarden']

    # Syncing White/Black list
    collection: Collection = db['whiteblacklist']

    docs = []

    for key in redis_client.scan_iter():
        if key[:5] == "list_":
            if collection.find_one({"ip": key[5:]}):
                continue

            docs.append({
                "ip": key[5:],
                "allowed": redis_client.get(key)
            })

    collection.insert_many(docs)
