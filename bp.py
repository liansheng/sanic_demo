#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: 01_bp.py
@time: 8/3/18 3:29 AM
"""
from sanic import Blueprint
from sanic.response import text

bp = Blueprint("first_bp")


@bp.route("/get_info")
async def get_info(request):
    return text("it is ok!")
