#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: consumerServer.py
@time: 9/3/18 1:55 AM
"""
from models.user_model import UserModel
from user.services.CheckServices import CheckServer
import logging
# from sanic import worker

logger = logging.getLogger("user")


async def process(consumer, app):
    print("in ")
    consumer_server = ConsumerServer(app)
    async for msg in consumer:
        print("awit ")
        print("consumed: ", msg.topic, msg.partition, msg.offset,
              msg.key, msg.value, msg.timestamp)
        # logger.debug(msg.value)
        # logger.error(msg.value)
        # logger.info(msg.value)
        await consumer_server.route(data=msg.value, topic_name=msg.topic)


class ConsumerServer:
    def __init__(self, app):
        self.collection = app.mongo["account_center"].user
        self.user_model = UserModel(self.collection)

    async def route(self, data, topic_name):
        if topic_name == "article":
            if "type" in data:
                # assert "user_id" in data.keys(), ""
                # check user_id
                check_server = CheckServer()
                try:
                    res = await check_server.is_user(data["messages"]["user_id"], self.user_model)
                except Exception as e:
                    return None
                if data["type"] == "-1":
                    await self.delete_article(data)
                if data["type"] == "1":
                    await self.add_article(data)

    async def add_article(self, data):
        """
        {"type":"1","routes":"clst\/desd",
        "messages":{"article_id":"5b8cf3249dc6d62990471aac","user_id":"5b84f3c95f627db143f2493d"},"
        topic":"article"}
        :param data:
        :return:
        """
        print(data["messages"]["user_id"], " add article count")
        await self.user_model.update_article_count(data["messages"]["user_id"])
        pass

    async def delete_article(self, data):
        """
        {"type":"-1","routes":"clst\/desd",
        "messages":{"article_id":"5b8cf3249dc6d62990471aac","user_id":"5b84f3c95f627db143f2493d"},"
        topic":"article"}
        :param data:
        :return:
        """
        await self.user_model.sub_article_count(data["messages"]["user_id"])
        pass
