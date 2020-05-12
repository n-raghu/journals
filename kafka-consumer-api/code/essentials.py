import sys
from datetime import datetime as dtm


def delivery_report(err, m):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {m.topic()} [{m.partition()}]')


def get_kafka_ins():
    return '192.168.206.207:9092'


def get_topic():
    return 'jt-consumer-api_1', 'jt-consumer-api_1'
