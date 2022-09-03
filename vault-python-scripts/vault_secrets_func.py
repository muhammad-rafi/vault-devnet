import hvac
import os 
import sys
import urllib3
import json

# Disable HTTPS warnings when skipping the TLS 
# urllib3.disable_warnings()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def vault_connect(vault_url, vault_token, cacert):
    """
    Returns an hvac client to communicate with Vault

    :param str vault_url: the vault server url
    :param str vault_token: the vault token
    :param path cacert: the path for the ca cert, pass 'False' to skip TLS verification
    """
    client = hvac.Client(url=vault_url, token=vault_token, verify=cacert)
    return client 

def write_secret(client, path, secrets):
    """
    Returns the infromation when secret is created.

    :param str path: mount point for the secret
    :param dict secrets: dictionary of secrets key values
    """
    
    response = client.secrets.kv.v2.create_or_update_secret(path, secrets)
    return response

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

if __name__ == "__main__":

    cacert = os.environ['VAULT_CACERT']
    vault_token=os.environ['VAULT_TOKEN']
    valut_url = os.environ['VAULT_ADDR']

    # path='hello'
    # secrets=dict(foo="bar")
    
    client = vault_connect(valut_url, vault_token, cacert)
    
    try: 
        client.is_authenticated()
        print("Authentication Sucessful")
    except: 
        print("Authentication Failed !")
        sys.ext(1)

    # write_response = write_secret(client, path, secrets)
    # print(write_response)
    
    # read_response = client.secrets.kv.v1.read_secret(path='lab-creds')
    # print(read_response)

    # response = client.secrets.kv.v1.read_secret(path='lab-creds')
    # response = client.secrets.kv.read_secret_version(path='dev-creds')
    #response = client.secrets.kv.v1.read_secret('lab-creds')
    #print(response)
    


    # # Read the device credentials from the path 'dev-creds/nxos-creds' using kv version 2 
    # response = client.secrets.kv.v2.read_secret_version(mount_point='dev-creds', path='nxos-creds')
    # # print(response)
    
    # username = response['data']['data']['username']
    # password = response['data']['data']['password']
    
    # print(username + "\n" + password)


    # # result = client.secrets.kv.v2.read_secret_version(path='secrets', path='dummy')

    
    # # Read the data written under path: secret/foo
    # read_response = client.secrets.kv.read_secret_version(path='foo')
    # print(read_response)



    