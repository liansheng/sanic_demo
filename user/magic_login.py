#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: magic_login.py
@time: 8/10/18 2:57 AM
"""
from sanic_jwt import BaseEndpoint


class MagicLoginHandler(BaseEndpoint):
    async def options(self, request):
        return response.text('', status=204)

    async def post(self, request):
        helper = MyCustomUserAuthHelper(app, request)
        token = helper.get_make_me_a_magic_token()
        helper.send_magic_token_to_user_email()

        # Persist the token
        key = f'magic-token-{token}'
        await app.redis.set(key, helper.user.uuid)

        response = {
            'magic-token': token
        }
        return json(response)


def check_magic_token(request):
    token = request.json.get('magic_token', '')
    key = f'magic-token-{token}'

    retrieval = await
    request.app.redis.get(key)
    if retrieval is None:
        raise Exception('Token expired or invalid')
    retrieval = str(retrieval)

    user = User.get(uuid=retrieval)

    return user
