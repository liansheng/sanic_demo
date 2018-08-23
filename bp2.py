#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: 01_bp.py
@time: 8/3/18 3:29 AM
"""
from sanic import Blueprint
from sanic.response import text

bp2 = Blueprint("first_bp2", url_prefix="/api/v1")

from sanic import Sanic
from sanic.views import HTTPMethodView
from sanic.response import text, json
from sanic.exceptions import ServerError
from sanic_jwt.decorators import protected


# app = Sanic('some_name')


class SimpleView(HTTPMethodView):
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


bp2.add_route(SimpleView.as_view(), "/view")
bp2.add_route(SimpleView2.as_view(), "/view2")
# app.add_route(SimpleView.as_view(), '/')


# @bp2.route("/get_info2")
# async def get_info(request):
#     return text("it is ok!")
