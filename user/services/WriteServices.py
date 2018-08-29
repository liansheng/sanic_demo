#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: WriteServices.py
@time: 8/28/18 1:55 AM
"""
from obj.user.user_model import (
    WriteFollowInfoSchema,
    WriteSelfFollowInfoSchema,
    WriteFollowingFollowInfoSchema)


class WriteModelServer:
    async def write_follower_relationship(self, app, follower_model, user_model, login_user_id, following_user_id):
        # 1  I(login_user_id) well following other p(following_user_id)
        # Can't write Chinese orzzzzzzzzzzzzzzzzzzz
        doc = await user_model.find_by_id(login_user_id)
        new_doc = await user_model.trans_obj_id(doc)
        self_schema = WriteSelfFollowInfoSchema()
        login_data = self_schema.load(new_doc)
        assert not login_data.errors, ("关注数据异常", login_data.errors)
        print(login_data.errors)
        print("result data ", login_data.data)
        print("login_user_id info ", doc)
        # 2
        follow_doc = await user_model.find_by_id(following_user_id)
        new_follow_doc = await user_model.trans_obj_id(follow_doc)
        follower_schema = WriteFollowingFollowInfoSchema()
        follow_data = follower_schema.load(new_follow_doc)
        print("new_follow_doc is ", new_follow_doc)
        print("follow_data is ", follow_data.data)
        print(follow_data.errors)
        assert not follow_data.errors, ("关注数据异常", follow_data.errors)


        # gen data, write data to collection

        pass

    pass
