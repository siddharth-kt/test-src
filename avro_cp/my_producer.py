import os
from io import BytesIO
from uuid import uuid4

from avro import schema
from avro.io import DatumWriter, BinaryEncoder
from confluent_kafka import Producer
from confluent_kafka.serialization import StringSerializer
from for_poc.commonValues import BootstrapServers, AVRO_TopicName

PRODUCER_CONFIGS = {
    "bootstrap.servers": BootstrapServers,
}

p = Producer(PRODUCER_CONFIGS)

schema_file_name = "user.avsc"
path = os.path.realpath(os.path.dirname(__file__))  # returns the current dir path.
with open(f"{path}/avro/{schema_file_name}") as f:
    schema_str = f.read()

string_serializer = StringSerializer('utf_8')

parsed_schema = schema.parse(schema_str)
writer = DatumWriter(parsed_schema)


def encode_dict(user_dict):
    bytes_writer = BytesIO()
    encoder = BinaryEncoder(bytes_writer)
    writer.write(user_dict, encoder)
    raw_bytes = bytes_writer.getvalue()
    return raw_bytes


print("Enter 0 in name field to exit.")
while True:
    p.poll(0)

    try:
        name = input("Enter name : ")
        if name == "0":
            break
        age = int(input("Enter age : "))

        user = dict(name=name, age=age)
        p.produce(topic=AVRO_TopicName,
                  key=string_serializer(str(uuid4())),
                  value=encode_dict(user))
        print("---")
    except KeyboardInterrupt:
        break
    except ValueError:
        print("Invalid input, record discarded!!!")
        continue

# Wait for any outstanding messages to be delivered and delivery report callbacks to be triggered.
p.flush()
