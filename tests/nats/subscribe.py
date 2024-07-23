import asyncio
import os

import nats
from nats.errors import TimeoutError

# Get the list of servers.
TIMEOUT = 1
SERVERS = os.environ.get("NATS_URL", "nats://localhost:4222")
STREAM = "blockchain"
SUBJECT = "blockchain.evm.block_number"
CONSUMERE = "blockchain"


async def test_pull_sub(js):
    n = 3
    for _ in range(n):
        await js.publish(SUBJECT, b"testing 123")

    sub = await js.pull_subscribe(SUBJECT, stream=STREAM)

    msgs = await sub.fetch(n)
    for msg in msgs:
        print(msg)
        msg.ack()


async def test_sub(js):
    async def message_handler(msg):
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()
        print(f"Received a message on '{subject} {reply}': {data}")

    sub = await js.subscribe(SUBJECT, stream=STREAM, cb=message_handler)

    while True:
        try:
            msg = await sub.next_msg()
            await msg.ack()
        except TimeoutError:
            break


async def test_ack(js):
    await js.publish(SUBJECT, b"testing 123")
    sub = await js.subscribe(SUBJECT, stream=STREAM, manual_ack=True)
    while True:
        try:
            msg = await sub.next_msg()
            print(msg.data.decode())
            # await msg.ack()
            await msg.ack_sync()
        except TimeoutError:
            break


async def main():
    nc = await nats.connect(servers=SERVERS)
    js = nc.jetstream()

    # await test_sub(js)
    # await test_pull_sub(js)
    await test_ack(js)

    await nc.close()


if __name__ == "__main__":
    asyncio.run(main())
