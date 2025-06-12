# Runway Lights SCADA CTF

This project simulates a simplified SCADA system for controlling airport runway lights using Modbus TCP. It is divided into three components:

## Components

1. **ics/**  
   Contains the **Modbus TCP ICS server**, simulating the physical system (runway lights). It listens for Modbus commands and updates the simulated light status.

2. **scada/**  
   Contains the **Flask-based web SCADA interface**, allowing users to log in and control the runway lights via a web interface. The interface polls the ICS server to display real-time light status.

3. **malicious/**  
   This folder contains code for a simple process that continuously sends a power-off signal to the runway lights. The goal of the CTF challenge should be to identify and shut down this process.

---

## How to Run in Developement

Make sure you have Python 3 installed. Then:

1. **Install dependencies:**

```bash
pip install -r requirements.txt
```

2. **Start all 3 processes:**

```bash
python main.py
```

**Alternatively, you can run each component separately:**

```bash
python -m ics.ics
python -m scada.scada
python -m malicious.malicious
```

## How to compile

1. **Install dependencies:**

Install dependencies if you haven't already

```bash
pip install -r requirements.txt
```

2. **Compile each component:**
```bash
pyinstaller ics.spec
pyinstaller scada.spec
pyinstaller malicious.spec
```

## Notes

* The SCADA interface requires login and displays live runway status, with the ability to toggle lights ON/OFF.
* ICS logic may enforce basic rules (e.g., deny invalid state transitions).
* Status polling ensures the UI reflects the real-time state of the lights.