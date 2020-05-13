import sys
import pickle
from datetime import datetime as dtm

from confluent_kafka import Producer

from essentials import get_kafka_ins, get_topic
from essentials import encode_dtm, delivery_report


def gen_msg(n):
    return {
        'msg': f'msg-{n}',
        'timestamp': dtm.now(),
    }


producer_cfg = {
    'bootstrap.servers': get_kafka_ins(),
}

P = Producer(producer_cfg)

for _i in range(5):
    P.produce(
        get_topic(),
        value=pickle.dumps(gen_msg(_i)),
        headers={
            'msg_version': 'v1',
        },
        callback=delivery_report,
    )
    P.poll(0.5)
