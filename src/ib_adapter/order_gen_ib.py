from ib_insync import *
import json
import logging
import asyncio
import nest_asyncio
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from config.kafka_config import get_kafka_config

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()

# Set up logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

# Define a file handler
file_handler = logging.FileHandler('ib_kafka_integration.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s'))
logging.getLogger().addHandler(file_handler)

# Get Kafka configuration
kafka_config = get_kafka_config()

# Establish IB connection
ib = IB()


async def publish_to_kafka(message):
    try:
        logging.info("Initializing Kafka producer...")
        producer = AIOKafkaProducer(
            bootstrap_servers=kafka_config['broker_url'],
            value_serializer=lambda m: json.dumps(m).encode('utf-8')
        )
        await producer.start()
        logging.info("Kafka producer started.")
        logging.info(f"Publishing message to Kafka topic {kafka_config['topics']['ib_order_responses_dev']}: {message}")
        await producer.send_and_wait(kafka_config['topics']['ib_order_responses_dev'], message)
        logging.info("Message published successfully.")
        await producer.stop()
        logging.info("Kafka producer stopped.")
    except Exception as e:
        logging.error(f"Error publishing message to Kafka: {e}")


async def place_ib_order():
    try:
        # Define the contract details
        contract = Contract()
        contract.symbol = 'DAX'
        contract.secType = 'FUT'
        contract.exchange = 'EUREX'
        contract.currency = 'EUR'
        contract.conId = 673277361  # Replace with the conId for the instrument

        # Send an order
        order = MarketOrder('SELL', 16)
        trade = ib.placeOrder(contract, order)

        # Log the message sent to IB
        log_message = f"Order sent to IB API: {order}"
        logging.info(log_message)

        # Print order status
        logging.info(f"Order status: {trade.orderStatus.status}")

        # Construct message for Kafka
        order_response_message = {
            'order_status': trade.orderStatus.status,
            'order_details': str(order)  # Convert order object to string or format as needed
        }

        # Publish order response to Kafka
        await publish_to_kafka(order_response_message)

    except Exception as e:
        logging.error(f"Error placing order: {e}")


async def consume_from_kafka():
    try:
        logging.info("Initializing Kafka consumer...")
        consumer = AIOKafkaConsumer(
            kafka_config['topics']['ib_order_requests_dev'],
            bootstrap_servers=kafka_config['broker_url'],
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            group_id=None  # Ensure each consumer group starts from the beginning
        )

        await consumer.start()
        logging.info("Kafka consumer started.")

        async for message in consumer:
            try:
                logging.info(f"Received trigger message from Kafka: {message.value}")

                # Trigger order placement upon receiving any message
                await place_ib_order()

            except Exception as e:
                logging.error(f"Error processing Kafka message: {e}")

    except Exception as e:
        logging.error(f"Error consuming from Kafka: {e}")
    finally:
        await consumer.stop()
        logging.info("Kafka consumer stopped.")


def orderStatusHandler(trade):
    try:
        logging.info(f"Order status updated: {trade.orderStatus.status}")

        # Construct message for Kafka
        order_response_message = {
            'order_status': trade.orderStatus.status,
            'order_details': str(trade.order)  # Convert order object to string or format as needed
        }

        # Publish order response to Kafka
        asyncio.run(publish_to_kafka(order_response_message))
    except Exception as e:
        logging.error(f"Error handling order status update: {e}")


async def main():
    logging.info("Starting script...")

    try:
        # Connect to IB
        logging.info("Connecting to IB...")
        await ib.connectAsync('127.0.0.1', 4002, clientId=2)
        logging.info("Connected to IB.")

        # Register event handlers
        ib.orderStatusEvent += orderStatusHandler

        # Start Kafka consumer to listen for messages and trigger order placement
        consume_task = asyncio.create_task(consume_from_kafka())

        # Keep the event loop running
        while True:
            ib.sleep(1)  # Sleep for a short interval to keep the loop running
            await asyncio.sleep(0)  # Yield control to asyncio event loop

    except KeyboardInterrupt:
        logging.info("Stopping script...")
    except Exception as e:
        logging.error(f"Error in main: {e}")
    finally:
        # Disconnect from IB after script execution
        ib.disconnect()
        logging.info("Disconnected from IB.")


if __name__ == "__main__":
    asyncio.run(main())
