from confluent_kafka import Consumer, TopicPartition

from essentials import get_topic, get_kafka_ins

cfg = {
    'bootstrap.servers': get_kafka_ins(),
    'group.id': 'jt-consumer-1x',
    'auto.offset.reset': 'earliest',
}
topic1, topic2 = get_topic()

C = Consumer(cfg)
C.assign(
    [
        TopicPartition(topic=topic1, partition=0, offset=6),
        TopicPartition(topic=topic2, partition=0, offset=5),
    ]
)

no_msg_counter = 0
while True:
    msg = C.poll(0)
    if msg:
        no_msg_counter = 0
        dat = {
            'msg_val': msg.value(),
            'msg_partition': msg.partition(),
            'msg_topic': msg.topic()
        }
        print(dat)
    elif no_msg_counter > 10000:
        print('No Messages Found from a long time')
    else:
        no_msg_counter += 1
C.close()
