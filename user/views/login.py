#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: login.py
@time: 8/19/18 11:13 PM
"""
from sanic_jwt import BaseEndpoint
from sanic_jwt import utils

from obj.util.responsePack import response_package
from obj.util.setting import app
import json


class MyAuthenticateEndpoint(BaseEndpoint):

    async def post(self, request, *args, **kwargs):
        request, args, kwargs = await self.do_incoming(request, args, kwargs)

        config = self.config
        user = await utils.call(
            self.instance.auth.authenticate, request, *args, **kwargs
        )

        access_token, output = await self.responses.get_access_token_output(
            request, user, self.config, self.instance
        )

        if config.refresh_token_enabled():
            refresh_token = await utils.call(
                self.instance.auth.generate_refresh_token, request, user
            )
            output.update({config.refresh_token_name(): refresh_token})
        else:
            refresh_token = None

        output.update(
            self.responses.extend_authenticate(
                request,
                user=user,
                access_token=access_token,
                refresh_token=refresh_token,
            )
        )

        output = await self.do_output(output)
        output.update({"user_info": user})

        output = response_package("200", output)
        print("output is ", output)
        resp = self.responses.get_token_reponse(
            request,
            access_token,
            output,
            refresh_token=refresh_token,
            config=self.config,
        )
        resp.cookies["user_id"] = user.get("user_id", None)
        await self.send_login_info_to_kafka(user)
        return await self.do_response(resp)

    async def send_login_info_to_kafka(self, user):
        # app.producerClient.sync_produce_message("user", message=json.dumps(user))
        # app.producerClient.sync_produce_message("user", message=json.dumps(user))
        print("send user is ", user)
        await app.producer.send("user", user)
        return True
