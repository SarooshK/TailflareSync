import requests
import os
import time
import json
from cloudflare import Cloudflare

#Tailscale base API URL
tailscale_url = "https://api.tailscale.com/api/v2"

#Tailscale API Keys
tailnet_id = os.getenv("TAILNET_ID")
tailnet_api_key = os.getenv("TAILNET_API_KEY")

#Cloudflare base API URL
cloudflare_url = "https://api.cloudflare.com/client/v4"

#Cloudflare API Key
cloudflare_api_key = os.getenv("CLOUDFLARE_API_KEY")
cloudflare_email = os.getenv("CLOUDFLARE_EMAIL")

#Cloudflare Zone ID - Can be found under the domain details on Cloudflare Admin page
cloudflare_zone_id = os.getenv("CLOUDFLARE_ZONE_ID")

#Domain URL - example google.com - the domain that the records will be added to
domain_URL = os.getenv("DOMAIN_URL")

while True:
    #Fetch Tailscale devices
    tailscale_request_URL = tailscale_url + "/tailnet/" + str(tailnet_id) + "/devices"

    tailscale_devices = requests.get(
    tailscale_request_URL,
    headers={
      "Authorization": "Bearer " + str(tailnet_api_key)
    })

    tailscale_devices_json = tailscale_devices.json()

    #Fetch DNS records from Cloudflare
    cloudflare_request_URL = cloudflare_url + "/zones/" + cloudflare_zone_id + "/dns_records"

    cloudflare_DNS_records = requests.get(
        cloudflare_request_URL,
    headers={
      "Authorization": "Bearer " + cloudflare_api_key
    })

    cloudflare_DNS_records_json = cloudflare_DNS_records.json()

    #Iterate though all the devices in the tailscale JSON object and pull the name prefix and IP
    for device in tailscale_devices_json["devices"]:

        #Get the name field and parse the prefix from the address
        name = device.get("name","")
        prefix_name = name.split(".",1)[0] if name else "(no-name)"

        #get the first IPv4 address per device
        ipv4 = next((a for a in device.get("addresses", []) if "." in a), None)
        ipv4 = ipv4 or "(no-ipv4)"

        for record in cloudflare_DNS_records_json["result"]:
            #print(record.get("name"))
            #print(prefix_name + "." + domain_URL)
            if prefix_name + "." + domain_URL == record.get("name"):
                print("name found")
                if ipv4 == record.get("content"):
                    print("IP is up to date - Skipping")
                else:
                    print("IP NOT UPDATED")

    print("Sleeping for 5Min now")
    time.sleep(300)