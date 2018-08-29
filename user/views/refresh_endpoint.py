#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: refresh_endpoint.py
@time: 8/26/18 8:34 PM
"""
from sanic_jwt import BaseEndpoint, utils, exceptions

from util.responsePack import response_package


class MyRefreshEndpoint(BaseEndpoint):

    async def post(self, request, *args, **kwargs):
        request, args, kwargs = await self.do_incoming(request, args, kwargs)

        # TODO:
        # - Add more exceptions
        payload = self.instance.auth.extract_payload(request, verify=False)
        user = await utils.call(
            self.instance.auth.retrieve_user, request, payload=payload
        )
        user_id = await self.instance.auth._get_user_id(user)
        refresh_token = await utils.call(
            self.instance.auth.retrieve_refresh_token,
            request=request,
            user_id=user_id,
        )
        if isinstance(refresh_token, bytes):
            refresh_token = refresh_token.decode("utf-8")

        purported_token = await self.instance.auth.retrieve_refresh_token_from_request(
            request
        )

        if refresh_token != purported_token:
            raise exceptions.AuthenticationFailed()

        access_token, output = await self.responses.get_access_token_output(
            request, user, self.config, self.instance
        )
        output = response_package("200", output)
        output.update(
            self.responses.extend_refresh(
                request,
                user=user,
                access_token=access_token,
                refresh_token=refresh_token,
                purported_token=purported_token,
                payload=payload,
            )
        )
        output = await self.do_output(output)

        resp = self.responses.get_token_reponse(
            request, access_token, output, config=self.config
        )

        return await self.do_response(resp)
