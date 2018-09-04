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
from util.basic.basemodel import BaseModel


class MongoDBModel(BaseModel):
    coll_name = None
    fields = None

    def __init__(self, collection):
        self.collection = collection
        """
        ['__call__', '__class__', '__delattr__', '__delegate_class__', '__dict__', '__dir__', 
        '__doc__', '__eq__', '__format__', '__ge__', '__getattr__', '__getattribute__', 
        '__getitem__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', 
        '__lt__', '__module__', '__motor_class_name__', '__ne__', '__new__', '__reduce__',
         '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__',
          '__weakref__', '_async_aggregate', '_async_aggregate_raw_batches', '_async_list_indexes',
           '_framework', 'aggregate', 'aggregate_raw_batches', 'bulk_write', 'codec_options', 
           'count_documents', 'create_index', 'create_indexes', 'database', 'delegate', 
           'delete_many', 'delete_one', 'distinct', 'drop', 'drop_index', 'drop_indexes',
            'estimated_document_count', 'find', 'find_one', 'find_one_and_delete', 
            'find_one_and_replace', 'find_one_and_update', 'find_raw_batches', 
            'full_name', 'get_io_loop', 'index_information', 'inline_map_reduce',
             'insert_many', 'insert_one', 'list_indexes', 'map_reduce', 'name', 
             'options', 'read_concern', 'read_preference', 'reindex', 'rename', 
             'replace_one', 'update_many', 'update_one', 'watch', 'with_options',
              'wrap', 'write_concern']

        """
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
        print("raw_find obj is ", obj)
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

    async def update_many(self, criteria, objNew, upsert=False, multi=True):
        """
        :param criteria:
        :param objNew:
        :param upsert:
        :param multi:
        :return:
        """
        docs = await self.collection.update_many(criteria, objNew)
        return docs if docs else None

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

    async def trans_obj_id(self, obj):
        if "_id" in obj.keys():
            obj["id"] = str(obj.pop("_id"))
        return obj
