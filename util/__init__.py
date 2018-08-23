#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: __init__.py
@time: 8/5/18 7:53 PM
"""
from sanic.exceptions import (
    SanicException,
    add_status_code
)


@add_status_code(200)
class Expe(SanicException):
    pass
