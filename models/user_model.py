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
        following_list = await self.find_list({"myself_user_id": user_id})
        return following_list.count()

    async def find_followers_count_by_user_id(self, user_id):
        """

        :param user_id:
        :return: 粉丝数量
        """
        following_list = await self.find_list({"following_user_id": user_id})
        return following_list.count()

    async def delete_follow_relationship(self, id_1, id_2):
        """

        :param id_1:
        :param id_2:
        :return:
        """
        following_list = await self.find(myself_user_id=id_1, following_user_id=id_2)
        count = len(following_list)
        if count == 1:
            self.remove_by_id(following_list[0]["_id"])
            return True
        else:
            return "is_null"

    async def update_or_created_follow_relationship(self, id_1, id_2):
        """
        id1 following id2
        :param id_1:
        :param id_2:
        :return:
        """
        try:
            # print("myself id ", id_1, "following id ", id_2)
            # following_list = await self.find({"myself": ObjectId(id_1), "following": ObjectId(id_2)})
            following_list = await self.find(myself_user_id=id_1, following_user_id=id_2)
            # print("following_list os ", following_list)
            count = len(following_list)
            if count == 1:
                return "existed"
            else:
                await self.create({"myself_user_id": id_1, "following_user_id": id_2})
            return True
        except Exception as e:
            raise AssertionError("关注失败")

    async def update_or_created_follow_relationship_by_data(self, data1, data2):
        """
        id1 following id2
        :param data1: {'myself_head_portrait': '/static/img/default_head_portrait.jpg',
                'myself_name': 'fawoaKNNgOTx', 'myself_user_id': '5b7e29dd5f627d0218528819'}
        :param data2: {'following_hsead_portrait': '/static/img/default_head_portrait.png',
                'following_name': 'fawoM7zemXN7', 'following_user_id': '5b7cfbd45f627ddd88e2c929'}
        :return:
        """
        try:
            # print("myself id ", id_1, "following id ", id_2)
            # following_list = await self.find({"myself": ObjectId(id_1), "following": ObjectId(id_2)})
            count = await self.find_list(myself_user_id=data1["myself_user_id"],
                                         following_user_id=data2["following_user_id"]).count()
            # print("following_list os ", following_list)
            if count == 1:
                return "existed"
            else:
                data1.update(data2)
                await self.create(data1)
            return True
        except Exception as e:
            raise AssertionError("关注失败")

    async def check_is_mutual_follow(self, id_1, id_2):
        """
        :param id_1:
        :param id_2:
        :return:  True | False
        """
        res = await self.find_list(myself_user_id=id_1, following_user_id=id_2).count()
        if res == 0:
            return False
        second = await self.find_list(myself_user_id=id_2, following_user_id=id_1).count()
        if second == 0:
            return False
        return True

    async def add_follow(self, id_1, id_2):
        """
        1. add 1 following 2 in redis
        2. add 2 followers 1 in redis
        3. 1 following count + 1 in mongo
        4, 2 followers count + 1 in mongo
        :param id_1:
        :param id_2:
        :return:
        """
        pass


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

    async def add_follow_count(self, user_id_1, user_id_2):
        """
        add user_id_1 following count
        add user_id_2 followers count
        :param user_id_1:
        :param user_id_2:
        :return:
        """
        await self.add_following_count(user_id_1)
        await self.add_followers_count(user_id_2)

    async def add_following_count(self, user_id):
        """

        :param user_id:
        :return:
        """
        self.inc_field_by_user_id(user_id, "following_count", 1)

    async def add_followers_count(self, user_id_2):
        """
        :param user_id_2:
        :return:
        """
        self.inc_field_by_user_id(user_id_2, "followers_count", 1)

    async def sub_following_count(self, user_id):
        """

        :param user_id:
        :return:
        """
        is_zero = await self.field_is_zero(user_id, "following_count")
        if is_zero:
            return True
        self.inc_field_by_user_id(user_id, "following_count", -1)

    async def sub_followers_count(self, user_id_2):
        """
        delete followers need check count is not = 0
        if count is 0,then not need -1
        :param user_id_2:
        :return:
        """
        is_zero = await self.field_is_zero(user_id_2, "followers_count")
        if is_zero:
            return True
        self.inc_field_by_user_id(user_id_2, "followers_count", -1)

    async def field_is_zero(self, user_id, field):
        """
        :param user_id:
        :return:
        """
        doc = await self.find_by_id(user_id)
        res = doc.get(field, None)
        if res == 0:
            return True
        else:
            return False

    async def sub_follow_count(self, user_id_1, user_id_2):
        """
        :param user_id_1:
        :param user_id_2:
        :return:
        """
        await self.sub_following_count(user_id_1)
        await self.sub_followers_count(user_id_2)
