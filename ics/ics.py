import logging

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,  # Set the logging level
    format='%(asctime)s - [ICS] - %(levelname)s: %(message)s',  # Custom format
    datefmt='%H:%M:%S'  # Display only hour, minute, and second
)
log = logging.getLogger("ICS")  # Create a custom logger
log_modbus = logging.getLogger("pymodbus")
log_modbus.setLevel(logging.WARN)

from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.device import ModbusDeviceIdentification
from threading import Thread
import time

from govee.govee_control import light_up_segments, reset_strip, activate_team_light



# --- Constants ---
ICS_SERVER_PORT = 5020  # Use 502 in production so wireshark autodetects protocol
COIL_RUNWAY_LIGHT = 0   # Coil address 0 represents the only runway light
SOLVE_DELAY = 3 # Number of seconds light needs to be on before considering the challenge solved

# --- Modbus Data Store ---
store = ModbusSlaveContext(
    di=None,
    co={COIL_RUNWAY_LIGHT: False},  # Initial state OFF
    hr=None,
    ir=None
)
context = ModbusServerContext(slaves=store, single=True)

def is_challenge_solved():
    """
    Checks if the challenge has been solved. I.E. the state of runway stays on for x seconds.
    """
    start_time = time.time()
    while True:
        is_current_state_on = context[0].getValues(1, COIL_RUNWAY_LIGHT, count=1)[0]
        if not is_current_state_on:
            return False
        # Check if the elapsed time has reached SOLVE_DELAY
        elapsed_time = time.time() - start_time
        if elapsed_time >= SOLVE_DELAY:
            break  # Exit the loop if the delay has passed
    return True

# --- Monitor Thread ---
def monitor_and_control():
    previous_state = context[0].getValues(1, COIL_RUNWAY_LIGHT, count=1)[0]
    reset_strip(1)
    while True:
        current_state = context[0].getValues(1, COIL_RUNWAY_LIGHT, count=1)[0]
        if current_state != previous_state:
            log.info(f"[ICS EVENT] Runway light changed to {'ON' if current_state else 'OFF'}")
            if is_challenge_solved():
                activate_team_light(11)
            previous_state = current_state
        time.sleep(0.5)

# --- Device Identity (for visibility in tools like Wireshark) ---
identity = ModbusDeviceIdentification()
identity.VendorName = "Euromaximus"
identity.ProductCode = "SCADA"
identity.ProductName = "EuroBay International Airport - Runwaylight System"
identity.ModelName = "RunwayICS v3"
identity.MajorMinorRevision = "3.0"

# --- Start the Server ---
def start_ics_server():
    Thread(target=monitor_and_control, daemon=True).start()
    log.info("ICS Modbus TCP Server is starting on port %d..." % ICS_SERVER_PORT)
    StartTcpServer(context, identity=identity, address=("0.0.0.0", ICS_SERVER_PORT))

if __name__ == "__main__":
    start_ics_server()
