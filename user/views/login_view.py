#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: login.py
@time: 8/16/18 6:38 PM
"""
from sanic_jwt import initialize, Authentication, exceptions, utils
from sanic.response import json
from models.user_model import UserModel
from user.user_marshal import UserLoginAfter, UserReadModel
from user.user_model import UserResisterSchema
from util.marshal_with.data_check import typeassert, typeassert_async
from util.responsePack import response_package
from util.setting import app
from user.check_common_mothed import gen_password


class MyAuthentication(Authentication):
    expiration_delta = 60 * 100
    url_prefix = "/api_user/v1/auth"

    # def __init__(self, *args, **kwargs):
    #     super(MyAuthentication, self).__init__(*args, **kwargs)
    @typeassert_async(UserResisterSchema)
    async def authenticate(self, request, *args, **kwargs):
        registered_phone = request.json.get("registered_phone", None)
        password = request.json.get("password", None)

        # "Missing registered_phone or password."
        collection = app.mongo["account_center"].user
        user_model = UserModel(collection)

        if not registered_phone:
            raise exceptions.MissingAuthorizationQueryArg("手机号码为空")
        if not password:
            raise exceptions.MissingAuthorizationQueryArg("密码为空")
        res = await user_model.find_one(registered_phone=registered_phone, password=gen_password(password))

        if res:
            new_res = await user_model.update_by_logging(res["_id"])
            return UserReadModel(data=new_res, status="登录").to_dict()
        else:
            raise exceptions.MissingAuthorizationQueryArg(
                "手机号码与密码不一致"
            )

    async def generate_refresh_token(self, request, user):
        """
        Generate a refresh token for a given user.
        """
        # search refresh token
        # if haved refresh token, only return it, not generate

        refresh_token = await utils.call(self.config.generate_refresh_token())
        user_id = await self._get_user_id(user)
        key = "refresh_token_{user_id}".format(user_id=user_id)
        # print("user  ,... ", user)
        # print("key ", key)
        r = await self.app.redis.get(key)
        if r:
            refresh_token = r
        # print("r -------------", r)
        await utils.call(
            self.store_refresh_token,
            user_id=user_id,
            refresh_token=refresh_token,
            request=request,
        )
        return refresh_token

    async def store_refresh_token(
            self, user_id, refresh_token, *args, **kwargs
    ):
        """
        befor store refresh token, search refresh token in redis
        :param user_id:
        :param refresh_token:
        :param args:
        :param kwargs:
        :return:
        """
        key = "refresh_token_{user_id}".format(user_id=user_id)
        # self.app.my_cache[key] = refresh_token
        # await self.app.redis.get(key)
        await self.app.redis.set(key, refresh_token)

    async def retrieve_refresh_token(self, user_id, *args, **kwargs):
        print("retrieve_refresh_token....................................")
        key = "refresh_token_{user_id}".format(user_id=user_id)
        # token = self.app.my_cache.get(key, None)
        token = await self.app.redis.get(key)
        print("key is ", key)
        print("token is ", token)
        return token

    async def retrieve_user(self, request, payload, *args, **kwargs):
        collection = app.mongo["account_center"].user
        user_model = UserModel(collection)
        print("retrieve_user payload is ", payload)
        if payload:
            user_id = payload.get("user_id", None)
            if user_id is None:
                raise exceptions.AuthenticationFailed()
            docs = await user_model.find_by_id(user_id)
            print("docs : ", docs)
            # return response_package("200", UserLoginAfter(**docs).to_dict())
            return UserLoginAfter(**docs).to_dict()
            # return {"user_id": user_id}
        else:
            return response_package("401", {"user_id": None})

    async def logout(self, user_id, *args, **kwargs):
        key = "refresh_token_{user_id}".format(user_id=user_id)
        await self.app.redis.delete(key)
        return True
