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
DEVICE = os.getenv("GOVEE_DEVICE")

def light_up_segment(segment_id, color=0xFFFFFF):
    print(f"Lighting up segment {segment_id}")

    rgb_payload = {
        "requestId": "light-up",
        "payload": {
            "sku": SKU,
            "device": DEVICE,
            "capability": {
                "type": "devices.capabilities.segment_color_setting",
                "instance": "segmentedColorRgb",
                "value": {
                    "segment": [segment_id],
                    "rgb": color
                }
            }
        }
    }


    try:
        rgb_response = requests.post(API_URL, headers=HEADERS, json=rgb_payload)
        print("RGB Response:", rgb_response.status_code, rgb_response.text)

    except Exception as e:
        print(f"Error lighting up segment: {e}")

def reset_lights(segments=list(range(10))):
    # Set brightness for all segments to 0
    reset_payload = {
        "requestId": "light-up",
        "payload": {
            "sku": SKU,
            "device": DEVICE,
            "capability": {
                "type": "devices.capabilities.segment_color_setting",
                "instance": "segmentedColorRgb",
                "value": {
                    "segment": segments,
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
            "device": DEVICE,
            "capability": {
                "type": "devices.capabilities.segment_color_setting",
                "instance": "segmentedBrightness",
                "value": {
                    "segment": segments,
                    "brightness": 100
                }
            }
        }
    }

    try:
        brightness_response = requests.post(API_URL, headers=HEADERS, json=reset_payload)
        print("Brightness Response:", brightness_response.status_code, brightness_response.text)

        brightness_response = requests.post(API_URL, headers=HEADERS, json=brightness_payload)
        print("Brightness Response:", brightness_response.status_code, brightness_response.text)

    except Exception as e:
        print(f"Error resetting lights: {e}")
