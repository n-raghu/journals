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
