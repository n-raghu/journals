We have seen many articles on Kafka, however, this article focuses mainly on Python API, confluent_kafka.
Documentation provides a good explanation and a guide to use the API.

In this article, I would like to cover Apache Kafka with third party message serializers like MesagePack in Python environment.
Let's also see few other usecase in the last.

As you already know that Apache Kafka is one of the mature and leading opensource message broker.
MessagePack: It's like a JSON but much faster and smaller than JSON.

Producer sample code:
from confluent_kafka import Producer
from msgpack import packb, unpackb

my_dat = 'string which needs to be packed'
my_dat_pack = packb(mydat)
P.produce(
    'my_topic',
    my_dat,
    callback=delivery_report,
)

Headers: Confluent team added support for headers from a long time and can be used for multiple purposes. I'm using headers to store trivial information related to messages like version of the message and the service who generated the message.

I have seen few examples, where people using compression algorithms to reduce the packet size. However, I compared using various datatypes where msgpack reduces the data size almost to the level of snappy compression. If you really think compression is mandatory, always use lossless and widely accepted libraries
1. snappy
2. zlib
3. Bzip2

Snappy aims to provide high speeds and reasonable compression. BZ2 trades speed for better compression, and zlib falls somewhere between them.

Consumer sample code:
C = Consumer
C.subscribe([])
C.poll()
C.close()

To rewind messages:


Confluent also provides TopicPartition function which helps 