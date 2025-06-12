import logging
import os

# --- Logging Setup ---
logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level
    format='%(asctime)s - [ICS] - %(levelname)s: %(message)s',  # Custom format
    datefmt='%H:%M:%S'  # Display only hour, minute, and second
)
log = logging.getLogger("ICS")  # Create a custom logger
log_modbus = logging.getLogger("pymodbus")
log_modbus.setLevel(logging.WARN)

import bcrypt
from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.device import ModbusDeviceIdentification
from flask import Flask, request, jsonify, session
from threading import Thread
import time
from waitress import serve

import ics.constants
from govee.govee_control import toggle_team_light


# --- Modbus Data Store ---
store = ModbusSlaveContext(
    di=None,
    co={ics.constants.COIL_RUNWAY_LIGHT: False},  # Initial state OFF
    hr=None,
    ir=None
)
context = ModbusServerContext(slaves=store, single=True)

# Flask app for handling API requests
app = Flask(__name__)
app.secret_key = os.urandom(24)

# User data for authentication with hashed passwords
users = {'team1': b'$2b$12$hUHULBpAOCqqGwnBVTskaeJPK7VuxlJYiPWKIWvPLJcmMZY.slF7q', 'team2': b'$2b$12$B/v7cyW75.tcn1g6OmThk.U1ho84phDLwCV6wwlpwjuxyRGCbrtiW', 'team3': b'$2b$12$fMdVg1l9655a6wIC07.6gOXoirAlDSlEKWqCvuo4bzkabHMRB6w8i', 'team4': b'$2b$12$bOl0AG4OAN5/FHDluN988.g/koIJ4mP5rxrGdXKn.Ab5GOVA1MtaS', 'team5': b'$2b$12$cNmf0ZvZUefVOcriiAYJa.Lj3.dXWSIrNBb5GwKEDs8EiBmJcNvoS', 'team6': b'$2b$12$HB5gxqoH3jTXdEKcXsT7huMhy1toZt5J.ArCKI3CRsQsTHXHoCdzu', 'team7': b'$2b$12$AZCN8B9RI9Q4.ao8Wq9aU.ABUgBjcRLxIvTWHViC60mQ71QyEb9gm', 'team8': b'$2b$12$rBk877KbUQ1ToZ/bUYmCAOD31Kw6irzMkMBvSu94dWAxCEJrEdWUy', 'team9': b'$2b$12$ZTEGIJeBRjqqL8GxnX/W4.B.Hg2UawoYXZL4g5Umw.MXtvcHCuqOC', 'team10': b'$2b$12$duAx.XAQQC9gIz7eHz9cxO/Kjy4ecdNpPtUXhz7yeacLmw5y8CVUi', 'team11': b'$2b$12$hH0XBI94VQHs6pbHfQEYROgeGGdL6YUkVbc1MxBKMoDgkx8lnjh.q', 'team12': b'$2b$12$sysnUgIW9X2IfgO3Z9EJT.dWj9q5dBQ3uw8O.tdKethx8aa62/ZsW', 'team13': b'$2b$12$/VStnpCPfoMK16Bl4zY2h.Tj6vD2sPZD6nukXUfAdyGl.HN1wbTZ6', 'team14': b'$2b$12$VH3/srW6sVUID7nHEUXYzObcFtH/DswD1jJB2OLHjmwAlM./UF2pS', 'team15': b'$2b$12$2wIEl8S4.ctW6z5DggvJ/OBn/u0xSwXa7x8LERS4smugP5lLcOqNO', 'team16': b'$2b$12$a4oKSQuF5hI4.t9MZz/VHeDGYa1Cv7WXMdYOOlKFFyjtlptKwX.dS', 'team17': b'$2b$12$1KkI1LS6n792mNyotJ/UuuTXsa0Wbh3uelcTlvtEuLKv5Ytp0dS0i', 'team18': b'$2b$12$OYJPAQw8HcpyB/No87PXv.XnVKkhuyfCvAqLk1/3JNdouo3Fesv.e', 'team19': b'$2b$12$SgYnCcv6qf0PO6O3AnqsHOyLzel99Rv5sN83/cQ8uVLaRyq6InPU2', 'team20': b'$2b$12$rs5zdJmt.QnE33Nz69pe9ORR8fJM5rYHgzsD1AYxzPWyssSi0dCdO', 'team21': b'$2b$12$sfuFAi2AthVIRKo1dk7WTe5KsvtKLrF7rcj0MlO1LxbNFrFO/Uy26', 'team22': b'$2b$12$8kgB.tnTo0M7ZoRdzRbcQOtUl.T3zl5wmnvtqssgO9xX0or6y3m/6', 'team23': b'$2b$12$VOOjVTrIF8TLnWVgcptxb.8pj33paMEYMZ3ns1RdgHtrYH6NxMJOW', 'team24': b'$2b$12$KaBeT7.kWjuGde3fE8qC4efZa.s9oaAfKvnb.cQwE0Gqc2G.OQ3ma', 'team25': b'$2b$12$c2F46gbx/O5xT.pkA6dIbOeQr0EJltG/k7ui97qrn.h/PI7DkaghG', 'team26': b'$2b$12$Lr.BvxY0.KLc.C1inSEivupUs259TYQaK9.DjJthjDCrWkDMYTaSW', 'team27': b'$2b$12$GLMFxNPTvLRr8mS4TIQVM.YYFsyOesSgVZkWtyswHgX2H0we7C6rm', 'team28': b'$2b$12$8SnTsw5h5hVtZCnzk6SIDemlZAkVvQjYDU2iKrgBKyYEfei09q26a', 'team29': b'$2b$12$ogTph.sdkgyWerxeGocxLu/nh20GZxW25M5jz/YRU9vNb8z//i6Dm', 'team30': b'$2b$12$382JyGKxxkc115wRiJJ7y.RnCBq.LdVQXS6nDC35tHTcyYEe.HaWe', 'team31': b'$2b$12$WWkc/l2A8aT0BHbknof1WuOY.1H4YTl0j/WwgW49dg.OPIJxVVHpm', 'team32': b'$2b$12$fXUgJeu74jE9EuBYWvrXoeplGkbc9CoQyTshkE9I/VQsKVq2VMYGS', 'team33': b'$2b$12$DqDaiN8HgsI5lQWKROVTEe/2YV5q1j5Bij4DG7TempXuOog9QrNaW', 'team34': b'$2b$12$f9TbQWn3fG8KhqUbw3GfcePNsmyAYNvgdPlGkfuqwO.WfK8Zd4nam', 'team35': b'$2b$12$K8Ds1JPzNY5KHagAUvjhA.KUt/clpG67bw9QVXB1mDBNUQMTOvl0C', 'team36': b'$2b$12$X6bOQnNd3eUaIe/ro/Z.G.RR1QGGNb4RTL3oy/9AEZs2iTwPJ5HC6', 'team37': b'$2b$12$U4rbpGKibJtXEwzLzQhIdOMu41BMHUb01oTDrmxZrIko0wtpP3j96', 'team38': b'$2b$12$eYhDa076uOWTt2XdLOaykemFC/O2kmRSMX0FGQZExalYfqXRWS3CO', 'team39': b'$2b$12$DYA6IRtz4v3lY0Cppm/3A.oiAhlsJjQotQvpnY6/rLLO/970cwyma', 'team40': b'$2b$12$f68wkp58LuHe1eLddujt5OyTbdY/ulDqkxiuWBcfQw2WOOPozM0ji'}
team_num = None

