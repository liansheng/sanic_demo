#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: logout_view.py
@time: 8/26/18 10:50 PM
"""

from sanic_jwt import BaseEndpoint
from sanic_jwt import utils
from sanic import response

from util.responsePack import response_package
from util.setting import app
import json


class LogoutEndpoint(BaseEndpoint):
    async def get(self, request):
        """
        :param request:
        :return:
        """
        print("begin logout ")
        payload = self.instance.auth.extract_payload(request, verify=False)
        user = await utils.call(
            self.instance.auth.retrieve_user, request, payload=payload
        )
        user_id = await self.instance.auth._get_user_id(user)
        logout_result = await utils.call(
            self.instance.auth.logout,
            request=request,
            user_id=user_id,
        )
        return response.json(response_package("200", {}))

    # async def post(self, request, *args, **kwargs):
    #     request, args, kwargs = await self.do_incoming(request, args, kwargs)
    #
    #     config = self.config
    #     user = await utils.call(
    #         self.instance.auth.authenticate, request, *args, **kwargs
    #     )
    #
    #     access_token, output = await self.responses.get_access_token_output(
    #         request, user, self.config, self.instance
    #     )
    #
    #     if config.refresh_token_enabled():
    #         refresh_token = await utils.call(
    #             self.instance.auth.generate_refresh_token, request, user
    #         )
    #         output.update({config.refresh_token_name(): refresh_token})
    #     else:
    #         refresh_token = None
    #
    #     output.update(
    #         self.responses.extend_authenticate(
    #             request,
    #             user=user,
    #             access_token=access_token,
    #             refresh_token=refresh_token,
    #         )
    #     )
    #
    #     output = await self.do_output(output)
    #     output.update({"user_info": user})
    #
    #     output = response_package("200", output)
    #     print("output is ", output)
    #     resp = self.responses.get_token_reponse(
    #         request,
    #         access_token,
    #         output,
    #         refresh_token=refresh_token,
    #         config=self.config,
    #     )
    #     resp.cookies["user_id"] = user.get("user_id", None)
    #     return await self.do_response(resp)
