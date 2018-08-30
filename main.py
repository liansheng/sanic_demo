#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: main.py
@time: 8/3/18 3:30 AM
"""
import os

from aoiklivereload.aoiklivereload import LiveReloader

from user.views.following_view import user_bp
from sanic_jwt import initialize

from user.views.check_view import CheckRegisteredParm
from user.views.login import MyAuthenticateEndpoint
from user.views.login_view import MyAuthentication
from user.views.registered_view import Register, Captcha
from user.views.logout_view import LogoutEndpoint
from user.views.refresh_endpoint import MyRefreshEndpoint
# from util.kafka.producer import ProducerClient
from util.setting import app
from sanic_jwt import utils

reloader = LiveReloader()
reloader.start_watcher_thread()

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

app.blueprint(user_bp)


@app.middleware('request')
async def print_on_request(request):
    # print(type(app.config.MONGO_URIS))
    # print(app.config.MONGO_URIS)
    print("I print when a request is received by the server")
    # print(type(request))
    # print(dir(request))

    # payload = request.app.auth.extract_payload(request, verify=False)
    # user = await utils.call(
    #     request.app.auth.retrieve_user, request, payload=payload
    # )
    # user_id = await request.app.auth._get_user_id(user)
    # print("payload is ", payload)
    # print("user id ", user)
    # print("user_id", user_id)
    return request


@app.middleware('response')
async def print_on_response(request, response):
    print("I print when a response is returned by the server")
    # print(dir(response))


# from sanic.response import json
#
#
# class MyResponses(Responses):
#
#     @staticmethod
#     def exception_response(request, exception):
#         exception_message = str(exception)
#         return json({
#             'error': True,
#             'message': f'You encountered an exception: {exception_message}'
#         }, status=exception.status_code)


i = initialize(
    app,
    refresh_token_enabled=True,
    class_views=(('/register', Register), ("/check_phone", CheckRegisteredParm),
                 ("/login", MyAuthenticateEndpoint), ("/logout", LogoutEndpoint),
                 ("/refresh_token", MyRefreshEndpoint), ("/captcha", Captcha)),
    authentication_class=MyAuthentication,
    # cookie_domain="sendMe.com",
)
if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=9999)
    app.run(host="0.0.0.0", port=9999, debug=True)