@app.route('/api/login', methods=['POST'])
def login():
    global team_num
    data = request.json
    username = data.get('username')
    password = data.get('password').encode('utf-8')  # Encode password to bytes

    # Check if the username and password are correct
    if username in users and bcrypt.checkpw(password, users[username]):
        team_num = int(username.replace("team", ""))  # Store team_num
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 403
    
@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('username', None)  # Remove username from session
    return jsonify({'message': 'Logout successful'}), 200

def is_challenge_solved():
    """
    Checks if the challenge has been solved. I.E. the state of runway stays on for x seconds.
    """
    log.debug("Checking if challenge is solved...")
    start_time = time.time()
    while True:
        is_current_state_on = context[0].getValues(1, ics.constants.COIL_RUNWAY_LIGHT, count=1)[0]
        if not is_current_state_on:
            log.debug('Challenge is not solved! Runway Lights turned off - \'malware\' is lickely still running')
            return False
        # Check if the elapsed time has reached SOLVE_DELAY
        elapsed_time = time.time() - start_time
        if elapsed_time >= ics.constants.SOLVE_DELAY:
            break  # Exit the loop if the delay has passed
        time.sleep(ics.constants.CHECK_INTERVAL)
    return True

# --- Monitor Thread ---
def monitor_and_control():
    global team_num
    is_strip_on = False # Whether the physical ligth strip segment is on
    already_solved = False # Whether the CTF challenge was already solved
    already_teased = False # Whether the team has been teased with the lights
    previous_state = context[0].getValues(1, ics.constants.COIL_RUNWAY_LIGHT, count=1)[0]
    while True:
        time.sleep(ics.constants.CHECK_INTERVAL)
        current_state = context[0].getValues(1, ics.constants.COIL_RUNWAY_LIGHT, count=1)[0]
        if current_state != previous_state:
            log.info(f"Runway light changed to {'ON' if current_state else 'OFF'}")
            if team_num is None:
                log.warning("team_num is None, make sure you are authenticated")
                previous_state = current_state
                continue
            if already_solved:
                log.debug("Challenge is already solved, not able to toggle lights anymore")
                previous_state = current_state
                continue
            if current_state: # Toggeled lights on
                if already_teased:
                    # Check if they have solved and challenge and only light up in that case
                    if is_challenge_solved():
                        toggle_team_light(team_num, True)
                        already_solved = True
                        is_strip_on = True
                else:
                    # Tease the players with the light
                    toggle_team_light(team_num, True)
                    is_strip_on = True
                    already_teased = False# True
                    time.sleep(ics.constants.MIN_TEASE_TIME)
            else: # Toggled lights off
                if is_strip_on:
                    toggle_team_light(team_num, False)
                    is_strip_on = False
            previous_state = current_state


