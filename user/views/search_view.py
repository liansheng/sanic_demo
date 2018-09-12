#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: search_view.py
@time: 8/27/18 12:26 AM
"""
from sanic.views import HTTPMethodView
from sanic import response
from sanic_jwt import protected

from models.friends_model import FriendModel
from models.user_model import UserModel, Follower
from user.services.parameter_check import ParameterCheck
from user.user_model import FansSchema, FollowingSchema, FriendSchema, UserSchema
from util.setting import app
from util.tools import get_user_id_by_request, head_portrait_change_change_change
from user.services.SearchService import SearchServices
from util.responsePack import response_package

parameter_check = ParameterCheck()
search_service = SearchServices()


class SearchUser(HTTPMethodView):
    # decorators = [protected()]
    def __init__(self):
        self.collection = app.mongo["account_center"].user
        self.user_model = UserModel(self.collection)
        self.follower_model = Follower(app.mongo["account_center"].follower)
        self.friends_model = FriendModel(app.mongo["account_center"].friends)
        self.MAPPING = {
            "followers": self.follower_model,
            "following": self.follower_model,
            "friend": self.friends_model,
            "user": self.user_model,
        }
        self.SchemaMapping = {
            "followers": FansSchema,
            "following": FollowingSchema,
            "friend": FriendSchema,
            "user": UserSchema,
        }

    async def get(self, request):
        """
        get followers following friend user list
        :param request:
        :return: search_type =
        """
        # print(dir(request))
        # print(dir(request.get))
        # user_id = await get_user_id_by_request(request)
        data = parameter_check.search_user_check(request.raw_args)

        model = self.MAPPING[data["type"]]
        schema = self.SchemaMapping[data["type"]]
        data_list = await search_service.search_user(model, data)
        # if data["type"] == "user":
        res_data = schema(many=True).dump(data_list).data
        for tmp in res_data:
            print(data["user_id"], str(tmp["user_id"]))
            tmp["is_i_follow_him"] = await self.follower_model.check_user1_is_following_user2(data["user_id"],
                                                                                              str(tmp["user_id"]))
            tmp["is_friend"] = await self.follower_model.check_is_mutual_follow(data["user_id"], str(tmp["user_id"]))
            tmp = await head_portrait_change_change_change(tmp, "user_head_portrait")

        print("data_list is ", data_list)
        print("res_data is ", res_data)
        # data_list, need serializers
        return response.json(response_package("200", {"data_info": res_data}))
        pass
