#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: my_auth.py
@time: 8/5/18 8:36 PM
"""
from sanic import Sanic
from sanic_jwt import exceptions
from sanic_jwt import initialize
from obj.util.globals import r
from sanic import response
from sanic.response import json


class User:

    def __init__(self, id, username, password):
        self.user_id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return "User(id='{}')".format(self.user_id)

    def to_dict(self):
        return {"user_id": self.user_id, "username": self.username}
        # properties = ['user_id', 'username', 'email', 'verified']
        # return {prop: getattr(self, prop, None) for prop in properties}


# users = [User(1, "user1", "abcxyz"), User(2, "user2", "abcxyz")]
#
# username_table = {u.username: u for u in users}
# userid_table = {u.user_id: u for u in users}
#
#
# async def authenticate(request, *args, **kwargs):
#     print(dir(request))
#     print(request.headers)
#     print(request.token)
#     username = request.json.get("username", None)
#     password = request.json.get("password", None)
#
#     if not username or not password:
#         raise exceptions.AuthenticationFailed("Missing username or password.")
#
#     user = username_table.get(username, None)
#     if user is None:
#         raise exceptions.AuthenticationFailed("User not found.")
#
#     if password != user.password:
#         raise exceptions.AuthenticationFailed("Password is incorrect.")
#
#     return user
#
#
# async def store_refresh_token(user_id, refresh_token, *args, **kwargs):
#     key = "refresh_token_{user_id}".format(user_id=user_id)
#     r.set(key, refresh_token)
#
#
# async def retrieve_refresh_token(request, user_id, *args, **kwargs):
#     key = "refresh_token_{user_id}".format(user_id=user_id)
#     await r.get(key)
#
#
# def get_user_by_id(user_id):
#     for tmp in users:
#         if tmp.user_id == user_id:
#             return tmp
#
#
# async def my_extender(payload, user):
#     print(payload, user, " this is extender")
#     # username = user.to_dict().get("username")
#     # payload.update({"username": username})
#     return payload
#
#
# async def retrieve_user(request, payload, *args, **kwargs):
#     if payload:
#         print(payload)
#         print(request.cookies)
#         user_id = payload.get("user_id", None)
#         user = get_user_by_id(user_id)
#         return user
#     else:
#         return {}
