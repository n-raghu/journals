import sys
from datetime import datetime as dtm


def delivery_report(err, m):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {m.topic()} [{m.partition()}]')


def encode_dtm(obj):
    if isinstance(obj, dtm):
        return {
            '__datetime__': True,
            'as_str': obj.strftime("%Y%m%dT%H:%M:%S")
        }
    return obj


def decode_dtm(obj):
    if '__datetime__' in obj:
        obj = dtm.strptime(obj["as_str"], "%Y%m%dT%H:%M:%S")
    return obj


def get_kafka_ins():
    return '192.168.206.207:9092'


def get_topic():
    return 'jt-producer-3p'
