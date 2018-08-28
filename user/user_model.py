#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: user_model.py
@time: 8/12/18 10:40 PM
"""
from obj.user.check_common_mothed import validate_phone, validate_must
from marshmallow import Schema, fields, validates, ValidationError, validate
from bson import ObjectId

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


class FansSchema(Schema):
    following = fields.Str()


class FollowingSchema(Schema):
    myself = fields.Str()


class FriendSchema(Schema):
    pass


if __name__ == '__main__':
    data_list = [{'_id': ObjectId('5b84e5e15f627dac33233cb2'), 'myself': '5b7cfbd45f627ddd88e2c929',
                  'following': '5b7e29dd5f627d0218528819'}]
    schema = FansSchema(many=True)
    result = schema.load(data_list)
    print(dir(result))
    print(result.data)
