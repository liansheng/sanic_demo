#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: config.py.py
@time: 8/21/18 6:49 PM
"""
import socket
import os

kafka_host = "172.16.1.120:19092, 172.16.1.121:19092, 172.16.1.122:19092"

default_head_portrait = "/static/img/default_head_portrait.png"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_IMG_DIR = os.path.join(BASE_DIR, "static", "img")
CAPTCHA_URL = os.path.join(STATIC_IMG_DIR, "captcha.png")

hostname = socket.gethostname()
if hostname == "ubuntu":

    REDIS_CONFIG = {"redis": ("localhost", 6379)}
    DATABASE_CONFIG = {
        "host": "localhost",
        "port": 27017,
        "name": "account_center",
    }
else:
    REDIS_CONFIG = {"redis": ("192.168.1.220", 6379, "fawo")}
    DATABASE_CONFIG = {
        "host": "192.168.1.220",
        "port": 27017,
        "name": "account_center",
    }

if __name__ == '__main__':
    print(CAPTCHA_URL)
