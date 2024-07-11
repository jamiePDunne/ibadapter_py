#
---

# Interactive Brokers Kafka Integration

This project demonstrates integration with Interactive Brokers (IB) using Kafka for messaging. Below are the essential files and their purposes:

## Usage

1. **Prerequisites:**
   - Kafka installed and running locally.
   - Interactive Brokers (IB) API Gateway or TWS running locally.

2. **Files to Run:**

   - **send_kafka_message.py:** generates an order trigger message.
   - **order_gen.py:** submits an order to ib API when  a trigger message is received via Kafka.
   - **inspecotr_ib_order_requests.py:** Monitors and sends order requests to IB.
   - **inspecotr_ib_order_responses.py:** Listens for and displays order responses from IB.
   - **config/kafka_config.py:** Configuration file for Kafka broker and topics.

3. **Expected Outcome:**
   - **Triggering Market Orders:** Expect messages indicating successful submission of market orders to IB.
   - **Viewing Order Requests:** Expect to see details of orders sent to IB for execution.
   - **Viewing Order Responses:** Expect updates and notifications on order status changes (e.g., filled orders) from IB.

4**Installation:**
   - Install dependencies using pip:
     ```
     pip install -r requirements.txt
     ```
---
