# ICS Client Webserver using Modbus TCP to control airport runway lights

from flask import Flask, render_template, request, jsonify
from pymodbus.client import ModbusTcpClient

app = Flask(__name__)

# Replace with actual server IP of the ICS server
ICS_SERVER_IP = '127.0.0.1'  # Change to your Modbus server's IP
ICS_SERVER_PORT = 502  # Modbus port

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/control', methods=['POST'])
def control():
    runway = request.form['runway']
    action = request.form['action']

    # Map runway to Modbus coil address
    coil_map = {'RWY_1': 0, 'RWY_2': 1}
    coil_address = coil_map.get(runway)
    coil_state = True if action == 'ON' else False

    try:
        client = ModbusTcpClient(ICS_SERVER_IP, port=ICS_SERVER_PORT)
        client.connect()
        result = client.write_coil(coil_address, coil_state)
        client.close()
        if result.isError():
            raise Exception("Modbus write error")
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

    return jsonify({'status': 'success', 'response': f'{runway} lights set to {action}'})

# Start the SCADA Web Server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
