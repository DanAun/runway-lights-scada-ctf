# List of functionalities that govee supports that we did not use for the CTF

import os
import requests
 
# Govee API settings
api_url = "https://openapi.api.govee.com/router/api/v1/device/control"
headers = {
    "Content-Type": "application/json",
    "Govee-API-Key": os.getenv("GOVEE_API_KEY")
}

sku = os.getenv("GOVEE_SKU")
serial = os.getenv("GOVEE_DEVICE_1")

state_path = '/router/api/v1/device/state'
control_path = '/router/api/v1/device/control'
scenes_path = '/router/api/v1/device/scenes'
diys_path = '/router/api/v1/device/diy-scenes'

def send_request(path, data):
    response = requests.post(api_url + path, headers=headers, json=data)
    print(response.status_code, response.text)

#
#   WHOLE LED STRIP
#

def get_capabilities():
    data = {
        "requestId": "uuid",
        "payload": {
            "sku": sku,
            "device": serial
        }
    }

    send_request(state_path, data)


def toggle_on():
    data = {
        "requestId": "uuid",
        "payload": {
            "sku": sku,
            "device": serial,
            "capability": {
                "type": "devices.capabilities.on_off",
                "instance": "powerSwitch",
                "value": 1
            }
        }
    }

    send_request(control_path, data)

def toggle_off():
    data = {
        "requestId": "uuid",
        "payload": {
            "sku": sku,
            "device": serial,
            "capability": {
                "type": "devices.capabilities.on_off",
                "instance": "powerSwitch",
                "value": 0
            }
        }
    }

    send_request(control_path, data)

# Values between 0 and 255
def color_rgb(r, g, b):
    
    color = ((r & 0xFF) << 16) | ((g & 0xFF) << 8) | ((b & 0xFF) << 0)
    
    data = {
        "requestId": "uuid",
        "payload": {
            "sku": sku,
            "device": serial,
            "capability": {
                "type": "devices.capabilities.color_setting",
                "instance": "colorRgb",
                "value": color
            }
        }
    }

    send_request(control_path, data)

# temperature between 2000 and 9000
def color_temperature_k(temperature):
    data = {
        "requestId": "uuid",
        "payload": {
            "sku": sku,
            "device": serial,
            "capability": {
                "type": "devices.capabilities.color_setting",
                "instance": "colorTemperatureK",
                "value": temperature
            }
        }
    }

    send_request(control_path, data)

# value between 1 and 100
def brightness(value):
    data = {
        "requestId": "1",
        "payload": {
            "sku": sku,
            "device": serial,
            "capability": {
                "type": "devices.capabilities.range",
                "instance": "brightness",
                "value": value
            }
        }
    }

    send_request(control_path, data)

##############################################
#   1 < musicMode < 11
#   1 < sensitivity < 100
#   autoColor:       1 = ON, 0 = OFF
#   0 <  r,g,b < 255
##############################################
def music_mode(musicMode, sensitivity, autoColor, r, g, b):
    
    color = ((r & 0xFF) << 16) | ((g & 0xFF) << 8) | ((b & 0xFF) << 0)
    
    data = {
        "requestId": "1",
        "payload": {
            "sku": sku,
            "device": serial,
            "capability": {
                "type": "devices.capabilities.music_setting",
                "instance": "musicMode",
                "value": {
                    "musicMode":musicMode,
                    "sensitivity":sensitivity,
                    "autoColor":autoColor,
                    "rgb": color
                }
            }
        }
    }

    send_request(control_path, data)

#
#   SEGMENTS
#

##############################################
#   0 < segments < 19   (array of int)
#   0 <  r,g,b < 255
##############################################
def change_segment_color(segments, r, g, b):

    color = ((r & 0xFF) << 16) | ((g & 0xFF) << 8) | ((b & 0xFF) << 0)
    
    data = {
        'requestId': '1',
        'payload': {
            'sku': sku,
            'device': serial,
            'capability': {
                'type': 'devices.capabilities.segment_color_setting',
                'instance': 'segmentedColorRgb',
                'value': {
                    'segment': segments,
                    'rgb': color
                }
            }
        }
    }

    send_request(control_path, data)

##############################################
#   0 < segments < 19   (array of int)
#   0 <  value < 100
##############################################
def change_segment_brightness(segments, value):
    data = {
        'requestId': '1',
        'payload': {
            'sku': sku,
            'device': serial,
            'capability': {
                'type': 'devices.capabilities.segment_color_setting',
                'instance': 'segmentedBrightness',
                'value': {
                    'segment': segments,
                    'brightness': value
                }
            }
        }
    }

    send_request(control_path, data)



#
#   SCENES / DIY
#

##############################################
#   Returns a JSON of the available scenes
##############################################
def get_scenes():
    data = {
        'requestId': 'uuid',
        'payload': {
            'sku': sku,
            'device': serial
        }
    }

    send_request(scenes_path, data)

# Use the values returned by get_scenes()
def set_scene(value):
    data = {
        "requestId": "1",
        "payload": {
            "sku": sku,
            "device": serial,
            "capability": {
                "type": "devices.capabilities.dynamic_scene",
                "instance": "lightScene",
                "value": value
            }
        }
    }

    send_request(control_path, data)

##############################################
#   Returns a JSON of the available diys
##############################################
def get_diys():
    data = {
        'requestId': 'uuid',
        'payload': {
            'sku': sku,
            'device': serial
        }
    }

    send_request(diys_path, data)

# Use the values returned by get_diys()
def set_diy(value):
    data = {
        "requestId": "1",
        "payload": {
            "sku": sku,
            "device": serial,
            "capability": {
                "type": "devices.capabilities.dynamic_scene",
                "instance": "diyScene",
                "value": value
            }
        }
    }

    send_request(control_path, data)

# First create a snapshot in Govee Home
def snapshot(value):
    data = {
        "requestId": "1",
        "payload": {
            "sku": sku,
            "device": serial,
            "capability": {
                "type": "devices.capabilities.dynamic_scene",
                "instance": "snapshot",
                "value": value
            }
        }
    }

    send_request(control_path, data)


#
#   TESTS
#


# get_capabilities()

# color_rgb(255,0,255)
# color_temperature_k(9000)
# brightness(25)

# get_diys()
# set_diy(15876728)

# music_mode(2, 20, 0, 255, 0, 255)