#!/usr/bin/env python

import sys
from configparser import ConfigParser

from confluent_kafka import Consumer

CONFIG_FILE = "./tests/kafka/config.ini"
TOPIC = "blockchain.ethereum.blocknumber"

if __name__ == "__main__":
    # Parse the configuration.
    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    config_parser = ConfigParser()
    config_parser.read(CONFIG_FILE)
    config = dict(config_parser["default"])
    config.update(config_parser["consumer"])

    # Create Consumer instance
    consumer = Consumer(config)

    # Subscribe to topic
    consumer.subscribe([TOPIC])

    # Poll for new messages from Kafka and print them.
    try:
        while True:
            msg = consumer.poll(1)
            if msg is None:
                # Initial message consumption may take up to
                # `session.timeout.ms` for the consumer group to
                # rebalance and start consuming
                print("Waiting...")
            elif msg.error():
                print(f"ERROR: {msg.error()}")
            else:
                # Extract the (optional) key and value, and print.

                print(msg.value().decode())

                # print(
                #     "Consumed event from topic {topic}: key = {key:12} value = {value:12}".format(
                #         topic=msg.topic(),
                #         key=msg.key().decode("utf-8"),
                #         value=msg.value().decode("utf-8"),
                #     )
                # )
    except KeyboardInterrupt:
        pass
    finally:
        # Leave group and commit final offsets
        consumer.close()
