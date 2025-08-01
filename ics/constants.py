import os

# --- Constants ---
ICS_SERVER_IP = os.getenv("ICS_SERVER_IP", "127.0.0.1")
ICS_SERVER_PORT = int(os.getenv("ICS_SERVER_PORT", "5020"))  # Use 502 in production so wireshark autodetects protocol
ICS_API_PORT = int(os.getenv("ICS_API_PORT", "54321")) # Port on which the ICS API listens
COIL_RUNWAY_LIGHT = 0   # Coil address 0 represents the only runway light
SOLVE_DELAY = 40 # Number of seconds light needs to be on before considering the challenge solved
CHECK_INTERVAL = 0.5 # Interval at which it will check that runwaylight is on, both when considering if challenge is solved and in main thred
MIN_TEASE_TIME = 10 # Minimal time that lights will be on when 'teasing' the players

# --- CTF FLAG values ---
key_b64 = b'p4d6v1hgvO3bAkQPO_Ms9TM6mPKa_2YkFa1W8Wlapiw='
flag_enc = b'gAAAAABojJh_ndpB3QxsnqbtFGHtgT6zVLZUiZ85xPXSazbNDhXwrUAnsMmLArrgsfw8Czd7HJcVIdokSGTIzeONaOPs3kVmTDR50nXzEOTYgKfMDQ_5xDVGP-jRktH2hbh5ULbrZMc_'