#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: setting.py
@time: 8/5/18 8:25 PM
"""

import os
import json
from sanic import Sanic, request, response
from sanic.exceptions import SanicException
import aioredis
from sanic_cors import CORS, cross_origin
import asyncio
from obj.database.mongo_database.mongo import Core as Mongo
from obj.user.user_marshal import UserResister
# from sanic_mongo import Mongo
from obj.util.responsePack import response_package
from obj.models.user_model import UserModel
from obj.util.tools import format_res
from kafka import KafkaProducer, KafkaConsumer
from obj.util.config import kafka_host
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import sys
from obj.util.config import BASE_DIR, REDIS_CONFIG

app = Sanic()
CORS(app, automatic_options=True, origins="*", send_wildcard=True)
app.config.update(REDIS_CONFIG)
# logging.getLogger（' sanic_cors '）。level = logging。DEBUG
app.static('/static', os.path.join(BASE_DIR, "static"))
# app.static('/favicon.ico', '../static/img/favicon.ico')
# app.static('/fa.ico', './s/favicon.ico')
# app.debug = False

mongo_uri = "mongodb://{host}:{port}/{database}".format(
    database='account_center',
    port=27017,
    host='localhost'
)
Mongo.SetConfig(app, account_center=mongo_uri)
Mongo(app)


@app.exception(SanicException, AssertionError)
@cross_origin(app, automatic_options=True, origins="*", send_wildcard=True)
async def process_exception(request, exception):
    status_code = str(getattr(exception, "status_code", "500"))
    # return json(response_package(status_code, exception.args))
    print(exception.args)
    return response.json(
        response_package(str(status_code), results=str(exception.args), message=format_res(exception.args)))
    # return json(response_package(str(status_code), results=exception.args))


async def consume(loop):
    consumer = AIOKafkaConsumer(
        'user',
        loop=loop, bootstrap_servers=kafka_host,
        group_id="my-group")
    # Get cluster layout and join group `my-group`
    await consumer.start()
    try:
        # Consume messages
        async for msg in consumer:
            print("consumed: ", msg.topic, msg.partition, msg.offset,
                  msg.key, msg.value, msg.timestamp)
    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()


async def process(consumer):
    print("in ")
    async for msg in consumer:
        print("awit ")
        print("consumed: ", msg.topic, msg.partition, msg.offset,
              msg.key, msg.value, msg.timestamp)


@app.listener('before_server_start')
async def server_init(app, loop):
    app.redis = await aioredis.create_redis_pool(app.config['redis'])
    # app.producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    #                              bootstrap_servers=kafka_host)
    # app.consumer = KafkaConsumer("user", bootstrap_servers=kafka_host, group_id="group111",
    #                              value_deserializer=lambda m: json.loads(m.decode('ascii')),
    #                              consumer_timeout_ms=1000)
    app.producer = AIOKafkaProducer(loop=loop, value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                                    bootstrap_servers=kafka_host)
    app.consumer = AIOKafkaConsumer(
        'user',
        loop=loop, bootstrap_servers=kafka_host,
        group_id="my-group4343")
    await app.producer.start()
    # await app.consumer.start()
    # await process(app.consumer)
    # async for msg in app.consumer:
    #     print("consumed: ", msg.topic, msg.partition, msg.offset,
    #           msg.key, msg.value, msg.timestamp)
    # loop.run_until_complete(consume(loop))


DATABASE_CONIFG = {
    "host": "localhost",
    "port": 27017,
    "name": "account_center",
}

secret = "F%^%$%czx76$%^a"

# INITIALIZE_CONFIG = {
#     # "authenticate": authenticate,
#     # "path_to_authenticate": '/login',
#     # "cookie_domain": "sendMe.com",
#     # "cookie_set": True,
#     'expiration_delta': 60 * 30,
#     # "retrieve_user": retrieve_user,
#     'debug': True,
#     # "extend_payload": my_extender,
#
#     # payload
#     "claim_aud": "sendMe.com",
#     "claim_iat": True,
#     "claim_iss": 'ls',
#     "secret": secret,
# }
