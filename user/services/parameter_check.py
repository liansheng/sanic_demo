#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: parameter_check.py
@time: 8/27/18 1:58 AM
"""
from bson import ObjectId


class ParameterCheck:

    def search_user_check(self, data):
        page_size = 20
        page_num = 1
        print("data is ", data, )
        # if "page_size" not in data.keys():
        data["page_size"] = 20
        if "page_num" not in data.keys():
            data["page_num"] = 1
        data["page_num"] = int(data["page_num"])
        assert data["type"] in ["followers", "following", "friend"], "参数错误"
        assert "user_id" in data.keys()
        assert ObjectId(data["user_id"])
        return data
