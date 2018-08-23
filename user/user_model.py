#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: user_model.py
@time: 8/12/18 10:40 PM
"""
from obj.user.check_common_mothed import validate_phone, validate_must
from marshmallow import Schema, fields, validates, ValidationError, validate

E = {
    'required': '参数是必须的',
    'type': '类型错误',  # used by Unmarshaller
    'null': '参数不能为空',
    # 'validator_failed': 'Invalid value.'
}


class UserResisterSchema(Schema):
    registered_phone = fields.Str(validate=[validate_phone])
    password = fields.Str(validate=[validate.Length(min=6, max=20)])


class RegisterPhoneSchema(Schema):
    # registered_phone = fields.Str(validate=[validate_phone], required=True, error_messages=E)
    registered_phone = fields.Str(validate=[validate_phone])
