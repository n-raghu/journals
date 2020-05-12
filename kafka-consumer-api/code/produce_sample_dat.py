import pickle
from time import sleep
from datetime import datetime as dtm

from confluent_kafka import Producer

from essentials import get_kafka_ins, get_topic, delivery_report

cfg = {
    'bootstrap.servers': get_kafka_ins(),
}

P = Producer(cfg)
msg_number = 1

while True:
    for topic in get_topic():
        P.produce(
            topic=topic,
            value=pickle.dumps(f'Message - {msg_number}, generated at {dtm.utcnow()}'),
            callback=delivery_report,
        )
    P.poll(0.5)
    sleep(180)
