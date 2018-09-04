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
        elif data_type == "user":
            return await self.search_users(collection, data)
        else:
            raise SanicException("参数错误")

    async def search_users(self, collection, data):
        """

        :param collection:
        :param data:
        :return:
        """
        offset = (data["page_num"] - 1) * data["page_size"]
        key_words = data.get("key_words", "")
        return await collection.find_user_by_name(offset=offset, key_words=key_words,
                                                  page_size=data["page_size"])

    async def search_followers(self, collection, data):
        # my fans, how much p follow me, loging user fans
        # following

        offset = (data["page_num"] - 1) * data["page_size"]
        print("offset ", offset)
        key_words = data.get("key_words", "")
        # res = await collection.find_list(following_user_id=data["user_id"]).skip(offset).to_list(data["page_size"])
        # res = await collection.find_list(following_user_id=data["user_id"]).to_list(data["page_size"])
        # return res
        return await collection.find_followers_by_name_and_user_id(user_id=data["user_id"], offset=offset,
                                                                   key_words=key_words, page_size=data["page_size"])

    async def search_following(self, collection, data):
        """
        how much p user id following, logging user following
        myself=user id
        :param collection:
        :param data:
        :return:
        """
        offset = (data["page_num"] - 1) * data["page_size"]
        print("offset is ", offset, data)
        key_words = data.get("key_words", "")
        # return await collection.find_list(myself_user_id=data["user_id"]).skip(offset).to_list(data["page_size"])

        # user_id, offset, key_words="", page_size=20
        return await collection.find_following_by_name_and_user_id(user_id=data["user_id"], offset=offset,
                                                                   key_words=key_words, page_size=data["page_size"])

    async def search_friend(self, collection, data):
        offset = (data["page_num"] - 1) * data["page_size"]
        key_words = data.get("key_words", "")
        # return await collection.raw_find({'myself': data["user_id"]}).skip(offset).to_list(data["page_size"])
        return await collection.find_friends_by_name_and_user_id(user_id=data["user_id"], offset=offset,
                                                                 key_words=key_words, page_size=data["page_size"])
