import logging

log = logging.getLogger("ICS")

import requests
import os
from dotenv import load_dotenv, dotenv_values 
load_dotenv()

# Govee API settings
API_URL = "https://openapi.api.govee.com/router/api/v1/device/control"
HEADERS = {
    "Content-Type": "application/json",
    "Govee-API-Key": os.getenv("GOVEE_API_KEY")
}
SKU = os.getenv("GOVEE_SKU")

def get_device_id(strip_num : int):
    """
    Gets the device ID for the strip (1-4)
    """
    return os.getenv("GOVEE_DEVICE_" + str(strip_num))

def activate_team_light(team_num):
    """
    Activates the given team_num's corresponding LED segments by calling light_up_segments with correct device and segment
    team_num should be from 1-40
    """

    if not 0 < team_num < 40:
        raise ValueError("team_num should be in range 1-40")
    team_num -= 1 # Convert from range 1-40 to 0-39
    strip = team_num // 10 + 1
    segment = team_num % 10
     
    light_up_segments(strip, segment)


def light_up_segments(strip_num, segment_id, color=0xFFFFFF):
    log.debug(f"Lighting up segment {segment_id}")
    device_id = get_device_id(strip_num)

    # Check if segment_id is a list; if not, convert it to a list
    if isinstance(segment_id, list):
        segments = segment_id  # Use the list as is
    elif isinstance(segment_id, int):
        segments = [segment_id]  # Wrap the integer in a list
    else:
        raise ValueError("segment_id must be an integer or a list of integers.")

    rgb_payload = {
        "requestId": "light-up",
        "payload": {
            "sku": SKU,
            "device": device_id,
            "capability": {
                "type": "devices.capabilities.segment_color_setting",
                "instance": "segmentedColorRgb",
                "value": {
                    "segment": segments,
                    "rgb": color
                }
            }
        }
    }


    try:
        rgb_response = requests.post(API_URL, headers=HEADERS, json=rgb_payload)
        if rgb_response.status_code == 200:
            log.info("Successfully turned on segment(s) %s on strip number %d" % (segment_id, strip_num))
        else:
            log.error("Something went wrong when turning on segment(s) %s on strip number %d. ERROR CODE: %s - %s" % (segment_id, strip_num, rgb_response.status_code, rgb_response.text))

    except Exception as e:
        log.error(f"Error lighting up segment: {e}")

def reset_all_strips():
    for i in range(1,5):
        reset_strip(i)
        
def reset_strip(strip_num):
    """
    Reset the strip corresponding to strip_num.
    This means we turn off all segments and set brighntess to max to ready the lights for use.
    """

    if not 0 < strip_num < 5:
        raise ValueError("strip_num should be 1-4")
    device_id = get_device_id(strip_num)
    # Set all segments to no light
    no_light_payload = {
        "requestId": "light-up",
        "payload": {
            "sku": SKU,
            "device": device_id,
            "capability": {
                "type": "devices.capabilities.segment_color_setting",
                "instance": "segmentedColorRgb",
                "value": {
                    "segment": list(range(10)),
                    "rgb": 0x000000  # Black -> OFF
                }
            }
        }
    }

    # Set brightness for all segments to 100
    brightness_payload = {
        "requestId": "brightness-up",
        "payload": {
            "sku": SKU,
            "device": device_id,
            "capability": {
                "type": "devices.capabilities.segment_color_setting",
                "instance": "segmentedBrightness",
                "value": {
                    "segment": list(range(10)),
                    "brightness": 100
                }
            }
        }
    }

    try:
        no_light_response = requests.post(API_URL, headers=HEADERS, json=no_light_payload)
        if no_light_response.status_code == 200:
            log.debug("Successfully set light off")
        else:
            log.error("Something went wrong when setting lights to OFF", 'ERROR CODE: ' + no_light_response.status_code, no_light_response.text)

        brightness_response = requests.post(API_URL, headers=HEADERS, json=brightness_payload)
        if brightness_response.status_code == 200:
            log.debug("Successfully set brightness of LEDs to 100")
        else:
            log.error("Something went wrong when setting brighntess to 100", 'ERROR CODE: ' + brightness_response.status_code, brightness_response.text)

        if no_light_response.status_code == 200 and brightness_response.status_code == 200:
            log.info("Successfully reset strip %d" % strip_num)

    except Exception as e:
        log.error(f"Error resetting lights: {e}")
