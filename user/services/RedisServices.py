#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: RedisServices.py
@time: 8/23/18 3:08 AM
"""


class RedisServer:

    async def gene_key(self, user_id, name):
        return "{}_{}".format(user_id, name)

    async def created_or_update_list(self, redis, key, unit):
        res = await redis.lpush(key, unit)