# --- Device Identity (for visibility in tools like Wireshark) ---
identity = ModbusDeviceIdentification()
identity.VendorName = "Euromaximus"
identity.ProductCode = "SCADA"
identity.ProductName = "EuroBay International Airport - Runwaylight System"
identity.ModelName = "RunwayICS v3"
identity.MajorMinorRevision = "3.0"

# --- Start the Server ---
def start_ics_server():
    try:
        log.info("ICS Modbus TCP Server is starting on port %d...", ics.constants.ICS_SERVER_PORT)
        Thread(target=StartTcpServer, args=(context,), kwargs={'identity': identity, 'address': ("localhost", ics.constants.ICS_SERVER_PORT)}, daemon=True).start()
    except Exception as e:
        log.critical("Failed to start ICS Modbus TCP Server: %s", e)
        
    try:
        log.debug("Starting monitoring and control thread...")
        Thread(target=monitor_and_control, daemon=True).start()
    except Exception as e:
        log.critical("Failed to start monitoring and control thread: %s", e)

    try:
        log.debug("Running authentication API on port %d" % ics.constants.ICS_API_PORT)
        serve(app, host='localhost', port=ics.constants.ICS_API_PORT)
    except Exception as e:
        log.critical("Failed to start authentication API on port %d" % ics.constants.ICS_API_PORT)


if __name__ == "__main__":
    start_ics_server()
