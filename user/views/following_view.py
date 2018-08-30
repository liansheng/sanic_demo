#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: following_view.py
@time: 8/23/18 12:18 AM
"""

from sanic import Blueprint
from sanic.response import text

from models.user_model import UserModel, Follower
from models.friends_model import FriendModel

from sanic import Sanic
from sanic.views import HTTPMethodView
from sanic.response import text, json
from sanic.exceptions import ServerError
from sanic_jwt.decorators import protected, inject_user

from user.views.edit_profile import EditView
from user.views.search_view import SearchUser
from util.setting import app
from user.services.CheckServices import CheckServer
from bson import ObjectId
from util.responsePack import response_package
from util.tools import get_user_id_by_request
from user.services.WriteServices import WriteModelServer
from user.views.change_password import ChangePassword

user_bp = Blueprint("user", url_prefix="/api_user/v1")

check_server = CheckServer()
write_model_server = WriteModelServer()


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

    # @inject_user()
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
    decorators = [protected()]

    def __init__(self):
        self.collection = app.mongo["account_center"].user
        self.user_model = UserModel(self.collection)
        self.follower_model = Follower(app.mongo["account_center"].follower)
        self.friends_model = FriendModel(app.mongo["account_center"].friends)

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
        # print(" user_id ", user.user_id)
        login_user_id = await get_user_id_by_request(request)
        assert login_user_id, "当前没有用户登录"
        following_user_id = request.json.get("following_user_id", None)
        assert following_user_id, "参数不能为空"

        # 1 check user id is real user
        await check_server.is_user(following_user_id, self.user_model)

        # 2 update or created follow relationship in mongo
        # count = self.follower_model.update_or_created_follow_relationship()
        # write follower collection server
        await write_model_server.write_follower_relationship(app, self.follower_model, self.user_model,
                                                             self.friends_model, login_user_id, following_user_id)
        # res = await self.follower_model.update_or_created_follow_relationship_by_data(login_user_id, following_user_id)
        # if res is not "existed":
        #     # if login id have not follow relationship. then inc following and followers count
        #     # 3 a->b check, a is <- b, then add friend relationship
        #     if await self.follower_model.check_is_mutual_follow(login_user_id, following_user_id):
        #         await self.friends_model.add(login_user_id, following_user_id)
        #         await app.redis.sadd("{}_{}".format(login_user_id, "friends"), following_user_id)
        #         await app.redis.sadd("{}_{}".format(following_user_id, "friends"), login_user_id)
        #
        #     # 4 update or created follow redis
        #     await self.user_model.add_follow_count(login_user_id, following_user_id)
        #     if isinstance(following_user_id, bytes):
        #         following_user_id = following_user_id.decode()
        #     await app.redis.sadd("{}_{}".format(login_user_id, "follower"), following_user_id)

        return json(response_package("200", {}))

    # def put(self, request):
    #     return text('I am put method')
    #
    # def patch(self, request):
    #     return text('I am patch method')

    # def delete(self, request):
    #     return text('I am delete method')


class UnFollow(HTTPMethodView):
    decorators = [protected()]

    def __init__(self):
        self.collection = app.mongo["account_center"].user
        self.user_model = UserModel(self.collection)
        self.follower_model = Follower(app.mongo["account_center"].follower)
        self.friends_model = FriendModel(app.mongo["account_center"].friends)

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
        login_user_id = request.cookies.get("user_id", None)
        assert login_user_id, "当前没有用户登录"
        following_user_id = request.json.get("un_following_user_id", None)
        assert following_user_id, "参数不能为空"

        # 1 check user id is real user
        await check_server.is_user(following_user_id, self.user_model)

        # 2 update or created follow relationship in mongo
        # count = self.follower_model.update_or_created_follow_relationship()
        await write_model_server.write_unfollower_relationship(app, self.follower_model, self.user_model,
                                                               self.friends_model, login_user_id, following_user_id)

        # res = await self.follower_model.update_or_created_follow_relationship(login_user_id, following_user_id)
        # await  self.follower_model.delete_follow_relationship(login_user_id, following_user_id)
        # if res is not "is_null":
        #     # if login id have not follow relationship. then inc following and followers count
        #     # 3 delete friend relationship
        #     await self.friends_model.remove(login_user_id, following_user_id)
        #     await app.redis.srem("{}_{}".format(login_user_id, "friends"), following_user_id)
        #     await app.redis.srem("{}_{}".format(following_user_id, "friends"), login_user_id)
        #
        #     # 4 update or created redis
        #     await self.user_model.sub_follow_count(login_user_id, following_user_id)
        #     await app.redis.srem("{}_{}".format(login_user_id, "follower"), count=1, value=following_user_id)

        return json(response_package("200", {}))


user_bp.add_route(Follow.as_view(), "/user/follow")
user_bp.add_route(UnFollow.as_view(), "/user/un_follow")
user_bp.add_route(SearchUser.as_view(), "/user/search")
user_bp.add_route(ChangePassword.as_view(), "/user/change_password/")
user_bp.add_route(EditView.as_view(), "/user/edit/")
