#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: WriteServices.py
@time: 8/28/18 1:55 AM
"""
from user.user_model import (
    WriteFollowInfoSchema,
    WriteSelfFollowInfoSchema,
    WriteFollowingFollowInfoSchema,
    WriteFriendSchema)
from util.kafka.productServer import ProductServer

kafka_server = ProductServer()


class WriteModelServer:
    async def write_follower_relationship(self, app, follower_model, user_model, friends_model, login_user_id,
                                          following_user_id):
        """
        Service segmentation
        :param app:
        :param follower_model:
        :param user_model:
        :param friends_model:
        :param login_user_id:
        :param following_user_id:
        :return:
        """
        # 1  I(login_user_id) well following other p(following_user_id)
        # Can't write Chinese orzzzzzzzzzzzzzzzzzzz
        doc = await user_model.find_by_id(login_user_id)
        new_doc = await user_model.trans_obj_id(doc)
        self_schema = WriteSelfFollowInfoSchema()
        login_data = self_schema.load(new_doc)
        assert not login_data.errors, ("关注数据异常", login_data.errors)
        # print(login_data.errors)
        # print("result data ", login_data.data)
        # print("login_user_id info ", doc)
        # 2
        follow_doc = await user_model.find_by_id(following_user_id)
        new_follow_doc = await user_model.trans_obj_id(follow_doc)
        follower_schema = WriteFollowingFollowInfoSchema()
        follow_data = follower_schema.load(new_follow_doc)
        # print("new_follow_doc is ", new_follow_doc)
        # print("follow_data is ", follow_data.data)
        # print(follow_data.errors)
        assert not follow_data.errors, ("关注数据异常", follow_data.errors)

        friend_schema = WriteFriendSchema()
        friend_data = friend_schema.load(new_follow_doc)
        assert not friend_data.errors, ("关注数据异常", friend_data.errors)

        # gen data, write data to collection
        res = await follower_model.update_or_created_follow_relationship_by_data(login_data.data, follow_data.data)
        # test
        await kafka_server.send_following_to_message(app, login_user_id, following_user_id,
                                                     login_data.data["myself_name"])
        if res is not "existed":

            # if login id have not follow relationship. then inc following and followers count
            # 3 a->b check, a is <- b, then add friend relationship
            if await follower_model.check_is_mutual_follow(login_user_id, following_user_id):
                # await friends_model.add(login_user_id, following_user_id)
                await friends_model.add_data(login_data.data, friend_data.data)
                await friends_model.add_data(self_schema.load(new_follow_doc).data, friend_schema.load(new_doc).data)
                await app.redis.sadd("{}_{}".format(login_user_id, "friends"), following_user_id)
                await app.redis.sadd("{}_{}".format(following_user_id, "friends"), login_user_id)
                # send msg to kafka message
                await kafka_server.send_friend_to_message(app, login_user_id, following_user_id,
                                                          login_data.data["myself_name"])
            else:
                # send msg to kafka message
                await kafka_server.send_following_to_message(app, login_user_id, following_user_id,
                                                             login_data.data["myself_name"])

            # 4 update or created follow redis
            await user_model.add_follow_count(login_user_id, following_user_id)
            if isinstance(following_user_id, bytes):
                following_user_id = following_user_id.decode()
            await app.redis.sadd("{}_{}".format(login_user_id, "follower"), following_user_id)

    async def write_unfollower_relationship(self, app, follower_model, user_model, friends_model, login_user_id,
                                            following_user_id):
        """
        Service segmentation
        :param app:
        :param follower_model:
        :param user_model:
        :param friends_model:
        :param login_user_id:
        :param following_user_id:
        :return:
        """
        # 1  I(login_user_id) well un following other p(following_user_id)
        # Can't write Chinese orzzzzzzzzzzzzzzzzzzz
        # doc = await user_model.find_by_id(login_user_id)
        # new_doc = await user_model.trans_obj_id(doc)
        # self_schema = WriteSelfFollowInfoSchema()
        # login_data = self_schema.load(new_doc)
        # assert not login_data.errors, ("关注数据异常", login_data.errors)
        # # print(login_data.errors)
        # # print("result data ", login_data.data)
        # # print("login_user_id info ", doc)
        # # 2
        # follow_doc = await user_model.find_by_id(following_user_id)
        # new_follow_doc = await user_model.trans_obj_id(follow_doc)
        # follower_schema = WriteFollowingFollowInfoSchema()
        # follow_data = follower_schema.load(new_follow_doc)
        # # print("new_follow_doc is ", new_follow_doc)
        # # print("follow_data is ", follow_data.data)
        # # print(follow_data.errors)
        # assert not follow_data.errors, ("关注数据异常", follow_data.errors)

        # res = await follower_model.update_or_created_follow_relationship(login_user_id, following_user_id)
        res = await follower_model.delete_follow_relationship(login_user_id, following_user_id)
        if res is not "is_null":
            # if login id have not follow relationship. then inc following and followers count
            # 3 delete friend relationship
            await friends_model.remove(login_user_id, following_user_id)
            await friends_model.remove(following_user_id, login_user_id)
            await app.redis.srem("{}_{}".format(login_user_id, "friends"), following_user_id)
            await app.redis.srem("{}_{}".format(following_user_id, "friends"), login_user_id)

            # 4 update or created redis
        await user_model.sub_follow_count(login_user_id, following_user_id)
        await app.redis.srem("{}_{}".format(login_user_id, "follower"), following_user_id)
