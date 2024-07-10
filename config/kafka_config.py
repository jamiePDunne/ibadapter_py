# config/kafka_config.py

KAFKA_BROKER_URL = 'localhost:9092'
KAFKA_TOPICS = {

    'ib_order_requests_dev': 'ib_order_requests_dev_topic',  # OrderManager sends to IBOrderHandler
    'ib_order_responses_dev': 'ib_order_responses_dev_topic',  # IBOrderHandler sends back to OrderManager
}

# Function to get Kafka configuration
def get_kafka_config():
    return {
        'broker_url': KAFKA_BROKER_URL,
        'topics': KAFKA_TOPICS
    }
