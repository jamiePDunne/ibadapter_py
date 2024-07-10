# example

from ib_insync import *
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def place_ib_order():
    try:
        # Connect to the IB Gateway or TWS
        ib = IB()
        ib.connect('127.0.0.1', 4002, clientId=2)

        # Define the contract details
        contract = Contract()
        contract.symbol = 'DAX'
        contract.secType = 'FUT'
        contract.exchange = 'EUREX'
        contract.currency = 'EUR'
        contract.conId = 673277361  # Replace with the conId for the instrument

        # Send an order
        order = MarketOrder('SELL', 12)
        trade = ib.placeOrder(contract, order)

        # Log the message sent to IB
        log_message = f"Order sent to IB API: {order}"
        logging.info(log_message)

        # Print order status
        logging.info(f"Order status: {trade.orderStatus.status}")

        # Keep the connection open to receive real-time data
        ib.run()

    except Exception as e:
        logging.error(f"Error placing order: {e}")

# Call the function to place the order
if __name__ == "__main__":
    place_ib_order()
