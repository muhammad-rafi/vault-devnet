import hvac
import os 
import json
from rich import print

cacert = os.environ['VAULT_CACERT']
vault_token=os.environ['VAULT_TOKEN']
vault_url = os.environ['VAULT_ADDR']

'''
References:
https://hvac.readthedocs.io/en/stable/usage/secrets_engines/kv_v1.html
https://hvac.readthedocs.io/en/stable/usage/secrets_engines/kv_v2.html
'''

# Note: set verify=False if you want to avoid using the ca cert. 
# and remove 'verify' patameter if you are using plain text HTTP.

client = hvac.Client(url=vault_url, token=vault_token, verify=cacert)

# Comment/Uncomment the code as needed, However, 
# I left the KV-2 with the custom mount point uncommented.

# create_response = client.secrets.kv.create_or_update_secret(path='test-creds', secret=dict(username='devnet', password='Cisco123!'))
# read_response = client.secrets.kv.read_secret(path='test-creds')
# print(read_response['data']['data']['username'])
# print(read_response['data']['data']['password'])
# print(dir(client.secrets.kv))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# When you use the default mount point of 'secret' with KV version 1     #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# # Create or update a secret 
# create_response = client.secrets.kv.v1.create_or_update_secret(path='test-creds', secret=dict(username='devnet', password='Cisco123!'))
# print(create_response.text)

# # Fetch the secret data 
# read_response = client.secrets.kv.v1.read_secret('test-creds') 
# print(read_response['data']['username'])
# print(read_response['data']['password'])

# # Delete secrets 
# delete_response = client.secrets.kv.v1.delete_secret('test-creds')
# print(delete_response)

# # List of secrets 
# list_response = client.secrets.kv.v1.list_secrets(path='test-creds',)
# print(json.dumps(list_response, indent=2))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# When you use the custom mount point of 'dev-creds' with KV version 1   #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# # Create or update a secret 
# create_response = client.secrets.kv.v1.create_or_update_secret(
#                     mount_point='lab-creds', path='test-creds', secret=dict(user='devnet'))

# # print(dir(create_response))
# print(create_response.text)

# # Fetch the secret data 
# read_response = client.secrets.kv.v1.read_secret(mount_point='lab-creds', path='test-creds')
# print(read_response['data']['user'])

# # Delete secrets 
# delete_response = client.secrets.kv.v1.delete_secret(mount_point='lab-creds', path='test-creds')
# print(delete_response.text)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# When you use the default mount point of 'secret' with KV version 2     #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# # Create a k/v pair secret under path: secret/test-creds 
# create_response = client.secrets.kv.v2.create_or_update_secret(
#     path='test-creds',
#     secret=dict(username='demouser2', password='demopassword2'),
#     )

# print(json.dumps(create_response, indent=2))

# # Read a secret under path: secret/test-creds 
# read_response = client.secrets.kv.v2.read_secret_version(path='test-creds',)
# print(json.dumps(read_response, indent=2))

# # List of secrets 
# list_response = client.secrets.kv.v2.list_secrets(path='dev-creds',)
# print(json.dumps(list_response, indent=2))

# # Read Secret Metadata
# meta_response = client.secrets.kv.v2.read_secret_metadata(path='dev-creds',)
# print(json.dumps(meta_response, indent=2))

# # Delete secrets along with versions 
# delete_response = client.secrets.kv.v2.delete_secret_versions(path='demo-creds', versions=[1, 2, 3],)
# print(delete_response)

# # Destroy secrets along with versions 
# destroy_response = client.secrets.kv.v2.destroy_secret_versions(path='demo-creds', versions=[1, 2, 3],)
# print(destroy_response)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# When you use the custom mount point of 'dev-creds' with KV version 2   #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# # set the max versions limit for the 'dev-creds' kv secret engine mount point
# secret_engine_config = client.secrets.kv.v2.configure(max_versions=10, mount_point='dev-creds',)
# print(secret_engine_config)

# Read kv secret engine mount point 'dev-creds' configuration
read_secret_engine = client.secrets.kv.v2.read_configuration(mount_point='dev-creds',)
print(read_secret_engine)

# Create a k/v pair secret under path: dev-creds/demo-creds
create_response = client.secrets.kv.v2.create_or_update_secret(
                            mount_point='dev-creds',
                            path='demo-creds',
                            secret=dict(username='demouser', password='demopassword'),
                            )

print(json.dumps(create_response, indent=2))

# Read a secret under path: dev-creds/nxos-creds
read_response = client.secrets.kv.v2.read_secret_version(mount_point='dev-creds', path='demo-creds',)
print(json.dumps(read_response, indent=2))

# # List of secrets - It has issues and need to raise a case
# list_response = client.secrets.kv.v2.list_secrets(mount_point='dev-creds', path='demo-creds',)
# print(list_response)

# Read Secret Metadata
meta_response = client.secrets.kv.v2.read_secret_metadata(mount_point='dev-creds', path='demo-creds',)
print(json.dumps(meta_response, indent=2))

# Delete secrets along with versions 
delete_response = client.secrets.kv.v2.delete_secret_versions(mount_point='dev-creds', path='demo-creds', versions=[1, 2, 3],)
print(delete_response)

# Destroy secrets along with versions 
destroy_response = client.secrets.kv.v2.destroy_secret_versions(mount_point='dev-creds', path='demo-creds', versions=[1, 2, 3],)
print(destroy_response)
