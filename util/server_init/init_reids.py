#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: init_reids.py
@time: 8/29/18 1:08 AM
"""
import json
from marshmallow import Schema, fields


class InitSchema(Schema):
    head_portrait = fields.Str()
    name = fields.Str()


class InitRedis:
    def __init__(self, redis, user_model):
        self.init_user_info_keys = ["head_portrait", "name"]
        self.redis = redis
        self.user_model = user_model
        pass

    async def _gen_user_info(self, doc):
        res_data = {}
        for field in self.init_user_info_keys:
            res_data[field] = doc.get(field, None)

        return res_data

    async def add_user_info_to_redis(self, page_docs):
        for doc in page_docs:
            key = "{}_user_info".format(str(doc["_id"]))
            values = await self._gen_user_info(doc)
            # print("values is ", values)
            await self.redis.set(key, json.dumps(values))
        # schema = InitSchema(many=True)
        # data = schema.load(page_docs).data
        # print("data is ")
        # print(data)

    async def init_user_info_to_redis(self):
        """
        init all user info by info keys to redis
        :return:
        """
        step = 100
        times = 0
        while True:
            offset = step * times
            page_docs = await self.user_model.find_list().skip(offset).to_list(step)
            await self.add_user_info_to_redis(page_docs)
            if len(page_docs) < step:
                break
            times += 1
        # c = self.user_model.find_list()
        # print(type(c))
        # print(c)
        # print(dir(c))
        # pass
