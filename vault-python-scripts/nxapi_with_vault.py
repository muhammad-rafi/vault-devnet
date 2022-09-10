import requests
from rich import print 
import hvac
import json
import os
import urllib3

urllib3.disable_warnings()

# make sure you have following environmental variable exported
client = hvac.Client(url=os.environ['VAULT_ADDR'],
                    token=os.environ['VAULT_TOKEN'], 
                    verify=os.environ['VAULT_CACERT']
                    )

read_response = client.secrets.kv.v2.read_secret_version(mount_point='cisco-sandboxes', 
                                                         path='nxos-sandbox',)
host = 'sbx-nxos-mgmt.cisco.com'
username = read_response['data']['data']['nxos_username'] 
password = read_response['data']['data']['nxos_password'] 

# Retrieve the NXAPI Token by using the username and password we pulled from the Vault server
auth_cookie = {}
login_url = f"https://{host}/api/aaaLogin.json"
payload = {
    'aaaUser' : {
        'attributes' : {
            'name' : username,
            'pwd' : password
            }
        }
    }

login_response = requests.post(login_url, data=json.dumps(payload), verify=False)
if login_response.status_code == requests.codes.ok:
    data = json.loads(login_response.text)['imdata'][0]
    token = str(data['aaaLogin']['attributes']['token'])
    auth_cookie = {"APIC-cookie" : token}
    # print(auth_cookie)


version_url = "https://" + host + "/api/mo/sys/showversion.json"
version_response = requests.request("GET", version_url,
                            cookies=auth_cookie, verify=False)

data = json.loads(version_response.text)['imdata'][0]['sysmgrShowVersion']['attributes']
os_version = data['nxosVersion']
up_time = data['kernelUptime']

print(f"NXOS Version: {os_version}")
print(f"System Uptime: {up_time}")
