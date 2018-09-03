#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: check_view.py
@time: 8/19/18 6:22 PM
"""
from sanic_jwt import initialize, Authentication, exceptions
# from sanic.response import json
from sanic_jwt import BaseEndpoint

# from user.user_model import RegisterPhoneSchema
from user.views.registered_view import MyCustomUserAuthHelper
# from util.marshal_with.data_check import typeassert, typeassert_async, typeassert_request
# from util.responsePack import response_package
# from util.setting import app


class CheckRegisteredParm(BaseEndpoint):

    async def post(self, request):
        registered_phone = request.json.get('registered_phone', None)
        if not registered_phone:
            raise exceptions.AuthenticationFailed(
                "注册手机号格式不正确"
            )
        if len(registered_phone) != 11:
            raise exceptions.AuthenticationFailed(
                "注册手机号格式不正确"
            )
        helper = MyCustomUserAuthHelper()
        return await helper.check_registered_phone(registered_phone=registered_phone)
