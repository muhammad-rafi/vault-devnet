import hvac
import requests
import os 
import json
from rich import print

'''
This script is only using Kv-v2 only, however, link is given for the kv-v1 two below; 

KV Secrets Engine - Version 1 (API)
https://www.vaultproject.io/api-docs/secret/kv/kv-v1

KV Secrets Engine - Version 2 (API)
https://www.vaultproject.io/api-docs/secret/kv/kv-v2
'''

cacert = os.environ['VAULT_CACERT']
vault_token=os.environ['VAULT_TOKEN']
vault_url = os.environ['VAULT_ADDR']

headers = {
    'X-Vault-Token': vault_token
}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Get the sealed status of the Vault server 
mount_points = requests.get(f'{vault_url}/v1/sys/seal-status', 
                            headers=headers, 
                            verify=cacert)

print(mount_points.json())

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Get the list of auth methods available
auth_list = requests.get(f'{vault_url}/v1/sys/auth', 
                            headers=headers, 
                            verify=cacert)

print(auth_list.json())

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# List Mounted Secrets Engines
mount_points = requests.get(f'{vault_url}/v1/sys/mounts', 
                            headers=headers, 
                            verify=cacert)

# print(mount_points.json())

# mount_points_dict = json.loads(mount_points.text).keys()
mount_points_dict = mount_points.json().keys()
# print(mount_points_dict)

for mount_point in mount_points_dict: 
    suffix = "/"
    if mount_point.endswith(suffix) == True: 
        print(mount_point)

# #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# # Create new KV secret engine with custom mount point 

# mount_point = 'test-kv'
# payload = {
#             "type": "kv",
#             "config": {
#                 "force_no_cache": True
#                 },
#             "option": {
#                 "version": "2"
#                 }
#             }

# response = requests.post(f'{vault_url}/v1/sys/mounts/{mount_point}', 
#                         headers=headers,
#                         data=json.dumps(payload),
#                         verify=cacert
#                         )

# print(response.json())

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Get the list of secrets available in the default mount point of 'secret'
secret_list = requests.get(f'{vault_url}/v1/secret/metadata?list=true', 
                            headers=headers, 
                            verify=cacert)

print(secret_list.json())

# Get the list of secrets available in the custom mount point of 'dev-creds'
secret_list = requests.get(f'{vault_url}/v1/dev-creds/metadata?list=true', 
                            headers=headers, 
                            verify=cacert)

print(secret_list.json())
