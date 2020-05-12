from time import sleep
from pprint import pprint

from confluent_kafka import Consumer, TopicPartition

from essentials import get_kafka_ins, get_topic
from essentials import delivery_report


cfg = {
    'bootstrap.servers': get_kafka_ins(),
    'group.id': f'{get_topic()}-1x',
    'auto.offset.reset': 'earliest',
}

C = Consumer(cfg)
partition_topic_offsets = [
    TopicPartition('kafka-topic-1', partition=1, offset=5),
    TopicPartition('kafka-topic-2', partition=3, offset=0),
    ]
C.commit(offsets=partition_topic_offsets, async=False)
C.close()

C = Consumer(cfg)
C.subscribe(['kafka-topic-1', 'kafka-topic-2', ])

no_msg_counter = 0
while True:
    msg = C.poll(0.05)
    if msg:
        no_msg_counter = 0
        print(
            {
                'msg_value': msg.value(),
                'partition': msg.partition(),
                'headers': msg.headers(),
                'key': msg.key(),
                'offset': msg.offset(),
            }
        )
    elif no_msg_counter > 10000:
        break
    else:
        no_msg_counter += 1
C.close()
