from time import sleep
from pprint import pprint

from msgpack import unpackb
from confluent_kafka import Consumer

from essentials import get_kafka_ins, get_topic
from essentials import delivery_report, decode_dtm


cfg = {
    'bootstrap.servers': get_kafka_ins(),
    'group.id': f'{get_topic()}-1x',
    'auto.offset.reset': 'earliest',
}

C = Consumer(cfg)
C.subscribe([get_topic()])

no_msg_counter = 0
while True:
    msg = C.poll(0.05)
    if msg:
        no_msg_counter = 0
        pprint(
            {
                'msg_value': unpackb(
                    msg.value(),
                    object_hook=decode_dtm,
                    raw=False,
                ),
                'partition': msg.partition(),
                'headers': msg.headers(),
            },
        )
    elif no_msg_counter > 1000:
        break
    else:
        no_msg_counter += 1
C.close()
