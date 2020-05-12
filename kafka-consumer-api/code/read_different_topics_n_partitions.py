from confluent_kafka import Consumer, TopicPartition

cfg = {
    'bootstrap.servers': '172.16.18.187:9092',
    'group.id': 'hb-events-1',
    'auto.offset.reset': 'earliest',
}

C = Consumer(cfg)
C.assign(
    [
        TopicPartition(topic='kafka-topic-1', partition=1, offset=6),
        TopicPartition(topic='kafka-topic-2', partition=3, offset=5),
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
