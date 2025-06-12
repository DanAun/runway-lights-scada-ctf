import pymodbus.exceptions
from pymodbus.client import ModbusTcpClient
import time
from ics.constants import ICS_SERVER_PORT

REQUEST_FREQUENCY = 10  # Frequency of requests in seconds
RETRY_DELAY = 10  # Delay in seconds before retrying connection

def loop_modbus_request():
    # Create a Modbus TCP client
    client = ModbusTcpClient('localhost', port=ICS_SERVER_PORT)
    
    while True:
        # Small delay to prevent overwhelming the server
        time.sleep(REQUEST_FREQUENCY)
        try:
            # Connect to the server
            client.connect()
            
            # Write 0 (OFF) to coil at address 0
            client.write_coil(0, False)
        
        except pymodbus.exceptions.ConnectionException as e:
            print(f"Connection error: {e}")
            print("Retrying in %d seconds..." % RETRY_DELAY)
            time.sleep(RETRY_DELAY)
        except KeyboardInterrupt:
            print("Script stopped by user")
            exit(0)
        finally:
            client.close()

if __name__ == "__main__":
    loop_modbus_request()