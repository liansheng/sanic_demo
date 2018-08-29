#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: login_and_registered_view.py
@time: 8/16/18 6:25 PM
"""
from sanic.response import (
    json,
    text
)
from sanic_jwt import BaseEndpoint, exceptions

from models.user_model import UserModel
from user.user_marshal import UserResister, UserRegisteredOnlyRead
from user.user_model import UserResisterSchema, RegisterPhoneSchema
from util.marshal_with.data_check import typeassert, typeassert_async
from util.responsePack import response_package
from util.setting import app


class MyCustomUserAuthHelper:
    def __init__(self):
        self.collection = app.mongo["account_center"].user
        self.user_model = UserModel(self.collection)

    @typeassert(UserResisterSchema)
    async def register_new_user(self, registered_phone, password):
        user_data = UserResister(registered_phone, password,
                                 user_model=self.user_model).to_dict()
        doc = await self.user_model.create(user_data)
        print(user_data)
        return UserRegisteredOnlyRead(user_data).to_dict()
        # res_data = {}
        # res_data["registered_phone"] = user_data["registered_phone"]
        # res_data["id"] = user_model.get_id(user_data)
        # res_data["id"] = str(doc.inserted_id)
        # print("doc ccccccccc ", doc)
        # return res_data

    @typeassert_async(RegisterPhoneSchema)
    async def check_registered_phone(self, registered_phone):
        res = await self.user_model.find_by_registered_phone(registered_phone=registered_phone)
        if res is not False:
            raise exceptions.AuthenticationFailed(
                "手机号已被注册"
            )
        else:
            return json(response_package("200", "手机号未被注册"))


class Register(BaseEndpoint):

    # async def get(self, request, *args, **kwargs):
    #     return json({"mo": "fuck"})
    #
    # async def options(self, request, *args, **kwargs):
    #     return text("", status=204)

    @typeassert(UserResisterSchema)
    async def post(self, request, *args, **kwargs):
        registered_phone = request.json.get('registered_phone', None)
        password = request.json.get('password', None)
        print("request  ---------------------")
        # # print(dir(request))
        print(request.cookies)

        helper = MyCustomUserAuthHelper()
        user = await helper.register_new_user(registered_phone=registered_phone, password=password)

        access_token, output = await self.responses.get_access_token_output(
            request,
            user,
            self.config,
            self.instance)

        refresh_token = await self.instance.auth.generate_refresh_token(request, user)
        output.update({
            self.config.refresh_token_name(): refresh_token
        })

        user_id = user.get("id", None)
        key = "refresh_token_{user_id}".format(user_id=user_id)
        res = await app.redis.set(key, refresh_token)
        print("regi   res ", res)
        output.clear()

        output.update(response_package("200", {"access_token": access_token,
                                               "refresh_token": refresh_token,
                                               "user_info": user}), )
        response = self.responses.get_token_reponse(
            request,
            access_token,
            output,
            refresh_token=refresh_token,
            config=self.config)
        # print(response.headers)
        # print(response)
        return response
        # return json()
