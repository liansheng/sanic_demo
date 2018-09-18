#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: content_definition.py
@time: 8/31/18 12:26 AM
"""
# message definition
# 关注12 ，加好友 13
MESSAGE_TYPE_MAP = {
    # "followers": "12",
    "following": "12",
    "friend": "13",
}

base = {
    "message_type": "1",
    "self_user_id": "str",
    "target_user_id": "str",
    "content": ""
}

# write kafka send user

USER_MESSAGE_TYPE_MAP = {
    "user_1": "login",
    "user_2": "register"
}
USER_MESSAGE_TYPE_ANTI_MAP = {
    "login": "user_1",
    "register": "user_2"
}

send_user = {'article_count': None,
             'created_time': '2018-08-22 20:28:29.406000',
             'firend_count': None,
             'followers_count': 8,
             'following_count': 4,
             'head_portrait': '/static/img/default_head_portrait.jpg',
             'is_add_bus_card': False,
             'is_add_id_card': False,
             'last_logging_time': '2018-09-05 14:34:39.387000',
             'name': '小蜜蜂nb',
             'qq': None,
             'registered_phone': '18119818122',
             'registration_sourece': None,
             'self_introduction': None,
             'user_id': '5b7e29dd5f627d0218528819',
             'wechat': None}
send_user_sum = {
    "head": {
        "message_type": "",
    },
    "body": "",
}

if __name__ == '__main__':
    from pprint import pprint

    pprint(send_user)
