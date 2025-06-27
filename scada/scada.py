import logging

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,  # Set the logging level
    format='%(asctime)s - [SCADA] - %(levelname)s: %(message)s',  # Custom format
    datefmt='%H:%M:%S'  # Display only hour, minute, and second
)

import sys
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_limiter import Limiter
from pymodbus.client import ModbusTcpClient
import requests
from ics.constants import ICS_SERVER_PORT, ICS_API_PORT
import os
from waitress import serve

if getattr(sys, 'frozen', False):
    # Running in a PyInstaller bundle
    base_path = sys._MEIPASS
else:
    base_path = os.path.abspath(".")

template_path = os.path.join(base_path, "scada", "templates")
static_path = os.path.join(base_path, "scada", "static")

app = Flask(__name__, template_folder=template_path, static_folder=static_path)
app.secret_key = os.urandom(24)

log = logging.getLogger('werkzeug')
log.setLevel(logging.WARN)


ICS_SERVER_IP = '127.0.0.1'
SCADA_WEB_PORT = 8000 # Port of SCADA webUI server ti be started on
COIL_ADDRESS = 0  # Single runway light coil address

def get_light_status():
    """Function to read the current status of the runway light."""
    client = ModbusTcpClient(ICS_SERVER_IP, port=ICS_SERVER_PORT)
    client.connect()
    try:
        result = client.read_coils(COIL_ADDRESS, count=1)
    except Exception as e:
        logging.error(f"Modbus read error: {e}")
        return None  # Handle read errors gracefully
    finally:
        client.close()
    return result.bits[0]

def received_flag():
    """Function that reads flag from ics server when challenge is solved. Returns None if challenge is not solved."""
    # Send a request to the ICS API for authentication
    try:
        response = requests.get(f'http://{ICS_SERVER_IP}:{ICS_API_PORT}/api/flag')
        if response.status_code == 200:
            return response.json().get('flag')
        elif response.status_code == 403:
            return None
        else:
            raise requests.exceptions.RequestException
    except requests.exceptions.RequestException as err:
        log.error("Failed to retreive flag from ics server!", err)

@app.route('/')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    status = get_status()
    #status = "ECTL{{eifjw0ifjwo0}}"

    return render_template('index.html', status=status)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Send a request to the ICS API for authentication
        try:
            response = requests.post(f'http://{ICS_SERVER_IP}:{ICS_API_PORT}/api/login', json={'username': username, 'password': password})
            if response.status_code == 200:
                session['logged_in'] = True
                return redirect(url_for('home'))
            elif response.status_code == 403:
                return render_template('login.html', error="Invalid credentials.")
            else:
                raise requests.exceptions.RequestException
        except requests.exceptions.RequestException as err:
            return render_template('login.html', error="Failed to communicate with ICS server. Call CTF staff!")
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Initialize the Limiter
limiter = Limiter(
    key_func=lambda: "global",  # Use a fixed key for all requests
    app=app,
    default_limits=[]  # No default limits, we will set specific limits on routes
)

@app.route('/toggle', methods=['POST'])
@limiter.limit("1 per second")  # Rate limit for this specific route
def toggle():
    if not session.get('logged_in'):
        return jsonify({'status': 'unauthorized'}), 401

    action = request.form.get('action')
    state = True if action == "ON" else False

    client = ModbusTcpClient(ICS_SERVER_IP, port=ICS_SERVER_PORT)
    client.connect()
    result = client.write_coil(COIL_ADDRESS, state)
    client.close()

    if result.isError():
        return jsonify({'status': 'error', 'message': 'Modbus write failed'})
    return jsonify({'status': 'success', 'message': f'Runway lights turned {action}'})

@app.route('/status', methods=['GET'])
def get_status():
    if not session.get('logged_in'):
        return jsonify({'status': 'unauthorized'}), 401
    flag = received_flag()
    if flag is not None:
        log.info("Returned flag to the team!")
        return jsonify({'runway_lights_state': flag})
    result = get_light_status()
    if result is None:
        return jsonify({'error': 'Modbus read failed'}), 500
    return jsonify({'runway_lights_state': result})


if __name__ == '__main__':
    try:
        serve(app, host='localhost', port=SCADA_WEB_PORT)
    except KeyboardInterrupt:
        log.info("Server shutdown by user")
