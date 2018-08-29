#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: tools.py
@time: 8/13/18 3:34 AM
"""
import random
import string
from functools import wraps
from sanic_jwt import utils


def format_res(obj):
    print("obj is ", obj)
    if isinstance(obj, (list, tuple)) and isinstance(obj[0], (list, tuple)):
        l = []
        for tmp in obj:
            l += list(tmp)
        return format_res(l)
    if isinstance(obj, (list, tuple)) and isinstance(obj[0], dict):
        # [ {} ]
        d = {}
        for tmp in obj:
            d.update(tmp)
        for k, v in d.items():
            if isinstance(v, list):
                d[k] = " ".join(v)
        return " ".join(["{} {}".format(k, v) for k, v in d.items()])
    elif isinstance(obj, (list, tuple)):
        return obj[0]
    elif isinstance(obj, dict):
        return " ".join(["{} {}".format(k, v) for k, v in obj.items()])
    else:
        return str(obj)


def singleton(cls):
    """
    A singleton created by using decorator
    :param cls: cls
    :return: instance
    """
    _instances = {}

    @wraps(cls)
    def instance(*args, **kw):
        if cls not in _instances:
            _instances[cls] = cls(*args, **kw)
        return _instances[cls]

    return instance


RANDOM_CHAR_SET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def random_str(l=8):
    res = ""
    for i in range(l):
        res += random.choice(RANDOM_CHAR_SET)
    return res


#
# def random_int(a=0, b=9, l=5):
#     res = ""
#     for i in range(l):
#         res += str(random.randint(a, b))
#     return res
import time


def exeTime(func):
    def newFunc(*args, **args2):
        t0 = time.time()
        print("@%s, {%s} start" % (time.strftime("%X", time.localtime()), func.__name__))
        back = func(*args, **args2)
        print("@%s, {%s} end" % (time.strftime("%X", time.localtime()), func.__name__))
        print("@%.3fs taken for {%s}" % (time.time() - t0, func.__name__))
        return back

    return newFunc


async def get_user_id_by_request(request):
    payload = request.app.auth.extract_payload(request, verify=False)
    user = await utils.call(
        request.app.auth.retrieve_user, request, payload=payload
    )
    user_id = await request.app.auth._get_user_id(user)
    return user_id


if __name__ == '__main__':
    print(random_str(5))
    # print(random_int())
    print(format_res(([{'registered_phone': '18119871135 已被注册'}],)))
