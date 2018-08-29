#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: my_consumer.py
@time: 8/21/18 6:50 PM
"""

from util.config import kafka_host
from kafka import KafkaConsumer
import json

if __name__ == '__main__':
    consumer = KafkaConsumer("user", bootstrap_servers=kafka_host, group_id="group111",
                             value_deserializer=lambda m: json.loads(m.decode('ascii')),
                             consumer_timeout_ms=1000)
    # for msg in consumer:
    #     print(msg)
    msg = next(consumer)
    print(msg.value)
