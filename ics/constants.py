# --- Constants ---
ICS_SERVER_PORT = 5020  # Use 502 in production so wireshark autodetects protocol
ICS_API_PORT = 54321 # Port on which the authenticator API listens
COIL_RUNWAY_LIGHT = 0   # Coil address 0 represents the only runway light
SOLVE_DELAY = 60 # Number of seconds light needs to be on before considering the challenge solved
CHECK_INTERVAL = 0.5 # Interval at which it will check that runwaylight is on, both when considering if challenge is solved and in main thred
MIN_TEASE_TIME = 10 # Minimal time that lights will be on when 'teasing' the players