#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: resister_view.py
@time: 8/12/18 8:02 PM
"""
from sanic_jwt import BaseEndpoint, initialize
from sanic_jwt.exceptions import AuthenticationFailed

from sanic_jwt import initialize, Authentication, exceptions, Responses
from util.marshal_with.data_check import MarshalWith, typeassert
from user.user_model import UserResisterSchema
from util.database.my_database import MyDataBase
from user.user_marshal import UserResister
from util.marshal_with.data_check import typeassert
from models.user_model import UserModel


# from main import database
# from process_app import database



# auth_bp = i.bp
# @auth_bp.listener("before_server_start")
# def set_db(app, loop):
#
