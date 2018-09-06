#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: personal_infomation.py
@time: 9/3/18 11:26 PM
"""
from sanic.views import HTTPMethodView
from sanic import response
from sanic_jwt.exceptions import MissingAuthorizationHeader

from models.friends_model import FriendModel
from models.user_model import UserModel, Follower
from user.services.CheckServices import CheckServer
from user.user_marshal import UserReadModel
from util.responsePack import response_package
from util.setting import app
from util.tools import get_user_id_by_request

check_server = CheckServer()


class PersonalInfomation(HTTPMethodView):
    """
    """
    def __init__(self):
        self.collection = app.mongo["account_center"].user
        self.user_model = UserModel(self.collection)
        self.follower_model = Follower(app.mongo["account_center"].follower)
        self.friends_model = FriendModel(app.mongo["account_center"].friends)

    async def get(self, request, user_id):
        try:
            login_user_id = await get_user_id_by_request(request)
        except MissingAuthorizationHeader as e:
            login_user_id = False
        doc = await check_server.is_user(user_id, self.user_model)
        data = await UserReadModel(data=doc, status="").to_dict()
        if login_user_id:
            is_friend = await self.follower_model.check_is_mutual_follow(login_user_id, user_id)
            is_i_following_him = await self.follower_model.check_user1_is_following_user2(login_user_id, user_id)
            data["is_friend"] = is_friend
            data["is_i_following_him"] = is_i_following_him
        else:
            data["is_friend"] = False
            data["is_i_following_him"] = False

        return response.json(response_package("200", data))
