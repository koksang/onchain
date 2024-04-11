#!/usr/bin/env python

import json
import sys
from configparser import ConfigParser
from random import choice

from confluent_kafka import Producer

NODE_API_URL = "https://late-compatible-sponge.quiknode.pro/8493db3aae9348e70a783905b9a158dc26023b6b"
CONFIG_FILE = "./tests/kafka/config.ini"
TOPIC = "blockchain.evm.blocknumber"
MESSAGES = [
    dict(
        key="input",
        # value=json.dumps({"block_number": "0xc5043f"}),
        value=json.dumps({"block_number": "0x1e8480"}),  # block_number = 2000000
    ),
] * 2

if __name__ == "__main__":
    # Parse the configuration.
    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    config_parser = ConfigParser()
    config_parser.read(CONFIG_FILE)
    config = dict(config_parser["default"])

    # Create Producer instance
    producer = Producer(config)

    # Optional per-message delivery callback (triggered by poll() or flush())
    # when a message has been successfully delivered or permanently
    # failed delivery (after retries).
    def delivery_callback(err, msg):
        if err:
            print(f"ERROR: Message failed delivery: {err}")
        else:
            print(
                "Produced event to topic {topic}: key = {key:12} value = {value:12}".format(
                    topic=msg.topic(),
                    key=msg.key().decode("utf-8"),
                    value=msg.value().decode("utf-8"),
                )
            )

    count = 0
    for msg in MESSAGES:
        key, value = msg["key"], msg["value"]
        producer.produce(TOPIC, key=key, value=value, callback=delivery_callback)
        count += 1

    # Block until the messages are sent.
    producer.poll(10000)
    producer.flush()
