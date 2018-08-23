#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: following_view.py
@time: 8/23/18 12:18 AM
"""

from sanic import Blueprint
from sanic.response import text

from obj.models.user_model import UserModel, Follower

from sanic import Sanic
from sanic.views import HTTPMethodView
from sanic.response import text, json
from sanic.exceptions import ServerError
from sanic_jwt.decorators import protected
from obj.util.setting import app
from obj.user.services.CheckServices import CheckRealUserServer
from bson import ObjectId

user_bp = Blueprint("user", url_prefix="/api/v1")

check_real_user_server = CheckRealUserServer()


class SimpleView(HTTPMethodView):
    def __init__(self):
        self.collection = app.mongo["account_center"].user
        self.user_model = UserModel(self.collection)

    async def get(self, request):
        print(dir(request))
        print(request.args)
        return text('I am get method async')

    async def post(self, request):
        return text('I am post method')

    async def put(self, request):
        return text('I am put method')

    async def patch(self, request):
        return text('I am patch method')

    async def delete(self, request):
        return text('I am delete method')


class SimpleView2(HTTPMethodView):
    decorators = [protected()]

    def get(self, request):
        print(dir(request))
        print(request.args)
        return json("this is protected")

    def post(self, request):
        return text('I am post method')

    def put(self, request):
        return text('I am put method')

    def patch(self, request):
        return text('I am patch method')

    def delete(self, request):
        return text('I am delete method')


class Follow(HTTPMethodView):
    def __init__(self):
        self.collection = app.mongo["account_center"].user
        self.user_model = UserModel(self.collection)
        self.follower_model = Follower(app.mongo["account_center"].follower)

    # def get(self, request):
    #     # get logging user follow
    #     print(dir(request))
    #     print(request.args)
    #     return json("this is protected")

    async def post(self, request):
        """
        add logging user following follow_user_id
        data = {"following_user_id": ""}
        :param request:
        :return:
        """
        # param check
        print("coooooooooooooooooooooo")
        print(request.cookies)
        login_user_id = request.cookies.get("user_id")
        following_user_id = request.json.get("following_user_id", None)
        assert following_user_id, "参数不能为空"
        # 1 check user id is real user
        doc = await check_real_user_server.is_user(following_user_id, self.user_model)
        # 2 update or created follow relationship in mongo
        # count = self.follower_model.update_or_created_follow_relationship()
        await self.follower_model.update_or_created_follow_relationship(login_user_id, following_user_id)

        # 3 update or created redis

        return text('I am post method')

    # def put(self, request):
    #     return text('I am put method')
    #
    # def patch(self, request):
    #     return text('I am patch method')

    def delete(self, request):
        return text('I am delete method')


user_bp.add_route(Follow.as_view(), "/user/follow")
