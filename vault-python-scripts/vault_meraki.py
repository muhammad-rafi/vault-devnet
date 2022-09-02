import requests 
import hvac

client = hvac.Client(url='http://<meraki_ip>:8200') 
read_response = client.secrets.kv.read_secret_version(path='meraki') 

MERAKI_API_KEY = 'X-Cisco-Meraki-API-Key' 
ORG_ID='123456' 

MERAKI_API_VALUE = read_response['data']['data']['MERAKI_API_VALUE'] 

url = 'https://api.meraki.com/api/v0/organizations/{}/inventory'.format(ORG_ID) 
response = requests.get(url=url, 
           headers={MERAKI_API_KEY : MERAKI_API_VALUE, 
           'Content-type': 'application/json'}) 

switch_list = response.json() 

switch_serial = [] 

for i in switch_list: 
    if i['model'][:2] in ('MS') and i['networkId'] is not None:
    switch_serial.append(i['serial']) 

print(switch_serial)