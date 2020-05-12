# Apache Kafka - Playing with Consumer API using Python library

###### _Prerequisite_: Requires prior knowledge(beginner to moderate level) on Kafka ecosystem.

<p>
Kafka has become one of the most widely used Message Broker for Event Bus architecture and Data Streams. We have been using Apache Kafka as a Message Broker for Microservices with CQRS design to build the services on different frameworks.
</p>

<p>
There are numerous articles available online which help developers to reuse the code snippets, however, it is mostly on Scala or Java.
With this write-up, I would like to share some of the reusable code snippets for Kafka Consumer API using Python library confluent_kafka.
confluent_kafka provides a good documentation explaining the funtionalities of all the API they support with the library. Their GitHub page also has adequate example codes.
</p>

Here, I would like to emphasize on two usecases which are rare but would definitely be used, at least a couple of times while working with message brokers.

 - Rewind Topic(Partition) offsets
 - Read from multiple partitions of different topics

### Producer API
<p>Firstly, lets get started with a sample code to produce a message.
</p>

```python
import pickle
from confluent_kafka import Producer

my_dat = 'data that needs to be send to consumer'
P.produce(
    'my_topic',
    pickle.dumps(my_dat),
    callback=delivery_report,
)
```
*pickle* is used to serialize the data, this is not necessary if you working with integers and string, however, when working with timestamps and complex objects, we have to serialize the data.
_Note_: The best practise is to use Apache Avro, which is highly used in combination with Kafka.

#### Create a consumer and consume data
<p>Initialize a consumer, subscribe to topics, poll consumer until data found and consume.</p>

```python
from confluent_kafka import Consumer

cfg = {
    'bootstrap.servers': '<kafka_host_ip>',
    'group.id': '<consumer_group_id>',
    'auto.offset.reset': 'earliest',
}
C = Consumer(cfg)
C.subscribe(['kafka-topic-1', 'kafka-topic-2', ])

for _ in range(10):
    msg = C.poll(0.05)
    if msg:
        dat = {
            'msg_value': msg.value(), # This is the actual content of the message
            'msg_headers': msg.headers(), # Headers of the message
            'msg_key': msg.key(), # Message Key
            'msg_partition': msg.partition(), # Partition id from which the message was extracted
            'msg_topic': msg.topic(), # Topic in which Producer posted the message to          
        }
        print(dat)
```

By default, consumer instances poll all the partitions of a topic, there is no need to poll each partition of topic to get the messages.
_msg_ has a _None_ value if _poll_ method has no messages to return. Boolean check will help us to understand whether the *poll* to broker fetched message or not.
Valid message has not only data, it also has other functions which helps us to query or control the data.

#### Read from multiple partitions of different topics
Scenario:
 - Read from partition 1 of topic 1 starting with offset value 6
 - Read from partition 3 of topic 2 starting with offset value 5
 - Read from partition 2 of topic 1 starting with offset value 9

```python
from confluent_kafka import Consumer, TopicPartition
cfg = {
    'bootstrap.servers': '172.16.18.187:9092',
    'group.id': 'hb-events-1',
    'auto.offset.reset': 'earliest',
}

C = Consumer(cfg)
C.assign(
    [
        TopicPartition(topic='kafka-topic-1', partition=1, offset=36),
        TopicPartition(topic='kafka-topic-2', partition=3, offset=35),
        TopicPartition(topic='kafka-topic-1', partition=2, offset=39),
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
```
When reading from a specific partition of a topic, assign is the best method to use instead of subscribe.
*assign* method accepts a list of TopicPartitions. *TopicPartition* is an instance which gets enrolled with one specific partition of a topic.

#### Rewind Topic(partition) offsets
Scenario:
 - Rewind the Partition 1 of topic-1 to offset 5
 - Reset the Partition 3 of topic-2

```python
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
```

_Irrespective of the current offset for the partition, we can rewind or reset the offset._
**Reset or rewind offset values are set for a specific consumer groupid which was used to commit the offset, offsets of other consumer groups are unaffected**

**How we achieved this?**
 - Create a list of TopicPartitions with the respective offset to reset
 - Commit these offsets to broker
 - When consumer subscribed to these topics poll, they get data from the recently set offset

**Only retained messages are retrieved**
 - Only message within the retention period are retrieved when you reset or rewind the offset.
 - If you lose or do not have a record of last successful offset, use **OFFSET_BEGINNING**, this will fetch data from the current beginning of the partition.

**Use REST API**
 - If you're frequently running out of issues and want to rewind, it is advised to *periodically* record/fetch the last successful offset to a table which look similar to events.
 - How frequent should we record?, depends on the business case. Recording every offset involves DB call which may slow down the service.
 - Create a wrapper REST-API which can update the table values.
 - Modify consumer groups to get last offset from table.
