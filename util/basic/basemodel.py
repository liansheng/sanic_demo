#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: basemodel.py
@time: 8/15/18 11:17 PM
"""
from __future__ import print_function
from __future__ import unicode_literals


class BaseModel(object):

    def find(self):
        raise NotImplementedError

    def find_by_id(self, id):
        raise NotImplementedError

    def create(self, obj):
        raise NotImplementedError

    def update_by_id(self, id, obj):
        raise NotImplementedError

    def remove_by_id(self, id):
        raise NotImplementedError
