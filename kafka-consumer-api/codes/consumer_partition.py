from time import sleep
from pprint import pprint

from msgpack import unpackb
from confluent_kafka import Consumer, TopicPartition

from essentials import get_kafka_ins, get_topic
from essentials import decode_dtm, delivery_report


def get_msg(m):
    return unpackb(
        m.value(),
        object_hook=decode_dtm,
        raw=False,
    )


cfg = {
    'bootstrap.servers': get_kafka_ins(),
    'group.id': f'{get_topic()}-1x',
    'auto.offset.reset': 'earliest',
}

marker = 5
cycle_number = 1
while True:
    cycle_number += 1
    print(f'#{cycle_number} - Started')
    C = Consumer(cfg)
    parts = [TopicPartition('topic69', partition=1, offset=marker - 1)]
    C.commit(offsets=parts, async=False)

    C = Consumer(cfg)
    C.subscribe([get_topic()])

    for _ in range(1000):
        msg = C.poll(0.05)
        if msg:
            pprint(dir(msg))
            dat = get_msg(msg)
            if msg.partition() == 1:
                marker = msg.offset()
            pprint(
                {
                    'msg_value': dat,
                    'partition': msg.partition(),
                    'headers': msg.headers(),
                    'key': msg.key(),
                    'offset': msg.offset(),
                }
            )
    C.close()
    sleep(5)
