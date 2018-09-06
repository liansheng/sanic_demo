#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: user_marshal.py
@time: 8/12/18 10:39 PM
"""

import random
import datetime as dt
from sqlalchemy.ext.declarative import declarative_base

from user.check_common_mothed import gen_password
from util.tools import random_str, exeTime, head_portrait_change_change_change
from models.user_model import UserModel
from util.config import default_head_portrait, do_main

Base = declarative_base()


class UserReadModel:
    fields = ["user_id", "registered_phone", "name", "registration_sourece", "self_introduction",
              "qq", "wechat", "head_portrait", "following_count", "followers_count", "firend_count",
              "created_time", "is_add_bus_card", "is_add_id_card", "last_logging_time", "article_count"]

    def __init__(self, data, status):
        self.data = data
        self.status = status

    async def to_dict(self):
        res = {}
        for field in self.fields:
            if field in self.data.keys():
                res[field] = self.data[field]
            else:
                res[field] = None
        res = await self.update(res)
        return res

    async def update(self, res):
        res = self.update_status(res)
        res = self.update_user_id(res)
        res = self.update_created_time(res)
        res = self.update_last_logging_time(res)
        res = await head_portrait_change_change_change(res)
        return res

    def update_last_logging_time(self, res):
        res["last_logging_time"] = str(self.data["last_logging_time"])
        return res

    def update_created_time(self, res):
        res["created_time"] = str(self.data["created_time"])
        return res

    def update_status(self, res):
        res["status"] = self.status
        return res

    def update_user_id(self, res):
        res["user_id"] = str(self.data["_id"])
        return res


class UserRegisteredOnlyRead:
    fields = ["name", "_id", "head_portrait", "registered_phone"]

    def __init__(self, data):
        self.data = data

    def to_dict(self):
        print("self data is ", self.data)
        res = {}
        for field in self.fields:
            res[field] = self.data.get(field, None)
        res = self.update(res)
        return res

    def update(self, res):
        res = self.update_id(res)
        res = self.update_head_portrait(res)
        return res

    def update_id(self, res):
        res["user_id"] = str(res.pop("_id", None))
        return res

    @staticmethod
    def update_head_portrait(res):
        head_portrait = res.pop("head_portrait", None)
        if head_portrait:
            res["head_portrait"] = do_main + head_portrait
        else:
            res["head_portrait"] = do_main + default_head_portrait
        return res


class UserResister:
    REGISTRATION_SOURCE = ["wechat", "weibo", "qq", "phone"]
    GENDER = ["男", "女", "未填写"]
    fields = ["name", "registered_phone", "password", "created_time", "registration_source",
              "self_introduction", "qq", "wechat", "gender", "head_portrait", "is_add_id_card",
              "is_add_bus_card", "last_logging_time", "bus_card_info", "id_card_info",
              "following_count", "followers_count", "friend_count", "article_count"]

    def __init__(self, registered_phone, password, user_model, registration_source="phone"):
        self.user_model = user_model
        self.name = self.gen_random_name()

        self.registered_phone = registered_phone
        self.password = gen_password(password)
        self.created_time = dt.datetime.now()
        self.registration_source = registration_source
        self.self_introduction = None
        self.qq = None
        self.wechat = None
        self.gender = self.default_gender()
        self.head_portrait = self.default_head_portrait()

        self.is_add_id_card = False
        self.bus_card_info = {}
        self.is_add_bus_card = False
        self.id_card_info = {}
        self.last_logging_time = dt.datetime.now()
        self.bus_card_info = None
        self.id_card_info = None

        self.following_count = 0  # 关注数量
        self.followers_count = 0  # 粉丝数量
        self.friend_count = 0  # 好友数量
        self.article_count = 0  #

    @staticmethod
    def default_gender():
        return "未填写"

    @staticmethod
    def default_head_portrait():
        return default_head_portrait

    def gen_random_name(self):
        return self.random_name()

    @exeTime
    def random_name(self):
        for tmp in range(100):
            name = "fawo{}".format(random_str(8))
            if self.check_name(name):
                break
        return name

    def check_name(self, name):
        docs = self.user_model.find(name=name)
        if docs is not False:
            return True
        else:
            return False

    def __repr__(self):
        return '<User(name={self.name!r})>'.format(self=self)

    def to_dict(self):
        # d = {c.name: getattr(self, c.name, None)
        #      for c in self.__table__.columns}
        # return d
        res = {}
        for field in self.fields:
            res[field] = getattr(self, field, None)
        return res
        # return {
        #     "registered_phone": self.registered_phone,
        #     "password": self.password,
        #     "created_time": self.created_time,
        #     "name": self.name,
        #     "is_add_id_card": self.is_add_id_card,
        #     "is_add_bus_card": self.is_add_bus_card,
        #     "last_logging_time": self.last_logging_time,
        # }


class UserLoginAfter:
    fields = ["registered_phone", "_id"]

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def to_dict(self):
        res = {}
        for field in self.fields:
            v = self.kwargs.get(field, None)
            if v:
                v = str(v)
            res.update({field: v})
        return self.trans_id(res)

    def trans_id(self, res):
        if "_id" in res:
            res["user_id"] = res.pop("_id")
        return res


if __name__ == "__main__":
    us = UserResister("13979873546", "123123")
    print(us.to_dict())
