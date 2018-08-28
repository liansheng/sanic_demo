#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: SearchService.py
@time: 8/27/18 2:32 AM
"""
from bson import ObjectId
from sanic.exceptions import SanicException


class SearchServices:
    async def search_user(self, collection, data):
        data_type = data["type"]
        if data_type == "followers":
            return await self.search_followers(collection, data)
        elif data_type == "following":
            return await self.search_following(collection, data)
        elif data_type == "friend":
            return await self.search_friend(collection, data)
        else:
            raise SanicException("参数错误")

    async def search_followers(self, collection, data):
        # my fans, how much p follow me,
        # following

        offset = (data["page_num"] - 1) * data["page_size"]
        res = await collection.find_list(following=data["user_id"]).skip(offset).to_list(data["page_size"])
        return res

    async def search_following(self, collection, data):
        """
        how much p user id following
        myself=user id
        :param collection:
        :param data:
        :return:
        """
        offset = (data["page_num"] - 1) * data["page_size"]
        print("offset is ", offset, data)
        return await collection.find_list(myself=data["user_id"]).skip(offset).to_list(data["page_size"])

    async def search_friend(self, collection, data):
        offset = (data["page_num"] - 1) * data["page_size"]
        return await collection.raw_find({'myself': data["user_id"]}).skip(offset).to_list(data["page_size"])
