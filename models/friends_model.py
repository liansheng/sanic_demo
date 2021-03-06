#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: friends_model.py
@time: 8/23/18 11:00 PM
"""
from __future__ import print_function
from __future__ import unicode_literals

import copy

from pypinyin import lazy_pinyin

from util.mongo_model.model import MongoDBModel
from sanic.exceptions import SanicException
import datetime as dt
from bson import ObjectId


class FriendModel(MongoDBModel):
    coll_name = "friend"

    # async def add(self, id1, id2):
    #     """
    #     add friend relationship between id and id2
    #     id1 following id2
    #     :param id1:
    #     :param id2:
    #     :return:
    #     """
    #     if await self.check_is_friend(id1, id2):
    #         return True
    #     else:
    #         await self.create({"myself": id1, "friend": id2})
    #     return True

    async def add_data(self, data1, data2):
        """
        add friend relationship between id and id2
        id1 following id2
        :param data1: {'myself_head_portrait': '/static/img/default_head_portrait.jpg',
                'myself_name': 'fawoaKNNgOTx', 'myself_user_id': '5b7e29dd5f627d0218528819'}
        :param data2: {'friend_head_portrait': '/static/img/default_head_portrait.png',
                'friend_name': 'fawoM7zemXN7', 'friend_user_id': '5b7cfbd45f627ddd88e2c929'}
        :return:
        """
        if await self.check_is_friend(data1["myself_user_id"], data2['friend_user_id']):
            return True
        else:
            new_data = copy.deepcopy(data1)
            new_data.update(data2)
            await self.create(new_data)
        return True

    async def get_friends_count(self, user_id):
        """
        :param user_id:
        :return:
        """
        return await self.collection.count_documents({"myself_user_id": user_id})

    async def check_is_friend(self, id1, id2):
        """
        check two people are friends
        :param id1:
        :param id2:
        :return: friends is True, not a friends is False
        """
        count = await self.collection.count_documents({"myself_user_id": id1, "friend_user_id": id2})
        if count == 1:
            return True
        else:
            return False

    async def remove(self, id1, id2):
        """
        remove friend relationship between id1 and id2
        :param id1:
        :param id2:
        :return:
        """
        docs = await self.find(myself_user_id=id1, friend_user_id=id2)
        count = len(docs)
        if count == 1:
            self.remove_by_id(docs[0]["_id"])
        return True

    async def find_friends_by_name_and_user_id(self, user_id, offset, key_words="", page_size=20):
        """
        docs = await self.collection.find(
            {"$or":
                [{"friend_name": {'$regex': key_words}, 'myself_user_id': user_id},
                 {"myself_name": {'$regex': key_words}, 'friend_user_id': user_id}]
            }
        ).skip(offset).to_list(page_size)

        :param user_id:
        :param offset:
        :param key_words:
        :param page_size:
        :return:
        """
        docs = await self.collection.find(
            {"friend_name": {'$regex': key_words}, 'myself_user_id': user_id}
        ).skip(offset).to_list(page_size)
        return docs

    async def update_name(self, user_id, new_name):
        await self.update_friend_name(user_id, new_name)
        res = await self.update_myself_name(user_id, new_name)
        return res

    async def update_friend_name(self, user_id, new_name):
        criteria = {"friend_user_id": user_id}
        obj_new = {"$set": {"friend_name": new_name}}
        return await self.update_many(criteria, obj_new)

    async def update_myself_name(self, user_id, new_name):
        criteria = {"myself_user_id": user_id}
        obj_new = {"$set": {"myself_name": new_name}}
        return await self.update_many(criteria, obj_new)

    async def update_head(self, user_id, sum_path):
        """
        :param user_id:
        :param sum_path:
        :return:
        """
        await self.update_myself_head(user_id, sum_path)
        res = await self.update_friend_head(user_id, sum_path)
        return res

    async def update_friend_head(self, user_id, path):
        """
        :param user_id:
        :param path:
        :return:
        """
        criteria = {"friend_user_id": user_id}
        obj_new = {"$set": {"friend_head_portrait": path}}
        return await self.update_many(criteria, obj_new)

    async def update_myself_head(self, user_id, path):
        """
        :param user_id:
        :param path:
        :return:
        """
        criteria = {"myself_user_id": user_id}
        obj_new = {"$set": {"myself_head_portrait": path}}
        return await self.update_many(criteria, obj_new)
