from threading import Thread
from scada.scada import app, SCADA_WEB_PORT
from ics.ics import start_ics_server
from malicious.malicious import loop_modbus_request

if __name__ == "__main__":
    # Run ICS server in a background thread
    ics_thread = Thread(target=start_ics_server, daemon=True)
    ics_thread.start()
    malicious_thread = Thread(target=loop_modbus_request, daemon=True)
    #malicious_thread.start()

    # Run Flask server in main thread (blocking call)
    app.run(host="0.0.0.0", port=SCADA_WEB_PORT)
