from confluent_kafka import Producer
from for_poc.commonValues import BootstrapServers, TopicName

PRODUCER_CONFIGS = {
    "bootstrap.servers": BootstrapServers,
}

p = Producer(PRODUCER_CONFIGS)

print("Enter 0 to exit.")
while True:
    p.poll(0)

    try:
        value = input("Enter value : ")
        if value == "0":
            break

        p.produce(TopicName, value.encode('utf-8'))
        print("---")
    except KeyboardInterrupt:
        break
    except ValueError:
        print("Invalid input, record discarded!!!")
        continue

# Wait for any outstanding messages to be delivered and delivery report callbacks to be triggered.
p.flush()
