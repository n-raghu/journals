import sys
from datetime import datetime as dtm

from msgpack import packb
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
        value=packb(
            gen_msg(_i),
            default=encode_dtm,
            use_bin_type=True,
        ),
        headers={
            'msg_version': 'v1',
        },
        callback=delivery_report,
    )
    P.poll(0.5)
