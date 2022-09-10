import hvac
import os 
import sys
import urllib3
import json
from rich import print

# Disable HTTPS warnings when skipping the TLS 
urllib3.disable_warnings()

'''
This script is using default mount point of 'secret' and CA cert for TLS 
with KV version 2, however you can pass custom mount in other functions
and you can also either skip TLS verification by not passing the 'verify' 
attribute into a 'vault_connect' fuction call.
'''

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def vault_connect(vault_url, vault_token, verify=False):
    """
    Returns an hvac client to communicate with Vault

    :param str vault_url: the vault server url
    :param str vault_token: the vault token
    :param str verify: path as a string for the ca cert, 
    or skip 'verify' attr to skip TLS verification
    """
    client = hvac.Client(url=vault_url, 
                         token=vault_token, 
                         verify=verify)
    return client 


def create_kv2_secret_engine(client, max_ver, mount_point):
    """
    Creates new KV secret engine with mount point name provided.

    :param hvac_client client: client to connect with Vault
    :param max_ver int: maximum versions of secret can be created 
    :param str mount_point: custom mount point to be created
    """
    
    # need to correct this, please ignore for now.
    # response = client.secrets.kv.v2.configure(max_versions=max_ver, mount_point=mount_point,)
    # return response
    pass

def read_kv2_secret(client, path, mount_point=None):
    """
    Returns the infromation for the secrets for the path provided.

    :param str path: mount point for the secret
    :param str mount_point: uses default 'secret' unless custom mount point is provided
    """

    if mount_point:
        response = client.secrets.kv.v2.read_secret_version(mount_point, path)
        return response
    else: 
        response = client.secrets.kv.v2.read_secret_version(path)
        return response


def create_kv2_secret(client, path, secrets, mount_point=None):
    """
    Returns the infromation when secret is created or updated.

    :param str path: mount point for the secret
    :param dict secrets: dictionary of secrets key values
    :param str mount_point: uses default 'secret' unless custom mount point is provided
    """

    if mount_point:
        response = client.secrets.kv.v2.create_or_update_secret(mount_point, path, secrets)
        return response
    else: 
        response = client.secrets.kv.v2.create_or_update_secret(path, secrets)
        return response
    

def patch_kv2_secret(client, path, secrets, mount_point=None):
    """
    Returns the infromation when another secret is added to same path.

    :param str path: mount point for the secret
    :param dict secrets: dictionary of secrets key values
    :param str mount_point: uses default 'secret' unless custom mount point is provided
    """

    if mount_point:
        response = client.secrets.kv.v2.patch(mount_point, path, secrets)
        return response
    else: 
        response = client.secrets.kv.v2.patch(path, secrets)
        return response  

def list_kv2_secret():
    pass


def delete_kv2_secret():
    pass


def undelete_kv2_secret():
    pass


def destroy_kv2_secret():
    pass


def list_kv2_secret():
    pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

if __name__ == "__main__":

    cacert = os.environ['VAULT_CACERT']
    vault_token=os.environ['VAULT_TOKEN']
    valut_url = os.environ['VAULT_ADDR']

    path='hello'
    secrets=dict(foo="bar")
    patch_secret=dict(baz="baz")
    
    client = vault_connect(valut_url, vault_token, verify=cacert)
    
    try: 
        client.is_authenticated()
        print(f"Authentication Sucessful: {client.is_authenticated()}")
    except: 
        print(f"Authentication Sucessful: {client.is_authenticated()}")
        sys.ext(1)

    # Create or update a secret
    if client.is_authenticated() == True:
        create_response = create_kv2_secret(client, path, secrets)
        print(f"Secret has been sucessfully created under the path: '{path}'")
        print(json.dumps(create_response, indent=2))

    # Add another secret to same path
    if client.is_authenticated() == True:
        patch_response = patch_kv2_secret(client, path, patch_secret)
        print(f"Secret has been sucessfully created under the path: '{path}'")
        print(json.dumps(patch_response, indent=2))

    # Read secrets from the specific path
    if client.is_authenticated() == True:
        patch_response = read_kv2_secret(client, path)
        print(json.dumps(patch_response, indent=2))
    
        # username = response['data']['data']['username']
        # password = response['data']['data']['password']




    