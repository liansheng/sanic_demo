#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: model.py
@time: 8/16/18 2:18 AM
"""
from __future__ import print_function
from __future__ import unicode_literals

from bson import ObjectId
from obj.util.basic.basemodel import BaseModel


class MongoDBModel(BaseModel):
    coll_name = None
    fields = None

    def __init__(self, collection):
        self.collection = collection
        self.on_init()

    def on_init(self):
        pass

    @staticmethod
    def __transform_doc(doc):
        doc['_id'] = str(doc['_id'])
        return doc

    def get_valid_obj(self, obj):
        # check fields
        valid_obj = {}

        if not self.fields:
            valid_obj = obj.copy()
        else:
            for f in self.fields:
                valid_obj[f] = obj[f]
        return valid_obj

    def find(self, *args, **kwargs):
        # print("args ", args)
        # print("kwargs ", kwargs)
        # if kwargs:
        docs = self.collection.find(kwargs).to_list(length=100)
        return docs

    def find_list(self, *args, **kwargs):
        print("kw is ", kwargs)
        docs = self.collection.find(kwargs)
        return docs

    def raw_find(self, obj):
        docs = self.collection.find(obj)
        return docs

    def find_one(self, **kwargs):
        doc = self.collection.find_one(kwargs)
        return None if doc is None else doc

    def find_by_id(self, id):
        doc = self.collection.find_one({'_id': ObjectId(id)})
        return None if doc is None else doc

    def create(self, obj):
        # valid_obj = self.get_valid_obj(obj)
        result = self.collection.insert_one(obj)
        return result

    def update_by_id(self, id, obj):
        # doc = self.find_by_id(id)
        # if doc is None:
        #     return None

        valid_obj = self.get_valid_obj(obj)
        self.collection.update_one(
            {'_id': ObjectId(id)},
            {'$set': valid_obj}
        )
        doc = self.find_by_id(id)
        if doc is None:
            return None
        return doc

    def remove_by_id(self, id):
        doc = self.find_by_id(id)
        if doc is None:
            return False
        else:
            self.collection.delete_one({'_id': ObjectId(id)})
            return True

    def inc_field_by_user_id(self, user_id, field, number):
        self.collection.update_one({"_id": ObjectId(user_id)}, {"$inc": {field: number}})
