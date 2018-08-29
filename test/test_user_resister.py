#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: test_user_resister.py
@time: 8/12/18 10:45 PM
"""
from user.user_model import UserResisterSchema

if __name__ == "__main__":
    in_data = {"phone": "18819323232", "password": "1234123"}
    in_data2 = {"phone": "18819323232", "password": "12"}
    schema = UserResisterSchema()
    result = schema.load(in_data)
    print(dir(result))
    print(result.errors)
    print(result.data)
    result, errors = schema.dump(in_data2)
    print(result, errors)

