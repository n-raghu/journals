import sys
from datetime import datetime as dtm

from msgpack import packb
from bson.objectid import ObjectId as bson_id
from confluent_kafka import Producer, TopicPartition

from essentials import get_kafka_ins, get_topic
from essentials import encode_dtm, delivery_report


def gen_msg():
    return {
        'bsond': str(bson_id()),
        'timestamp': dtm.now(),
        'msg_topic': get_topic(),
    }


producer_cfg = {
    'bootstrap.servers': get_kafka_ins(),
}

P = Producer(producer_cfg)


for _ in range(5):
    P.produce(
        get_topic(),
        value=packb(
            gen_msg(),
            default=encode_dtm,
            use_bin_type=True,
        ),
        key=str(bson_id()),
        headers={
            'a': 'yes',
            'b': 'no',
        },
        callback=delivery_report,
    )
    P.poll(0.5)
