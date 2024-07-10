# src/message_gen/send_kafka_message.py


import asyncio
import json
from aiokafka import AIOKafkaProducer
from config.kafka_config import get_kafka_config

async def send_message(topic, message):
    try:
        kafka_config = get_kafka_config()
        broker_url = kafka_config['broker_url']

        producer = AIOKafkaProducer(
            bootstrap_servers=broker_url,
            loop=asyncio.get_running_loop(),
            value_serializer=lambda m: json.dumps(m).encode('utf-8')  # Serialize as JSON
        )
        await producer.start()

        # Send a message
        await producer.send_and_wait(topic, message)
        print(f"Message '{message}' sent to '{topic}'")

    except Exception as e:
        print(f"Error sending message to Kafka: {e}")
    finally:
        await producer.stop()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    kafka_config = get_kafka_config()
    topic = kafka_config['topics']['ib_order_requests_dev']
    message = {
        'trigger': 'buy'
        # Add more fields as needed
    }

    loop.run_until_complete(send_message(topic, message))
