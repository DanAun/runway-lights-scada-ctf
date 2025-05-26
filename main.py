from threading import Thread
from scada.scada import app
from ics.ics import start_ics_server

if __name__ == "__main__":
    # Run ICS server in a background thread
    ics_thread = Thread(target=start_ics_server, daemon=True)
    ics_thread.start()

    # Run Flask server in main thread (blocking call)
    app.run(host="0.0.0.0", port=8000)
