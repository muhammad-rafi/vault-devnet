import hvac
import os
import sys

# Reference: https://hvac.readthedocs.io/en/stable/overview.html#initialize-the-client

shares = 5
threshold = 3
ca_cert = os.environ['VAULT_CACERT'] # set CA cert path as an env variable.

# Authentication with TLS using CA Cert
client = hvac.Client(
    url='https://localhost:8200',
    verify=ca_cert
)

print(f"Authentication Successful: {client.is_authenticated()}")

try: 
    # check if Vault is initialized
    vault_init = client.sys.is_initialized()
    if vault_init == True:
        print("Vault has already been Initialized.")
    elif vault_init == False:
        result = client.sys.initialize(shares, threshold)
        root_token = result['root_token']
        keys = result['keys']
        print(f"(Vault Initialization: {client.sys.is_initialized()}")

        # set the root token
        client.token = root_token

    # check if Vault is sealed
    vault_sealed = client.sys.is_sealed()
    if vault_sealed == False:
        print("Vault has already been unsealed.")
        sys.exit(1)
    elif vault_sealed == True:
        # Unseal a Vault cluster with individual keys
        unseal_response1 = client.sys.submit_unseal_key(keys[0])
        unseal_response2 = client.sys.submit_unseal_key(keys[1])
        unseal_response3 = client.sys.submit_unseal_key(keys[2])

        print(f"(Is Vault sealed: {client.sys.is_sealed()}")
except Exception as error:
    print(error)
    