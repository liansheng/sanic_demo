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

from models.user_model import UserModel
from user.user_marshal import UserReadModel
from util.setting import app
from util.tools import get_user_id_by_request
from util.responsePack import response_package


class EditView(HTTPMethodView):
    decorators = [protected()]
    fields = ["self_introduction", "name"]

    def __init__(self):
        self.collection = app.mongo["account_center"].user
        self.user_model = UserModel(self.collection)

    async def patch(self, request):
        try:
            user_id = await get_user_id_by_request(request)
            data = request.json
            new_data = {}
            for k, v in data.items():
                if k not in self.fields:
                    continue
                new_data[k] = v
            doc = await self.user_model.update_by_id(user_id, new_data)
            return response.json(response_package("200", UserReadModel(data=doc, status="").to_dict()))
        except TimeoutError as e:
            return response.json(response_package("999", {"e": str(e)}))
