import asyncio
import os

import nats

from onchain.models.blockchains.evm_pb2 import BlockNumber

SERVERS = os.environ.get("NATS_URL", "nats://localhost:4222")
STREAM = "blockchain"
SUBJECT = "blockchain.evm.block_number"


async def main():
    nc = await nats.connect(servers=SERVERS)
    js = nc.jetstream()

    data = BlockNumber(id=1234567890)

    ack = await js.publish(SUBJECT, data.SerializeToString())
    print(f"Ack: stream={ack.stream}, sequence={ack.seq}")
    # Ack: stream=hello, sequence=1
    await nc.close()


if __name__ == "__main__":
    asyncio.run(main())
