
from confluent_kafka import Consumer, TopicPartition
from msgpack import unpackb

cfg = {
    'bootstrap.servers': '172.16.18.187:9092',
    'group.id': 'hb-events-1',
    'auto.offset.reset': 'earliest',
}

C = Consumer(cfg)
C.assign(
    [
        TopicPartition(topic='heartbeats', partition=1, offset=0),
        TopicPartition(topic='topic-events'),
    ]
)

for _ in range(1000000):
    msg = C.poll(0)
    if msg and msg.topic() == 'heartbeats':
        break


C.subscribe(['topic-events', 'heartbeats'])

for _ in range(100):
    msg = C.poll(1.0)
    if msg:
        break
