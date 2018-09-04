#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: update_user_info_to_friend_and_follow.py
@time: 9/3/18 6:38 PM
"""


class UpdateServer:
    async def update_name(self, k, v, user_id, follower_model, friends_model):
        if k == "name":
            print(k, v, user_id)
            await follower_model.update_name(user_id, v)
            await friends_model.update_name(user_id, v)
        pass
