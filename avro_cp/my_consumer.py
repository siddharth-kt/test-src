import os
from io import BytesIO

from avro import schema
from avro.io import DatumReader, BinaryDecoder
from confluent_kafka import Consumer
from for_poc.commonValues import BootstrapServers, AVRO_TopicName, AVRO_ConsumerGroupName

CONSUMER_CONFIGS = {
    'bootstrap.servers': BootstrapServers,
    'group.id': AVRO_ConsumerGroupName,
    'auto.offset.reset': 'earliest',
}

c = Consumer(CONSUMER_CONFIGS)

schema_file_name = "user.avsc"
path = os.path.realpath(os.path.dirname(__file__))  # returns the current dir path.
with open(f"{path}/avro/{schema_file_name}") as f:
    schema_str = f.read()

# Parse the schema using the avro.schema.parse method
parsed_schema = schema.parse(schema_str)

# Create an Avro reader object using the parsed schema
reader = DatumReader(parsed_schema)


def decode_msg(msg_value):
    message_bytes = BytesIO(msg_value)
    decoder = BinaryDecoder(message_bytes)
    event_dict = reader.read(decoder)
    return event_dict


c.subscribe([AVRO_TopicName])

while True:
    msg = c.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        print("Consumer error: {}".format(msg.error()))
        continue

    print('Received message: {}'.format(decode_msg(msg.value())))

c.close()

