import requests
import os
import time

#Tailscale base API URL
tailscale_url = "https://api.tailscale.com/api/v2"

#Tailscale API Keys
tailnet_id = os.getenv("TAILNET_ID")
tailnet_api_key = os.getenv("TAILNET_API_KEY")

while True:
    requestURL = tailscale_url + "/tailnet/" + str(tailnet_id) + "/devices"

    tailscaleDevices = requests.get(
    requestURL,
    headers={
      "Authorization": "Bearer " + str(tailnet_api_key)
    })

    json_devices = tailscaleDevices.json()
    
    print("========================")
    print("   TAILSCALE DEVICES")
    print("========================")

    num = 0
    
    for devices in json_devices:
        num += 1
        print(num)

    time.sleep(300)