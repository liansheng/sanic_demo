#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: globals.py
@time: 8/5/18 10:55 PM
"""
import redis


REDIS_CONFIG = {"host": "127.0.0.1", "port": 6379}
r = redis.Redis(host=REDIS_CONFIG['host'], port=REDIS_CONFIG["port"])



