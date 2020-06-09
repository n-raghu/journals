# KAFKA - PRODUCER API WITH THIRD PARTY TOOLS

This is continuation to the previous post - [Kafka - Playying with Consumer API](https://dev.to/nraghu/kafka-playing-with-consumer-api-using-python-library-3b50), where I covered some peculiar usecases of Consumer API.
Here, I would like to play with Producer API to create message using third party tools like MessagePack for serialization and KafDrop for monitoring

### [MessagePack](https://msgpack.org/index.html)
MessagePack is one of the best available schemaless IDL to 

#### Code Snippets
Example shows how to pack and unpack the common data types, to work with custom data types like datetime.datetime, check DateTime example

 - Simple Example
```python
from msgpack import packb, unpackb

data = {'a': 5}
msg_packet = packb(data)

recreated_data = unpackb(msg_packet)
```

 - Using Datetime
```python
from datetime import datetime as dtm
from dateutil import parser

def dtm_encode(obj):
    if isinstance(obj, dtm):
        return {
            '__dtm__': True,
            'obj_as_str': obj.isoformat()
        }
    return obj

def dtm_decode(obj):
    if '__dtm__' in obj:
        return parser.isoparse(obj['obj_as_str'])
    return obj

dat = {'a':5, 'dates': {'created_at': dtm.now()}}
serialized_dat = packb(dat, default=dtm_encode)
deserialzed_dat = unpackb(serialized_dat, object_hook=dtm_decode)
```

#### Why serialize the messages?
Serialization is the process of transforming an object into a format that it can be stored, at the destination the data can be deserialized to recreate the original object. Since Kafka uses filesystem to store the messages, we have to serialize and deserialize the data

#### Schema-based and Schemaless IDL
In Schema-based IDL, the primitives of the message are pre-defined where publishers and consumers can validate the message before working on it. By the name schemaless, it can have custom primitives for each and every message.
If you're having a standard and rigid database schema, you might want to use Apache Avro which is a best fit and widely used in combination with Apache Kafka. In contrast, if you're working with schemaless or bigdata oriented systems where primitives are highly volatile, there is an overhead of maintaining the Avro schemas, where schemaless IDL comes into picture. Few schemaless IDL libraries available.
 - [JSON](www.json.org)
 - [UJSON](https://github.com/ultrajson/ultrajson)
 - [MessagePack](https://msgpack.org/index.html)
 - [BSON](http://bsonspec.org/)
 - [Pickle](https://docs.python.org/3.6/library/pickle.html)

I chose MessagePack among the list because it has an incredible performance and is super simple to setup and start working with and also much smalller and faster than simple JSON.


### [KafDrop](https://github.com/obsidiandynamics/kafdrop)
<p>
Kafdrop is an opensource web UI for viewing Kafka topics and browsing consumer groups. The tool displays information such as brokers, topics, partitions, consumers, and lets you view messages.
</p>

#### Example screen how a KafDrop looks like

### Produce a Message and see in Kafdrop
```python
from datetime import datetime as dtm

from msgpack import packb, unpackb
from confluent_kafka import Producer

'''
Note: Import or recreate "dtm_encode" function from the Code Snippet section 
'''


def delivery_report(err, m):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {m.topic()} [{m.partition()}]')


producer_config = {
    'bootstrap.servers': '172.16.6.9'
}
producer_topic = 'raghu-producer-test'
P = Producer(producer_config)
data = {
    'a':5,
    'created_at': dtm.now()
}
data_packet = packb(data, default=dtm_encode, use_bin_type=True)

P.produce(
    producer_topic,
    value=data_packet,
    callback=delivery_report,
)
P.poll(0.01)
```

#### Snapshot of Kafdrop

### Best Practices
 - Skip compression to save time
 - Can use encryption AES-256 for messages in-transit
 - Headers
