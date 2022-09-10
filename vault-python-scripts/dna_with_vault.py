import requests
import hvac
import urllib3
from pprint import pprint

urllib3.disable_warnings()  

# dnac_username = 'devnetuser'
# dnac_password = 'Cisco123!'

# This script is using 'localhost' as Vault Server IP and default mount point of 'secret' 
# with KV Version 2.

client = hvac.Client(url='https://localhost:8200') 
read_response = client.secrets.kv.read_secret_version(path='dnac-secrets')  

dnac_ip = "sandboxdnac.cisco.com"
username = read_response['data']['data']['dnac_username'] 
password = read_response['data']['data']['dnac_password'] 

# Get the DNA API TOKEN 
url = "https://{}/dna/system/api/v1/auth/token".format(dnac_ip)
headers = {}
response =  requests.post(
        url, 
        auth=(username, password), 
        headers = headers,
        verify=False
)

DNAC_TOKEN =  response.json()["Token"]
# pprint(DNAC_TOKEN)

# GET THE LIST OF DEVICES 
url = f"https://{dnac_ip}/dna/intent/api/v1/network-device"
headers = {"x-auth-token": DNAC_TOKEN}

response =  requests.get(url, headers=headers, verify=False)
pprint(response.json())

