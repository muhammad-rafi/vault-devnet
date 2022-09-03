import hvac
import os 
import json

cacert = os.environ['VAULT_CACERT']
vault_token=os.environ['VAULT_TOKEN']
vault_url = os.environ['VAULT_ADDR']

client = hvac.Client(
            url=vault_url, 
            token=vault_token, 
            verify=cacert,
            )

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# When you use the default mount point of 'secret' with KV version 2     #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# Write a k/v pair secret under path: secret/test-creds
write_response = client.secrets.kv.v2.create_or_update_secret(
    path='test-creds',
    secret=dict(username='demouser', password='demopassword'),
    )

print(json.dumps(write_response, indent=2))

# Read a secret under path: secret/test-creds
read_response = client.secrets.kv.v2.read_secret_version(path='test-creds',)
print(json.dumps(read_response, indent=2))


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# When you use the custom mount point of 'dev-creds' with KV version 2   #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# Write a k/v pair secret under path: dev-creds/demo-creds
write_response = client.secrets.kv.v2.create_or_update_secret(
                            mount_point='dev-creds',
                            path='demo-creds',
                            secret=dict(username='demouser', password='demopassword'),
                            )

print(json.dumps(write_response, indent=2))

# Read a secret under path: dev-creds/demo-creds
read_response = client.secrets.kv.v2.read_secret_version(mount_point='dev-creds', path='nxos-creds',)
print(json.dumps(read_response, indent=2))
    