import asyncio
import os

import nats

SERVERS = os.environ.get("NATS_URL", "nats://localhost:4222")
STREAM = "testing"
SUBJECT = "testing.evm.block_number"


async def main():
    nc = await nats.connect(servers=SERVERS)
    js = nc.jetstream()
    await js.add_stream(name=STREAM, subjects=[SUBJECT])

    await nc.close()


if __name__ == "__main__":
    asyncio.run(main())
