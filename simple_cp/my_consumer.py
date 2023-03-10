from confluent_kafka import Consumer
from for_poc.commonValues import BootstrapServers, TopicName, ConsumerGroupName

CONSUMER_CONFIGS = {
    'bootstrap.servers': BootstrapServers,
    'group.id': ConsumerGroupName,
    'auto.offset.reset': 'earliest',
}

c = Consumer(CONSUMER_CONFIGS)

c.subscribe([TopicName])

while True:
    msg = c.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        print("Consumer error: {}".format(msg.error()))
        continue

    print('Received message: {}'.format(msg.value().decode('utf-8')))

c.close()

