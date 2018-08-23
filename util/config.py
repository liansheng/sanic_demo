#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: config.py.py
@time: 8/21/18 6:49 PM
"""
import os

kafka_host = "172.16.1.121:19092,172.16.1.122:19092"  # 172.16.1.120:19092

default_head_portrait = "/static/img/default_head_portrait.jpg"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_IMG_DIR = os.path.join(BASE_DIR, "static", "img")

REDIS_CONFIG = {"redis": ("localhost", 6379)}
CAPTCHA_URL = os.path.join(STATIC_IMG_DIR, "captcha.png")


if __name__ == '__main__':
    print(CAPTCHA_URL)
