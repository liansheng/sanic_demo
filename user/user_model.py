#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: user_model.py
@time: 8/12/18 10:40 PM
"""
import datetime
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


class WriteFollowInfoSchema(Schema):
    name = fields.Str(attribute="myself_name")
    head_portrait = fields.Str(attribute="myself_head_portrait")
    id = fields.Str(attribute="myself_user_id")


class WriteSelfFollowInfoSchema(Schema):
    name = fields.Str(attribute="myself_name", required=True)
    head_portrait = fields.Str(attribute="myself_head_portrait", required=True)
    id = fields.Str(attribute="myself_user_id", required=True)


class WriteFollowingFollowInfoSchema(Schema):
    name = fields.Str(attribute="following_name", required=True)
    head_portrait = fields.Str(attribute="following_hsead_portrait", required=True)
    id = fields.Str(attribute="following_user_id", required=True)


def test1():
    data = {'id': '5b7e29dd5f627d0218528819', 'name': 'fawoaKNNgOTx', 'registered_phone': '18119818122',
            'password': '1aed525ccb40311ef37ba08d5d7b53fa',
            'created_time': datetime.datetime(2018, 8, 22, 20, 28, 29, 406000),
            'registration_source': 'phone', 'self_introduction': None, 'qq': None, 'wechat': None,
            'gender': '未填写', 'head_portrait': '/static/img/default_head_portrait.jpg', 'is_add_id_card': False,
            'is_add_bus_card': False, 'last_logging_time': datetime.datetime(2018, 8, 28, 1, 37, 6, 100000),
            'bus_card_info': None, 'id_card_info': None, 'following_count': 1, 'followers_count': 3, 'friend_count': 0}
    schema = WriteFollowingFollowInfoSchema()
    result = schema.load(data)
    print(result.data)


def test2():
    class UserSchema(Schema):
        name = fields.String()
        email = fields.Email(data_key='emailAddress')

    s = UserSchema()

    data = {
        'name': 'Mike',
        'email': 'foo@bar.com'
    }
    result = s.dump(data)
    print(result)
    # {'name': u'Mike',
    # 'emailAddress': 'foo@bar.com'}

    data = {
        'name': 'Mike',
        'emailAddress': 'foo@bar.com'
    }
    result = s.load(data)
    print(result)


if __name__ == '__main__':
    # data_list = [{'_id': ObjectId('5b84e5e15f627dac33233cb2'), 'myself': '5b7cfbd45f627ddd88e2c929',
    #               'following': '5b7e29dd5f627d0218528819'}]
    # schema = FansSchema(many=True)
    # result = schema.load(data_list)
    # print(dir(result))
    # print(result.data)
    test1()
