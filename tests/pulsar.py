"""Unit tests
"""

from google.protobuf.descriptor_pb2 import DescriptorProto
from onchain.core.schema import ProtobufBytesSchema
from onchain.models.blockchains.evm_pb2 import Log


if __name__ == "__main__":
    import pulsar

    #
    SERVICE_URL = "pulsar://127.0.0.1:6650"
    TOPIC = "onchain/polygon/testing"
    RANGE = 2
    PROTO_DESCRIPTOR = DescriptorProto()
    Log.DESCRIPTOR.CopyToProto(PROTO_DESCRIPTOR)
    #
    log = Log(
        removed=True,
        logIndex=1,
        transaction_index=1,
        transaction_hash="asdsas",
        block_hash="sadas",
        block_number=1,
        address="sada",
        data="sada",
        topics=["sadas", "sadas"],
    )

    #
    client = pulsar.Client(service_url=SERVICE_URL)
    producer = client.create_producer(
        topic=TOPIC,
        schema=ProtobufBytesSchema(record_cls=Log, schema_definition=PROTO_DESCRIPTOR),
    )

    for i in range(RANGE):
        producer.send(log)
        print(f"Sending - {log}\n")

    #
    consumer = client.subscribe(
        topic=TOPIC,
        subscription_name="testing123",
        schema=ProtobufBytesSchema(record_cls=Log, schema_definition=PROTO_DESCRIPTOR),
    )

    print(" <<<<<<<<<<<<<<<<<<<< CONSUMER >>>>>>>>>>>>>>>>>>>>> \n\n\n")
    for i in range(RANGE):
        msg = consumer.receive()
        print(f"Received - {msg.value()}\n")

    client.close()
