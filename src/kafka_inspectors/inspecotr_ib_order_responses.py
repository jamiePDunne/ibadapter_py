# src/kafka_inspectors/inspecotr_ib_order_responses.py


import asyncio
from aiokafka import AIOKafkaConsumer
from config.kafka_config import get_kafka_config

async def consume_messages():
    try:
        kafka_config = get_kafka_config()
        kafka_topic = kafka_config['topics']['ib_order_responses_dev']
        kafka_server = kafka_config['broker_url']

        consumer = AIOKafkaConsumer(
            kafka_topic,
            bootstrap_servers=kafka_server,
            group_id="view_only_group",  # Use a unique consumer group ID
            auto_offset_reset='earliest',  # Start consuming from the beginning
        )

        await consumer.start()

        async for msg in consumer:
            print(f"Received message: {msg.value.decode('utf-8')}")

    finally:
        await consumer.stop()

async def main():
    await consume_messages()

if __name__ == "__main__":
    asyncio.run(main())
