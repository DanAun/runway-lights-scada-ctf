# ICS Modbus TCP Server to control runway lights

from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
import logging
from threading import Thread
import time

# Configure logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# Create a data store with two coils: RWY_1 (coil 0), RWY_2 (coil 1)
store = ModbusSlaveContext(
    di=None,
    co={0: False, 1: False},
    hr=None,
    ir=None
)
context = ModbusServerContext(slaves=store, single=True)

# Function to monitor and log the LED state

def monitor_leds():
    previous_states = [None, None]
    while True:
        rwy1 = context[0].getValues(1, 0, count=1)[0]
        rwy2 = context[0].getValues(1, 1, count=1)[0]
        if previous_states[0] != rwy1:
            print(f"[LED CONTROL] RWY_1 lights {'ON' if rwy1 else 'OFF'}")
            previous_states[0] = rwy1
        if previous_states[1] != rwy2:
            print(f"[LED CONTROL] RWY_2 lights {'ON' if rwy2 else 'OFF'}")
            previous_states[1] = rwy2
        time.sleep(1)  # Polling interval

# Start monitoring in a separate thread
Thread(target=monitor_leds, daemon=True).start()

# Start the Modbus TCP server
print("Starting ICS Modbus TCP Server on port 502...")
StartTcpServer(context, address=("0.0.0.0", 502))