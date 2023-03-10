from confluent_kafka.admin import AdminClient, NewTopic
from for_poc.commonValues import BootstrapServers, TopicName

ADMIN_CONFIGS = {
    "bootstrap.servers": BootstrapServers
}

admin_client = AdminClient(ADMIN_CONFIGS)
# Our broker is running on localhost:9092

topic_list = [NewTopic(TopicName, num_partitions=1, replication_factor=1)]
fs = admin_client.create_topics(topic_list)

# Wait for each operation to finish.
for topic, f in fs.items():
    try:
        f.result()  # The result itself is None
        print("Topic {} created".format(topic))
    except Exception as e:
        print("Failed to create topic {}: {}".format(topic, e))
