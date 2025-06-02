from pymodbus.client import ModbusTcpClient
import time

def send_modbus_request():
    # Create a Modbus TCP client
    client = ModbusTcpClient('localhost', port=5020)
    
    try:
        while True:
            # Connect to the server
            client.connect()
            
            # Write 0 (OFF) to coil at address 0
            client.write_coil(0, False)
            
            # Small delay to prevent overwhelming the server
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("Script stopped by user")
    finally:
        client.close()

if __name__ == "__main__":
    send_modbus_request()