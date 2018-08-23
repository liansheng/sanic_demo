#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: user_model.py
@time: 8/16/18 2:23 AM
"""
from __future__ import print_function
from __future__ import unicode_literals

from obj.util.mongo_model.model import MongoDBModel
from sanic.exceptions import SanicException
import datetime as dt
from bson import ObjectId


class Follower(MongoDBModel):
    coll_name = "follower"

    async def find_following_count_by_user_id(self, user_id):
        """

        :param user_id:
        :return: 关注数量
        """
        following_list = await self.find({"myself": ObjectId(user_id)})
        return following_list.count()

    async def find_followers_count_by_user_id(self, user_id):
        """

        :param user_id:
        :return: 粉丝数量
        """
        pass

    async def update_or_created_follow_relationship(self, id_1, id_2):
        """
        id1 following id2
        :param id_1:
        :param id_2:
        :return:
        """
        try:
            following_list = await self.find({"myself": ObjectId(id_1), "following": ObjectId(id_2)})
            count = len(following_list)
            if count == 1:
                return True
            else:
                await self.create({"myself": ObjectId(id_1), "following": ObjectId(id_2)})
            return True
        except Exception as e:
            # log
            raise AssertionError("关注失败")
        return True


class UserModel(MongoDBModel):
    coll_name = "user"
    unique_fields = ["registered_phone"]

    @staticmethod
    def trans_obj_id_str(docs):

        if isinstance(docs, list):
            for doc in docs:
                doc_id = str(doc.pop("_id"))
                doc['id'] = doc_id
            return docs
        elif isinstance(docs, dict):
            doc_id = str(docs.pop('_id'))
            docs['id'] = doc_id
            return docs

    @staticmethod
    def get_id(docs):
        return str(docs["_id"])

    async def find_by_registered_phone(self, registered_phone):
        doc = await self.find_one(registered_phone=registered_phone)
        return doc if doc else False

    async def create(self, obj):
        # user created need check register_phone unique
        check_res = await self.check_unique(obj)
        if check_res is not False:
            raise SanicException(check_res)
        result = await self.collection.insert_one(obj)
        return result

    async def check_unique(self, obj):
        error_list = []
        for fields in self.unique_fields:
            res = await self.collection.find({fields: obj[fields]}).to_list(length=100)
            if res:
                # if fields == "registered_phone":
                #     message = "s"
                # else:
                #     message = "not a unique"
                message = "已被注册"
                # error_list.append("{} {} is not a unique".format(fields, obj[fields]))
                error_list.append({fields: "{} {}".format(obj[fields], message)})
        if error_list:
            return error_list
        return False

    def update_by_logging(self, user_id):
        doc = self.update_last_logging_time(user_id)

        return doc

    def update_last_logging_time(self, user_id, last_login_time=None):
        if not last_login_time:
            last_login_time = dt.datetime.now()
        obj = {"last_logging_time": last_login_time}
        self.update_by_id(user_id, obj)
        doc = self.find_by_id(user_id)
        if doc is None:
            return None
        return doc
