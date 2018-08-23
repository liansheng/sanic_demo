#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: db.py
@time: 8/8/18 7:18 PM
"""

import motor.motor_asyncio
import asyncio
from obj.util.setting import DATABASE_CONIFG

# client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_CONIFG["host"], DATABASE_CONIFG["port"])
# db = client["test_database"]
# collection = db["test_collection"]


class MyDataBase:
    def __init__(self, db_name="account_center", collection="test_collection"):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_CONIFG["host"], DATABASE_CONIFG["port"])
        self.db = self.client[db_name]
        self.loop = asyncio.get_event_loop()
        self.collection = self.db[collection]

    def set_collection(self, collection):
        self.collection = self.db[collection]

    def set_db(self, db_name):
        self.db = self.client[db_name]

    def insert_one(self, document):
        self.loop.run_until_complete(self.do_insert(document))

    async def do_insert(self, document=None):
        if document is None:
            pass
        result = await self.collection.insert_one(document)
        # print("result %s" % repr(result.inserted_id))
        return result.inserted_id

    def __str__(self):
        return "db name is {} , collection is {}".format(self.db, self.collection)


# async def do_insert(collection, document=None):
#     if not document:
#         document = {"test": "hello word"}
#         result = await collection.insert_one(document)
#         print("result %s" % repr(result.inserted_id))
#
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(do_insert(collection))

document = {"test1": "lase data2 "}

# mydb = MyDataBase()
# mydb.insert_one(document=document)
# print(mydb)
