#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: producerServer.py
@time: 9/2/18 10:47 PM
"""
from util.kafka.content_definition import MESSAGE_TYPE_MAP, base, send_user_sum, USER_MESSAGE_TYPE_ANTI_MAP

data = {"head":
    {
        "to": "",
        "type": ""
    },
    "body": ""}


class ProductServer:

    # def send_follow_to_message(self, app, self_user_id, target_user_id):
    async def send_add_follow_relationship_message(self, app, self_user_id, target_user_id):
        """
        self_user_id  following target_user_id
        :param app:
        :param self_user_id:
        :param target_user_id:
        :return:
        """

        pass

    async def send_friend_to_message(self, app, self_user_id, target_user_id, self_user_name):
        """
        {"head": {"to": "string 推送给具体用户的用户ID", "type": "string 消息类型代码"}, "body": 数据类型自定义，内容自定义}
        * body中的内容消息微服务不做任何处理直接推送给客户端,
        :param app:
        :param self_user_id:
        :param target_user_id:
        :return:
        """
        base["message_type"] = MESSAGE_TYPE_MAP["friend"]
        base["self_user_id"] = self_user_id
        base["target_user_id"] = target_user_id
        base["content"] = "{}XX关注了你，可以互相聊天了".format(self_user_name)

        data = {"head": {"to": "", "type": ""}, "body": ""}
        data["head"]["to"] = str(target_user_id)
        data["head"]["type"] = MESSAGE_TYPE_MAP["friend"]
        data["head"]["from"] = str(self_user_id)
        data["body"] = "{}XX关注了你，可以互相聊天了".format(self_user_name)

        await app.producer.send("message", data)
        pass

    async def send_following_to_message(self, app, self_user_id, target_user_id, self_user_name):
        """
        :param app:
        :param self_user_id:
        :param target_user_id:
        :return:
        """
        base["message_type"] = MESSAGE_TYPE_MAP["following"]
        base["self_user_id"] = self_user_id
        base["target_user_id"] = target_user_id
        base["content"] = "{}关注了你，关注对方开启聊天".format(self_user_name)

        data = {"head": {"to": "", "type": ""}, "body": ""}
        data["head"]["to"] = str(target_user_id)
        data["head"]["type"] = MESSAGE_TYPE_MAP["following"]
        data["body"] = "{}关注了你，关注对方开启聊天".format(self_user_name)

        await app.producer.send("message", data)

    async def send_someone_else_logged_to_message(self, app, target_user_id):
        """
        :param app:
        :param target_user_id:
        :return:
        """
        data["head"]["to"] = str(target_user_id)
        data["head"]["type"] = "16"
        data["body"] = "该账号已在其他手机登录，如非本人请赶紧登录并修改密码"
        await app.producer.send("message", data)

    # async def send_followers_to_message(self, app, self_user_id, target_user_id):
    #     """
    #     :param app:
    #     :param self_user_id:
    #     :param target_user_id:
    #     :return:
    #     """
    #     base["message_type"] = MESSAGE_TYPE_MAP["followers"]
    #     base["self_user_id"] = self_user_id
    #     base["target_user_id"] = target_user_id
    #     await app.producer.send("message", base)
    #     pass


class SendServer:
    async def send_to(self, app, topic, message_type, body):
        send_user_sum["head"]["message_type"] = USER_MESSAGE_TYPE_ANTI_MAP.get(message_type, None)
        send_user_sum["body"] = body
        await app.producer.send(topic, send_user_sum)
