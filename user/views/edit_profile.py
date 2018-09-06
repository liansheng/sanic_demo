#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: edit_profile.py
@time: 8/30/18 2:47 AM
"""

from sanic.views import HTTPMethodView
from sanic_jwt.decorators import protected
from sanic import response
from sanic.exceptions import InvalidUsage

from models.friends_model import FriendModel
from models.user_model import UserModel, Follower
from user.user_marshal import UserReadModel
from util.setting import app
from util.tools import get_user_id_by_request
from util.responsePack import response_package
from user.services.update_user_info_to_friend_and_follow import UpdateServer

update_server = UpdateServer()


class EditView(HTTPMethodView):
    decorators = [protected()]
    fields = ["self_introduction", "name"]
    unique = ["name"]
    update_to_friend_follow = ["name"]

    def __init__(self):
        self.collection = app.mongo["account_center"].user
        self.user_model = UserModel(self.collection)
        self.follower_model = Follower(app.mongo["account_center"].follower)
        self.friends_model = FriendModel(app.mongo["account_center"].friends)

    async def patch(self, request):
        try:
            user_id = await get_user_id_by_request(request)
            data = request.json
            new_data = {}
            for k, v in data.items():
                if k not in self.fields:
                    continue
                new_data[k] = v
            for k, v in new_data.items():
                if k in self.unique:
                    res = await self.user_model.check_unique_simple_field(k, v)
                    if res is False:
                        raise InvalidUsage("{} 已被使用".format(v))
            # name need update to follow and friend collection
            doc = await self.user_model.update_by_id(user_id, new_data)
            for k, v in new_data.items():
                if k in self.update_to_friend_follow:
                    await update_server.update_name(k, v, user_id, self.follower_model, self.friends_model)
            data = await UserReadModel(data=doc, status="").to_dict()
            return response.json(response_package("200", data))
        except TimeoutError as e:
            return response.json(response_package("999", {"e": str(e)}))
