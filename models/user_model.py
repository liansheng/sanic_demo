#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: user_model.py
@time: 8/16/18 2:23 AM
"""
from __future__ import print_function
from __future__ import unicode_literals

from util.mongo_model.model import MongoDBModel
from sanic.exceptions import SanicException
import datetime as dt
from bson import ObjectId
import copy


class Follower(MongoDBModel):
    coll_name = "follower"

    async def find_following_count_by_user_id(self, user_id):
        """

        :param user_id:
        :return: 关注数量
        """
        following_list = await self.find_list({"myself_user_id": user_id})
        return following_list.count()

    async def check_user1_is_following_user2(self, user1, user2):
        """
        :param user1:
        :param user2:
        :return:
        """
        count = await self.collection.count_documents({"myself_user_id": user1, "following_user_id": user2})
        if count > 0:
            return True
        else:
            return False

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

    # async def update_or_created_follow_relationship(self, id_1, id_2):
    #     """
    #     id1 following id2
    #     :param id_1:
    #     :param id_2:
    #     :return:
    #     """
    #     try:
    #         # print("myself id ", id_1, "following id ", id_2)
    #         # following_list = await self.find({"myself": ObjectId(id_1), "following": ObjectId(id_2)})
    #         following_list = await self.find(myself_user_id=id_1, following_user_id=id_2)
    #         # print("following_list os ", following_list)
    #         count = len(following_list)
    #         if count == 1:
    #             return "existed"
    #         else:
    #             await self.create({"myself_user_id": id_1, "following_user_id": id_2})
    #         return True
    #     except Exception as e:
    #         raise AssertionError("关注失败")

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
            count = await self.collection.count_documents(filter={"myself_user_id": data1["myself_user_id"],
                                                                  "following_user_id": data2["following_user_id"]})
            if count == 1:
                return "existed"
            else:
                new_data = copy.deepcopy(data1)
                new_data.update(data2)
                if "created_time" not in new_data:
                    new_data["created_time"] = dt.datetime.now()
                await self.create(new_data)
            return True
        except Exception as e:
            raise AssertionError("关注失败", str(e))

    async def get_followers_count(self, user_id):
        """
        get this user_id followers(Fans)
        :param user_id:
        :return:
        """
        fans_count = await self.collection.count_documents({"following_user_id": user_id})
        return fans_count

    async def get_following_count(self, user_id):
        """
        get how many people does this man following
        :param user_id:
        :return:
        """
        return await self.collection.count_documents({"myself_user_id": user_id})

    async def check_is_mutual_follow(self, id_1, id_2):
        """
        :param id_1:
        :param id_2:
        :return:  True | False
        """
        first = await self.collection.count_documents({"myself_user_id": id_1, "following_user_id": id_2})
        # res = await self.find_list(myself_user_id=id_1, following_user_id=id_2).count()
        if first == 0:
            return False
        second = await self.collection.count_documents({"following_user_id": id_1, "myself_user_id": id_2})
        # second = await self.find_list(myself_user_id=id_2, following_user_id=id_1).count()
        if second == 0:
            return False
        return True

    async def find_following_by_name_and_user_id(self, user_id, offset, key_words="", page_size=20):
        """
        search user_id's following
        :param user_id:
        :param offset:
        :param key_words:
        :param page_size:
        :return:
        """
        docs = await self.collection.find(
            {"following_name": {'$regex': key_words}, 'myself_user_id': user_id}
        ).skip(offset).to_list(page_size)
        return docs

    async def find_followers_by_name_and_user_id(self, user_id, offset, key_words="", page_size=20):
        """
        search user_id's fans
        :param user_id:
        :param offset:
        :param key_words:
        :param page_size:
        :return:
        """
        docs = await self.collection.find(
            {"myself_name": {'$regex': key_words, '$options': 'i'}, 'following_user_id': user_id}
        ).skip(offset).to_list(page_size)
        return docs

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

    async def update_head(self, user_id, sum_path):
        """
        :param user_id:
        :param sum_path:
        :return:
        """
        await self.update_myself_head(user_id, sum_path)
        res = await self.update_following_head(user_id, sum_path)
        return res

    async def update_following_head(self, user_id, path):
        """
        :param user_id:
        :param path:
        :return:
        """
        criteria = {"following_user_id": user_id}
        obj_new = {"$set": {"following_head_portrait": path}}

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

    async def update_name(self, user_id, new_name):
        await self.update_following_name(user_id, new_name)
        res = await self.update_myself_name(user_id, new_name)
        return res

    async def update_following_name(self, user_id, new_name):
        criteria = {"following_user_id": user_id}
        obj_new = {"$set": {"following_name": new_name}}
        return await self.update_many(criteria, obj_new)

    async def update_myself_name(self, user_id, new_name):
        criteria = {"myself_user_id": user_id}
        obj_new = {"$set": {"myself_name": new_name}}
        return await self.update_many(criteria, obj_new)


