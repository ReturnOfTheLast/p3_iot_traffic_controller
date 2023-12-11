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
        redis_client.set(
            f"list_{document['ip']}",
            'white' if document['allowed'] else 'black'
        )


def sync_redis_to_mongo():
    db_client = MongoClient(environ['MONGO_URI'])
    redis_client = Redis(environ['REDIS_HOST'], environ['REDIS_PORT'], 0)

    db: Database = db_client['iotwarden']

    # Syncing White/Black list
    collection: Collection = db['whiteblacklist']

    docs = []

    for key in redis_client.scan_iter():
        str_key = key.decode()
        if str_key[:5] == "list_":
            if collection.find_one({"ip": str_key[5:]}):
                continue

            allowed = redis_client.get(str_key) == 'white'

            docs.append({
                "ip": str_key[5:],
                "allowed": allowed
            })
    if len(docs) > 0:
        collection.insert_many(docs)
