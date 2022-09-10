import requests
import json
import hvac

# This script is using 'localhost' as Vault Server IP and default mount point of 'secret'
# with KV Version 2.

client = hvac.Client(url='https://localhost:8200') 
read_response = client.secrets.kv.read_secret_version(path='meraki-secrets')  

MERAKI_API_KEY = read_response['data']['data']['MERAKI_API_KEY'] 
MERAKI_ORG_ID=read_response['data']['data']['MERAKI_ORG_ID'] 
list_switches_serial_no = [] 

# List the switches serial numbers
url = 'https://api.meraki.com/api/v0/organizations/{}/inventory'.format(MERAKI_ORG_ID) 
response = requests.get(url=url, 
           headers={"X-Cisco-Meraki-API-Key" : MERAKI_API_KEY, 
           'Content-type': 'application/json'}
           ) 

switches = response.json() 

for switch in switches: 
    if switches['model'][:2] in ('MS') and switches['networkId'] is not None:
        list_switches_serial_no.append(switches['serial']) 

    print(list_switches_serial_no)

# List of networks 
url = 'https://api.meraki.com/api/v0/organizations/{}/networks'.format(MERAKI_ORG_ID)
response = requests.get(url=url, 
           headers={"X-Cisco-Meraki-API-Key" : MERAKI_API_KEY, 
           'Content-type': 'application/json'}
           )

list_networks = response.json()

print(json.dumps(list_networks, indent=4))

