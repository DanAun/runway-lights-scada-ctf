from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.device import ModbusDeviceIdentification
import logging
from threading import Thread
import time

from govee_control import light_up_segment, reset_lights

# --- Constants ---
ICS_SERVER_PORT = 5020  # Port 502 requires root, so we use 5020 unless privileged access is okay
COIL_RUNWAY_LIGHT = 0   # Coil address 0 represents the only runway light

# --- Logging Setup ---
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

# --- Modbus Data Store ---
store = ModbusSlaveContext(
    di=None,
    co={COIL_RUNWAY_LIGHT: False},  # Initial state OFF
    hr=None,
    ir=None
)
context = ModbusServerContext(slaves=store, single=True)

# --- API Simulation ---
def send_api_call(runway_state: bool):
    """
    Simulates sending the new state of the runway light to an external API.
    """
    log.info(f"[API CALL] Runway light is now {'ON' if runway_state else 'OFF'}")
    light_up_segment(4)
    return True

# --- Monitor Thread ---
def monitor_and_control():
    previous_state = None
    reset_lights()
    while True:
        current_state = context[0].getValues(1, COIL_RUNWAY_LIGHT, count=1)[0]
        if current_state != previous_state:
            if current_state:
                log.info(f"[ICS EVENT] Runway light changed to {'ON' if current_state else 'OFF'}")
                send_api_call(current_state)
            previous_state = current_state
        time.sleep(0.5)

# --- Device Identity (for visibility in tools like Wireshark) ---
identity = ModbusDeviceIdentification()
identity.VendorName = "SimulatedICS"
identity.ProductCode = "SCADA"
identity.VendorUrl = "http://example.com"
identity.ProductName = "Runway Light ICS"
identity.ModelName = "RunwayICS v3"
identity.MajorMinorRevision = "3.0"

# --- Start the Server ---
def start_ics_server():
    Thread(target=monitor_and_control, daemon=True).start()
    log.info("ICS Modbus TCP Server is starting on port %d..." % ICS_SERVER_PORT)
    StartTcpServer(context, identity=identity, address=("0.0.0.0", ICS_SERVER_PORT))

if __name__ == "__main__":
    start_ics_server()
