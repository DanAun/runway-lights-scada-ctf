import logging
log = logging.getLogger("ICS")

import requests
import os
from dotenv import load_dotenv
load_dotenv()

# Constants
STRIPS_USED = 4 # Number of LED strips used
SEGMENT_PER_STRIP = 10 # Number of segments on the strips
MAX_TEAM_NUM = STRIPS_USED * SEGMENT_PER_STRIP # Max number of teams we can include with the LEDs
DEFAULT_LIGHT_COLOR = 0xFFFFFF # Default light color when lighing up segments

# Govee API settings
API_URL = "https://openapi.api.govee.com/router/api/v1/device/control"
HEADERS = {
    "Content-Type": "application/json",
    "Govee-API-Key": os.getenv("GOVEE_API_KEY")
}
SKU = os.getenv("GOVEE_SKU")

def get_device_id(strip_num : int):
    """
    Gets the device ID for the strips (1-STRIPS_USED)
    """
    id = os.getenv("GOVEE_DEVICE_" + str(strip_num))
    if not id:
        raise KeyError("Missing GOVEE_DEVICE_" + "%d value in .env for strip %d" % (strip_num, strip_num))
    else:
        return id

def activate_team_light(team_num):
    """
    Activates the given team_num's corresponding LED segments by calling light_up_segments with correct device and segment
    team_num should be from 1 to MAX_TEAM_NUM
    """
    if team_num not in range(1,MAX_TEAM_NUM+1):
        raise ValueError("team_num should be in range 1 to %d" % MAX_TEAM_NUM+1)
    team_id = team_num - 1
    strip = (team_id // SEGMENT_PER_STRIP) + 1
    segment = team_id % SEGMENT_PER_STRIP
    try:
        light_up_segments(strip, segment)
        log.info("Successfully activated team %d's LED segment!" % (team_num))
    except Exception as e:
        log.critical("Failed to turn on team %d's LED segment because: %s" % (team_num, e))


def light_up_segments(strip_num, segment_id, color=DEFAULT_LIGHT_COLOR):
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
            log.debug("Successfully turned on segment(s) %s on strip number %d" % (segment_id, strip_num))
        else:
            log.error("Something went wrong when turning on segment(s) %s on strip number %d. ERROR CODE: %s - %s" % (segment_id, strip_num, rgb_response.status_code, rgb_response.text))

    except Exception as e:
        log.error(f"Error lighting up segment: {e}")

def reset_all_strips():
    try:
        for i in range(1,STRIPS_USED+1):
            reset_strip(i)
        log.info("Successfully reset all strips!")
    except Exception as e:
        log.error("Failed to reset all strips! Following exception encountered: %s" % e)
        
def reset_strip(strip_num):
    """
    Reset the strip corresponding to strip_num.
    This means we turn off all segments and set brighntess to max to ready the lights for use.
    """

    if strip_num not in range(1,STRIPS_USED+1):
        raise ValueError("strip_num should be in range 1 to %d" % STRIPS_USED)
    try:
        device_id = get_device_id(strip_num)
    except KeyError as e:
        log.error("Failed to reset strip %d because: %s" % (strip_num, e))
        return
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
                    "segment": list(range(SEGMENT_PER_STRIP)),
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
                    "segment": list(range(SEGMENT_PER_STRIP)),
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
            log.debug("Successfully reset strip %d" % strip_num)

    except Exception as e:
        log.error(f"Exception when resetting strip {strip_num}: {e}")
