#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: CheckServices.py
@time: 8/23/18 1:38 AM
"""
from bson import ObjectId

from obj.models.user_model import UserModel
from obj.util.setting import app


class CheckServer:

    def is_real_id(self, user_id):
        try:
            user_id_obj = ObjectId(user_id)
        except Exception:
            return False
        return True

    async def is_user(self, user_id, user_model):
        assert self.is_real_id(user_id), "要关注的用户不存在"
        doc = await user_model.find_by_id(user_id)
        assert doc, "要关注的用户不存在"
        return doc


if __name__ == '__main__':
    user_id = "5b7e29dd5f627d0218528819"
