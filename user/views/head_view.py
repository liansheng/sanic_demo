#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: head_view.py
@time: 8/30/18 7:50 PM
"""
import hashlib
import os
from sanic.response import json
from sanic.views import HTTPMethodView
from util.config import HEAD_PATH
from PIL import Image


# 获取图片后缀名
def get_suffix(filename):
    temp_addr = filename.split('.')
    suffix = temp_addr[-1]
    file_type = ['jpg', 'jpeg', 'gif', 'png']
    assert len(temp_addr) >= 2, ("错误的文件名", "upload file name is {}".format(filename))
    assert suffix in file_type, ("错误的文件格式", "upload file name is {}".format(filename))
    return suffix
