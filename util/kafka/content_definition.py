#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: content_definition.py
@time: 8/31/18 12:26 AM
"""
# message definition
MESSAGE_TYPE_MAP = {
    "followers": "12",
    "following": "13",
    "friend": "14"
}

base = {
    "message_type": "1",
    "self_user_id": "str",
    "target_user_id": "str",
    "content": ""
}
