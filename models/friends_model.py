#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: friends_model.py
@time: 8/23/18 11:00 PM
"""
from __future__ import print_function
from __future__ import unicode_literals

from obj.util.mongo_model.model import MongoDBModel
from sanic.exceptions import SanicException
import datetime as dt
from bson import ObjectId


class FriendModel(MongoDBModel):
    coll_name = "friend"

    async def add(self, id1, id2):
        """
        add friend relationship between id and id2
        :param id1:
        :param id2:
        :return:
        """
        if await self.check_is_friend(id1, id2):
            return True
        else:
            await self.create({"myself": ObjectId(id1), "friend": ObjectId(id2)})
        return True

    async def check_is_friend(self, id1, id2):
        docs = await self.find(myself=ObjectId(id1), friend=ObjectId(id2))
        count = len(docs)
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
        docs = await self.find(myself=ObjectId(id1), friend=ObjectId(id2))
        count = len(docs)
        if count == 1:
            self.remove_by_id(docs[0]["_id"])
        return True
