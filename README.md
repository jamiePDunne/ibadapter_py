---

# Interactive Brokers Kafka Integration

This project demonstrates integration with Interactive Brokers (IB) using Kafka for messaging. Below are the essential files and their purposes:

## Usage

1. **Prerequisites:**
   - Kafka installed and running locally.
   - Interactive Brokers (IB) API Gateway or TWS running locally.

2. **Files to Run:**

   - **send_kafka_message.py:** Sends market orders to IB via Kafka.
   - **inspecotr_ib_order_requests.py:** Monitors and sends order requests to IB.
   - **inspecotr_ib_order_responses.py:** Listens for and displays order responses from IB.
   - **config/kafka_config.py:** Configuration file for Kafka broker and topics.

3. **Instructions:**

   - **Triggering Market Orders:**
     - Execute `send_kafka_message.py` to send market orders to IB.

   - **Viewing Order Requests:**
     - Run `inspecotr_ib_order_requests.py` to monitor order requests sent to IB.

   - **Viewing Order Responses:**
     - Run `inspecotr_ib_order_responses.py` to view responses received from IB.

4. **Expected Outcome:**
   - **Triggering Market Orders:** Expect messages indicating successful submission of market orders to IB.
   - **Viewing Order Requests:** Expect to see details of orders sent to IB for execution.
   - **Viewing Order Responses:** Expect updates and notifications on order status changes (e.g., filled orders) from IB.

5. **Installation:**
   - Install dependencies using pip:
     ```
     pip install -r requirements.txt
     ```

6. **Notes:**
   - Ensure IB API Gateway or TWS is active locally.
   - Customize message content in `send_kafka_message.py` if needed.
   - Adjust Kafka configurations in `config/kafka_config.py` according to your setup.

---