class UserModel(MongoDBModel):
    coll_name = "user"
    unique_fields = ["registered_phone", "name"]

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
        check_res = await self.new_check_unique(obj)
        if check_res is not False:
            raise SanicException(check_res)
        result = await self.collection.insert_one(obj)
        return result

    async def new_check_unique(self, obj):
        return await self.check_phone(obj)

    async def check_phone(self, obj):
        registered_phone = obj.get("registered_phone", None)
        if registered_phone:
            res = await self.collection.find({"registered_phone": registered_phone}).to_list(length=100)
            if res:
                return "{} 已被注册".format(registered_phone)
        return False

    # async def check_unique(self, obj, message="已被注册"):
    #     error_list = []
    #     for fields in self.unique_fields:
    #         t = obj.get(fields, None)
    #         if t is None:
    #             continue
    #         res = await self.collection.find({fields: obj[fields]}).to_list(length=100)
    #         if res:
    #             # if fields == "registered_phone":
    #             #     message = "s"
    #             # else:
    #             #     message = "not a unique"
    #             # error_list.append("{} {} is not a unique".format(fields, obj[fields]))
    #             error_list.append({fields: "{} {}".format(obj[fields], message)})
    #     if error_list:
    #         return error_list
    #     return False

    async def check_unique_simple_field(self, key, value):
        res = await self.collection.find({key: value}).to_list(length=100)
        if res:
            return False
        return True

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

    async def update_article_count(self, user_id):
        self.inc_field_by_user_id(user_id, "article_count", 1)

    async def sub_article_count(self, user_id):
        """
        :param user_id:
        :return:
        """
        is_zero = await self.field_is_zero(user_id, "article_count")
        if is_zero:
            return True
        self.inc_field_by_user_id(user_id, "article_count", -1)

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

    async def update_password(self, user_id, password):
        """
        :param user_id:
        :param password:
        :return:
        """
        obj = {"password": password}
        return self.update_by_id(user_id, obj)

    async def update_head(self, user_id, sum_path):
        """
        :param user_id:
        :param sum_path:
        :return:
        """
        obj = {"head_portrait": sum_path}
        return self.update_by_id(user_id, obj)

    async def update_following_count(self, user_id, count):
        obj = {"following_count": count}
        return self.update_by_id(user_id, obj)

    async def update_followers_count(self, user_id, count):
        obj = {"followers_count": count}
        return self.update_by_id(user_id, obj)

    async def update_friend_count(self, user_id, count):
        obj = {"friend_count": count}
        return self.update_by_id(user_id, obj)

    async def find_user_by_name(self, offset, key_words, page_size):
        """
        :param offset:
        :param key_words:
        :param page_size:
        :return:
        """
        docs = await self.collection.find(
            {"name": {'$regex': key_words}}
        ).skip(offset).to_list(page_size)
        return docs

    async def get_head_portrait(self, user_id):
        doc = await self.find_by_id(user_id)
        if isinstance(doc, dict):
            return doc.get("head_portrait", None)
        else:
            return None
