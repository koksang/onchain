import json
import logging as log
import os

import clickhouse_connect
from confluent_kafka import Producer
from requests import request

NS = "onchain"
SVC = "svc.cluster.local"

CH_HOST = f"clickhouse.{NS}.{SVC}"
CH_USER = CH_PASSWORD = "onchain"
CH_DATABASE = "ethereum"
CH_TABLE = "block"

NODE_API_URL = os.environ["NODE_API_URL"]
TOPIC = "blockchain.evm.blocknumber"
KAFKA_HOST = f"onchain-kafka-bootstrap.{NS}.{SVC}:9092"
CONFIG = {"bootstrap.servers": KAFKA_HOST}


def get_blockchain_latest_block_number(
    api_url: str = NODE_API_URL,
    method: str = "eth_blockNumber",
    headers: dict[str, str] = {"Content-Type": "application/json"},
) -> int:
    payload = json.dumps(
        {
            "method": method,
            "params": [],
            "id": 1,
            "jsonrpc": "2.0",
        }
    )
    response = request(
        "POST",
        api_url,
        headers=headers,
        data=payload,
    )
    block_number = int(response.json()["result"], 16)
    log.info(f"Node latest block number: {block_number}")
    return block_number


def get_ch_latest_block_number(
    ch: clickhouse_connect.driver.Client,
    db: str = CH_DATABASE,
    table: str = CH_TABLE,
) -> int:
    result = ch.query(f"select max(number) from {db}.{table}")
    block_number = int(result.result_rows[0][0])
    log.info(f"CH latest block number: {block_number}")
    return block_number


def generate_block_numbers(node: int, ch: int, limit: int = 1000):
    assert node >= ch, f"Clickhouse {ch} > Node latest block {node}"

    block_start = ch + 1
    block_end = min([node + 1, block_start + limit])
    log.info(f"Generating new block number from block: {block_start} to {block_end}")
    return map(hex, range(block_start, block_end))


if __name__ == "__main__":
    log.info(f"Connecting to {CH_HOST}")
    ch = clickhouse_connect.get_client(
        host=CH_HOST, port=8123, username=CH_USER, password=CH_PASSWORD
    )
    log.info(f"Connected to clickhouse {CH_HOST}")

    log.info(f"Connecting to kafka {KAFKA_HOST}")
    kafka = Producer(CONFIG)
    log.info(f"Connected to kafka {KAFKA_HOST}")

    block_numbers = generate_block_numbers(
        get_blockchain_latest_block_number(), get_ch_latest_block_number(ch=ch)
    )

    for number in block_numbers:
        log.info(f"number: {number}")
        kafka.produce(TOPIC, key="number", value=number)

    kafka.poll(10000)
    kafka.flush()
