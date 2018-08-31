#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: content_definition.py
@time: 8/31/18 12:26 AM
"""
# message definition
MESSAGE_TYPE_MAP = {
    "1": "followers",
    "2": "following",
    "3": "friend",
}

base = {
    "message_type": "1",
    "self_user_id": "str",
    "target_user_id": "str",
}
