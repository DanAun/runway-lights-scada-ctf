import logging
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from pymodbus.client import ModbusTcpClient
from ics.ics import ICS_SERVER_PORT
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Use a fixed key in production

# Dummy credentials
USERNAME = "admin"
PASSWORD = "password"

ICS_SERVER_IP = '127.0.0.1'
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

@app.route('/')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    result = get_light_status()

    if result is None:
        status = "Error"
    else:
        status = "ON" if result else "OFF"

    return render_template('index.html', status=status)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == USERNAME and request.form['password'] == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Invalid credentials.")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/toggle', methods=['POST'])
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
    result = get_light_status()
    if result is None:
        return jsonify({'error': 'Modbus read failed'}), 500
    return jsonify({'runway_lights_state': result})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
