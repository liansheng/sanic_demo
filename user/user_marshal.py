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

from obj.user.check_common_mothed import gen_password
from obj.util.tools import random_str, exeTime
from obj.models.user_model import UserModel
from obj.util.config import default_head_portrait

Base = declarative_base()


class UserReadModel:
    fields = ["user_id", "registered_phone", "name", "registration_sourece", "self_introduction",
              "qq", "wechat", "head_portrait", "following_count", "followers_count", "firend_count",
              "created_time", "is_add_bus_card", "is_add_id_card", "last_logging_time"]

    def __init__(self, data, status):
        self.data = data
        self.status = status

    def to_dict(self):
        res = {}
        for field in self.fields:
            if field in self.data.keys():
                res[field] = self.data[field]
            else:
                res[field] = None
        res = self.update(res)
        return res

    def update(self, res):
        res = self.update_status(res)
        res = self.update_user_id(res)
        res = self.update_created_time(res)
        res = self.update_last_logging_time(res)
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


class UserResister:
    REGISTRATION_SOURCE = ["wechat", "weibo", "qq", "phone"]
    GENDER = ["男", "女", "未填写"]

    def __init__(self, registered_phone, password, user_model, registration_source="phone"):
        self.registered_phone = registered_phone
        self.password = password
        self.created_time = dt.datetime.now()
        self.registration_source = registration_source
        self.self_introduction = None
        self.qq = None
        self.wechat = None
        self.gender = "未填写"
        self.head_portrait = default_head_portrait

        self.name = self.gen_random_name()

        self.is_add_id_card = False
        self.is_add_bus_card = False
        self.last_logging_time = dt.datetime.now()
        self.bus_card_info = None
        self.id_card_info = None

        self.following_count = 0  # 关注数量
        self.followers_count = 0  # 粉丝数量
        self.friend_count = 0  # 好友数量

        self.user_model = user_model

    def gen_random_name(self):
        return self.random_name()

    @exeTime
    def random_name(self):
        for tmp in range(1000):
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
        return {
            "registered_phone": self.registered_phone,
            "password": gen_password(self.password),
            "created_time": self.created_time,
            "name": self.name,
            "is_add_id_card": self.is_add_id_card,
            "is_add_bus_card": self.is_add_bus_card,
            "last_logging_time": self.last_logging_time,
        }


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
            res["id"] = res.pop("_id")
        return res


if __name__ == "__main__":
    us = UserResister("13979873546", "123123")
    print(us.to_dict())