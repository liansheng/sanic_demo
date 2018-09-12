#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: update_user_info_to_friend_and_follow.py
@time: 9/3/18 6:38 PM
"""
import json


class UpdateServer:

    async def update_anything(self, k):
        func = getattr(self, "update_{}".format(k))

    async def update_name(self, k, v, user_id, follower_model, friends_model, app, user_model):
        if k == "name":
            await self.update_name_db(v, user_id, follower_model, friends_model)
            await self.update_name_redis(v, user_id, app, user_model)
        pass

    async def update_name_db(self, v, user_id, follower_model, friends_model):
        await follower_model.update_name(user_id, v)
        await friends_model.update_name(user_id, v)

    async def update_name_redis(self, v, user_id, app, user_model):
        """
        :param k:
        :param v:
        :param user_id:
        :param follower_model:
        :param friends_model:
        :return:
        """
        res = await app.redis.get("{}_user_info".format(user_id))
        if res:
            res_json = json.loads(res)
        else:
            res_json = {"name": v, "head_portrait": await user_model.get_head_portrait(user_id)}
        res_json["name"] = v
        await app.redis.set("{}_user_info".format(user_id), json.dumps(res_json))

    async def update_head(self, k, v, user_id, user_model, follower_model, friends_model, app):
        if k == "head":
            await self.update_head_db(v, user_id, user_model, follower_model, friends_model)
            await self.update_head_redis(v, user_id, app)
            pass

    async def update_head_redis(sell, v, user_id, app):
        res = await app.redis.get("{}_user_info".format(user_id))
        res_json = json.loads(res)
        res_json["head_portrait"] = v
        await app.redis.set("{}_user_info".format(user_id), json.dumps(res_json))

    async def update_head_db(self, v, user_id, user_model, follower_model, friend_model):
        """
        :param v:
        :param user_id:
        :param follower_model:
        :param friend_model:
        :return:
        """

        await user_model.update_head(user_id, v)
        await follower_model.update_head(user_id, v)
        await friend_model.update_head(user_id, v)
