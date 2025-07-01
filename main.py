from threading import Thread
from govee.govee_control import reset_all_strips
from scada.scada import app, SCADA_WEB_PORT
from ics.ics import start_ics_server
from malicious.malicious import loop_modbus_request
from waitress import serve

if __name__ == "__main__":
    # Run ICS server in a background thread
    ics_thread = Thread(target=start_ics_server, daemon=True).start()
    #malicious_thread = Thread(target=loop_modbus_request, daemon=True).start()
    #Thread(target=reset_all_strips, daemon=True).start()

    # Run Flask server in main thread (blocking call)
    serve(app, host='localhost', port=SCADA_WEB_PORT)
