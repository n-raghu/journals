# KAFKA - PRODUCER API WITH THIRD PARTY TOOLS

<p>
This is a continuation to the previous post - , where I covered some peculiar usecases of Consumer API.
Here, I would like to play with Producer API to create message using third party tools like MessagePack for serialization and KafDrop for monitoring
</p>

### Lets get started...

### MessagePack
MessagePack is one of best available schemaless IDL which 

 - Skip compression to save time
 - Can use encryption AES-256 for messages in-transit

### KafDrop
<p>
Kafdrop is an opensource web UI for viewing Kafka topics and browsing consumer groups. The tool displays information such as brokers, topics, partitions, consumers, and lets you view messages.
Check more about KafDrop https://github.com/obsidiandynamics/kafdrop
</p>

### Why should I serialize the messages?
Serialization is the process of transforming an object into a format that it can stored, at the destination you can deserialize the data to recreate the original object. Since Kafka uses filesystem to store the messages, we have to serialize and deserialize the data.
If you're having a standard and rigid database schema, if might want to use Apache Avro which is a best fit widely used in combination with Apache Kafka. In contrast, if you're working with schemaless or bigdata oriented systems, there is an overhead of maintaining the Avro schemas, where schemaless IDL comes into picture. Few schemaless IDL libraries available 
 - JSON
 - UJSON
 - MessagePack
 - Marshal
 - Pickle
 