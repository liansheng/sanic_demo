#!/usr/bin python3
# -*- coding: utf-8 -*-
# @File  : consumer.py
# @Author: Luzhenming
# @Date  : 8/6/2018
# @Desc  : 
"""
消费者
"""

from pykafka import KafkaClient


class ConsumerClient():
    """
    消费者客户端
    """

    def __init__(self, host, managed=True, consumer_group="consumer_group_0"):
        self.consumer_group = consumer_group
        self.managed = managed
        self.host = host
        self.client = KafkaClient(hosts=self.host)
        self.client

    def get_topic(self, topic_name):
        """
        获取topic
        :param topic_name:
        :return:
        """
        return self.client.topics[topic_name.encode()]

    def get_partitions(self, topic):
        """
        获取partition集
        :param topic:
        :return:
        """
        return topic.partitions

    def get_simple_consumer(self, topic, consumer_group, partitions):
        """
        获取指定offset消费的消费者
        :param consumer_group:
        :param partitions:
        :return:
        """
        if not consumer_group:
            consumer_group = self.consumer_group

        return topic.get_simple_consumer(consumer_group.encode(), partitions=[partitions])

    def get_balanced_consumer(self, topic, consumer_group=None):
        """
        获取均衡消费消费者
        :param topic:
        :param consumer_group:
        :param managed:
        :return:
        """
        if not consumer_group:
            consumer_group = self.consumer_group

        return topic.get_balanced_consumer(consumer_group.encode(), managed=self.managed)

    def get_earliest_offsets(self, topic_name, partition_index=0):
        """
        获取topic最早可用offset
        :param topic_name:
        :return:
        """
        topic = self.get_topic(topic_name)

        return topic.earliest_available_offsets()[partition_index].offset[0]

    def get_last_offsets(self, topic_name, partition_index=0):
        """
        获取topic最新可用的offset
        :param topic_name:
        :return:
        """
        topic = self.get_topic(topic_name)

        return topic.latest_available_offsets()[partition_index].offset[0]

    def simple_consumer(self, topic_name, offset=0, consumer_group=None, partition_index=0):
        """
        消费者指定offset消费
        :param topic_name:  topic名称
        :param offset:      指定消息偏移
        :param consumer_group:  消费者分组，默认使用self.consumer_group
        :param partition_index: 分区，默认使用 0
        :return: 队列消息
        """
        # 默认分组
        if not consumer_group:
            consumer_group = self.consumer_group

        topic = self.get_topic(topic_name)

        partitions = self.get_partitions(topic)

        # 选择一个分区
        partition = partitions[partition_index]

        # 获取消费者进行消费
        consumer = self.get_simple_consumer(topic, consumer_group, partition)

        # 设置消费者offset
        consumer.reset_offsets([(partition, offset)])

        # 消费
        msg = consumer.consume()

        return msg.value.decode()

import json

if __name__ == '__main__':
    """
    消费者使用示例
    """
    # 建立消费者客户端，consumer_group：消费者分组，每个主题下的分区只能被同一分组的消费者消费一次，可以任意指定分组，无须预先创建
    consumerClient = ConsumerClient("172.16.1.120:19092,172.16.1.121:19092,172.16.1.122:19092",
                                    consumer_group="consumer_group_11")
    # 指定topic,订阅主题，订阅不同的主题即可消费不同类型的消息
    topic = consumerClient.get_topic("message")
    # 获取负载均衡消费者客户端
    balanced_consumer = consumerClient.get_balanced_consumer(topic)

    while True:
        # 消费消息，该方法会阻塞线程，有新的消息进入队列才会继续执行
        consume = balanced_consumer.consume()
        c = consume.value.decode()
        print(" this is c")
        print(json.loads(c))
        print(consume.value.decode())

        # 消费消息完成后提交offset，不提交下次重启后会从上个提交点开始获取消息
        balanced_consumer.commit_offsets()
