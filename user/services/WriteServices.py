#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: WriteServices.py
@time: 8/28/18 1:55 AM
"""
from obj.user.user_model import WriteFollowInfoSchema


class WriteModelServer:
    async def write_follower_relationship(self, follower_model, user_model, login_user_id, following_user_id):
        doc = await user_model.find_by_id(login_user_id)
        new_doc = await user_model.trans_obj_id(doc)
        WriteFollowInfoSchema
        print("login_user_id info ", doc)
        pass
    pass
