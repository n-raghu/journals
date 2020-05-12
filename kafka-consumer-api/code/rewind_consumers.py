from time import sleep
from pprint import pprint

from confluent_kafka import Consumer, TopicPartition

from essentials import get_kafka_ins, get_topic
from essentials import delivery_report


cfg = {
    'bootstrap.servers': get_kafka_ins(),
    'group.id': 'jt-consumer-1x',
    'auto.offset.reset': 'earliest',
}

topic1, topic2 = get_topic()
C = Consumer(cfg)
partition_topic_offsets = [
    TopicPartition(topic1, partition=0, offset=5),
    TopicPartition(topic2, partition=0, offset=0),
    ]
C.commit(offsets=partition_topic_offsets, async=False)
C.close()

C = Consumer(cfg)
C.subscribe([topic1, topic2])

no_msg_counter = 0
while True:
    msg = C.poll(0.5)
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
