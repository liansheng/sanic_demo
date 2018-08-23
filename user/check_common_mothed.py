#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: check_common_mothed.py
@time: 8/12/18 10:52 PM
"""
import re
from marshmallow import ValidationError
from sanic.exceptions import SanicException
import time
import hashlib

def validate_must(field):
    if not field:
        raise SanicException("{} is must".format(field))


def validate_phone(phone):
    phone_pat = re.compile('^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$')
    res = re.match(phone_pat, phone)
    # print("validate_phone res : ", res)
    if not res:
        raise SanicException("{} 手机号格式不正确".format(phone))


def md5(mystr):
    m = hashlib.md5()
    m.update(mystr.encode('utf-8'))
    return m.hexdigest()


def gen_password(pwd):
    return md5("sdg#$%#@DSF" + pwd)


if __name__ == "__main__":
    p = "13435651234"
    validate_phone(p)
