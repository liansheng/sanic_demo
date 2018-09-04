#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: producerServer.py
@time: 9/2/18 10:47 PM
"""
from util.kafka.content_definition import MESSAGE_TYPE_MAP, base


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

        :param app:
        :param self_user_id:
        :param target_user_id:
        :return:
        """
        base["message_type"] = MESSAGE_TYPE_MAP["friend"]
        base["self_user_id"] = self_user_id
        base["target_user_id"] = target_user_id
        base["content"] = "{}XX关注了你，可以互相聊天了".format(self_user_name)
        await app.producer.send("message", base)
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
        print("base is ", base)
        await app.producer.send("message", base)
        pass

    async def send_followers_to_message(self, app, self_user_id, target_user_id):
        """
        :param app:
        :param self_user_id:
        :param target_user_id:
        :return:
        """
        base["message_type"] = MESSAGE_TYPE_MAP["followers"]
        base["self_user_id"] = self_user_id
        base["target_user_id"] = target_user_id
        await app.producer.send("message", base)
        pass
