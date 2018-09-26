#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: login_and_registered_view.py
@time: 8/16/18 6:25 PM
"""
import os
import base64

from io import StringIO, BytesIO

from sanic.response import (
    json,
    text
)
from sanic_jwt import BaseEndpoint, exceptions

from models.user_model import UserModel
from user.user_marshal import UserResister, UserRegisteredOnlyRead
from user.user_model import UserResisterSchema, RegisterPhoneSchema
from util.config import STATIC_IMG_DIR, CAPTCHA_TIMEOUT, IMG_RELATIVE_PATH, EXPIRATION_DELTA
from util.kafka.productServer import SendServer
from util.marshal_with.data_check import typeassert, typeassert_async
from util.responsePack import response_package
from util.server_init.init_reids import InitRedis
from util.setting import app
from user.services.captcha import CreateCaptcha
from util.tools import random_str, get_login_device
import datetime as dt

send_kafka_server = SendServer()


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

    async def check_captcha(self, captcha_key, captcha_num):
        key = await app.redis.get(captcha_key)
        assert key, "验证码已过期"
        assert key == captcha_num, "验证码不正确"

    @typeassert(UserResisterSchema)
    async def post(self, request, *args, **kwargs):
        # check captcha
        captcha_key = request.json.get("captcha_mark", None)
        captcha_num = request.json.get("captcha", None)
        assert captcha_key, "验证码未填写"
        await self.check_captcha(captcha_key, captcha_num)

        registered_phone = request.json.get('registered_phone', None)
        password = request.json.get('password', None)
        print("request  ---------------------")
        # # print(dir(request))
        print(request.cookies)

        helper = MyCustomUserAuthHelper()
        user = await helper.register_new_user(registered_phone=registered_phone, password=password)
        await send_kafka_server.send_to(app=app, topic="user", message_type="register", body=user)
        init_redis = InitRedis(app.redis, UserModel(app.mongo["account_center"].user))
        await init_redis.init_registered_info_to_redis(user)

        access_token, output = await self.responses.get_access_token_output(
            request,
            user,
            self.config,
            self.instance)

        refresh_token = await self.instance.auth.generate_refresh_token(request, user)
        output.update({
            self.config.refresh_token_name(): refresh_token
        })

        user_id = user.get("user_id", None)
        key = "refresh_token_{user_id}".format(user_id=user_id)
        res = await app.redis.set(key, refresh_token)
        login_device = await get_login_device(request)
        await app.redis.set("{}_{}".format(login_device, user_id), access_token, expire=EXPIRATION_DELTA)
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


class Captcha(BaseEndpoint):

    async def get(self, request):
        # return captcha address, and set a  redis k-v, and set k to redis ,
        theme = request.raw_args.get("theme", "dark")
        uuid = random_str(32)

        x = CreateCaptcha(theme)
        image = x.gene_code()
        buffer = BytesIO()
        image.save(buffer, format='png')
        img_str = base64.b64encode(buffer.getvalue())

        await app.redis.set(str(uuid), str(x.text), expire=CAPTCHA_TIMEOUT)

        response = json(response_package("200", {"image_b64data": img_str, "captcha": uuid}))
        # response.cookies["captcha"] = str(uuid)
        return response
