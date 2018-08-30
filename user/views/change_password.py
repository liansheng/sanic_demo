#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: change_password.py
@time: 8/30/18 1:08 AM
"""

from sanic.views import HTTPMethodView
from sanic_jwt.decorators import protected
from sanic import response

from models.user_model import UserModel
from user.check_common_mothed import gen_password
from util.setting import app
from util.tools import get_user_id_by_request
from user.services.CheckServices import CheckServer
from util.responsePack import response_package

check_server = CheckServer()


class ChangePassword(HTTPMethodView):
    decorators = [protected()]

    def __init__(self):
        self.collection = app.mongo["account_center"].user
        self.user_model = UserModel(self.collection)

    async def post(self, request):
        try:
            user_id = await get_user_id_by_request(request)
            new_password = request.json.get("new_password", None)
            old_password = request.json.get("old_password", None)
            print(request.json)
            assert old_password, "原始密码未填写"
            assert new_password, "新密码未填写"

            doc = await check_server.is_user(user_id, self.user_model)
            assert doc["password"] == gen_password(old_password), "原始密码不对"
            await self.user_model.update_password(user_id, gen_password(new_password))
            return response.json(response_package("200", {}))
        except TimeoutError as e:
            return response.json(response_package("999", {"e": str(e)}))


