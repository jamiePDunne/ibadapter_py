# ib_adapter/order_gen_ib.py

from ib_insync import *
import logging
import asyncio
from config.kafka_config import get_kafka_config

# Set up logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

# Get Kafka configuration
kafka_config = get_kafka_config()

# Establish IB connection
ib = IB()
ib.connect('127.0.0.1', 4002, clientId=2)  # Adjust host, port, and clientId as necessary

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
        order = MarketOrder('BUY', 1)
        trade = ib.placeOrder(contract, order)

        # Log the message sent to IB
        log_message = f"Order sent to IB API: {order}"
        logging.info(log_message)

        # Print order status
        logging.info(f"Order status: {trade.orderStatus.status}")

    except Exception as e:
        logging.error(f"Error placing order: {e}")

async def consume_from_kafka():
    try:
        consumer = AIOKafkaConsumer(
            kafka_config['topics']['ib_order_requests_dev'],
            bootstrap_servers=kafka_config['broker_url'],
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            group_id=None  # Ensure each consumer group starts from the beginning
        )

        await consumer.start()

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

async def main():
    logging.info("Starting script...")

    try:
        # Start Kafka consumer to listen for messages and trigger order placement
        await consume_from_kafka()
    except Exception as e:
        logging.error(f"Error in main: {e}")
    finally:
        # Disconnect from IB after script execution
        ib.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
