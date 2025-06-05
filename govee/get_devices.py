import requests
import json
import os
from dotenv import load_dotenv, dotenv_values 
load_dotenv()

# Define the API endpoint and headers
url = "https://openapi.api.govee.com/router/api/v1/user/devices"
headers = {
    "Content-Type": "application/json",
    "Govee-API-Key": os.getenv("GOVEE_API_KEY")
}

# Make the GET request
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    json_data = response.json()
    
    # Write the JSON data to a file
    with open('devices.json', 'w') as json_file:
        json.dump(json_data, json_file, indent=4)  # Write with indentation for readability
    
    print("JSON response written to devices.json")
else:
    print(f"Error: {response.status_code} - {response.text}")
