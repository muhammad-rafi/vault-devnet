import hvac
import os 
import urllib3

# Disable HTTPS warnings when skipping the TLS 
urllib3.disable_warnings()

# Different way to create hvac client
# client = hvac.Client(url="https://localhost:8200")
# client = hvac.Client(url="https://localhost:8200", token=None)
# client = hvac.Client(url="https://localhost:8200", token="vault_token", verify=cacert, cert=cert)
# client = hvac.Client(url="https://localhost:8200", token="vault_token", verify=cacert)
# client = hvac.Client(url="https://localhost:8200", token="vault_token", verify=True)

# Set variables from the environment variables 
# cacert = os.environ['VAULT_CACERT']
# vault_token=os.environ['VAULT_TOKEN']
# valut_url = os.environ['VAULT_ADDR']

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Authentication without TLS - Using plaintext / HTTP
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

client = hvac.Client(url='http://localhost:8200', token=os.environ['VAULT_TOKEN'])
print(f"Authentication Successful: {client.is_authenticated()}")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Authentication with TLS using CA and Client Certs
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

client = hvac.Client(
    url='https://localhost:8200',
    token=os.environ['VAULT_TOKEN'],
    cert=("/opt/vault/tls/client-cert.pem", "/opt/vault/tls/client-key.pem"),
    verify="/opt/vault/tls/ca-cert.pem"
)

print(f"Authentication Successful: {client.is_authenticated()}")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Authentication with TLS using CA Cert
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

client = hvac.Client(
    url='https://localhost:8200',
    token=os.environ['VAULT_TOKEN'],
    verify="/opt/vault/tls/ca-cert.pem"
)

print(f"Authentication Successful: {client.is_authenticated()}")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Authentication with TLS but skip verification
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

client = hvac.Client(
    url='https://127.0.0.1:8200',
    token=os.environ['VAULT_TOKEN'],
    verify=False
)

print(f"Authentication Successful: {client.is_authenticated()}")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Authentication using Functions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def vault_connect(vault_url, vault_token=None):
    """
    Returns an hvac client to communicate with Vault

    :param str vault_url: the vault server url
    :param str vault_token: the vault token
    """
    client = hvac.Client(url=vault_url, token=vault_token)
    return client 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def vault_connect_cacert(vault_url, vault_token, cacert):
    """
    Returns an hvac client to communicate with Vault

    :param str vault_url: the vault server url
    :param str vault_token: the vault token
    :param path cacert: the path for the ca cert, pass 'False' to skip TLS verification
    """
    client = hvac.Client(url=vault_url, token=vault_token, verify=cacert)
    return client 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def vault_client(params):
    url = params.get('url')
    ca_cert = params.get('ca_cert')
    ca_path = params.get('ca_path')
    client_cert = params.get('client_cert')
    client_key = params.get('client_key')
    cert = (client_cert, client_key)
    check_verify = params.get('verify')
    namespace = params.get('namespace', None)
    if check_verify == '' or check_verify:
        if ca_cert:
            verify = ca_cert
        elif ca_path:
            verify = ca_path
        else:
            verify = check_verify
    else:
        verify = check_verify
    client = hvac.Client(url=url, cert=cert, verify=verify, namespace=namespace)
    return client 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def vaultclient(**kwargs):
    client(url='https://localhost:8200',
                cert=('test/client-cert.pem', 'test/client-key.pem'),
                verify='test/server-cert.pem',
                **kwargs)
    return client
