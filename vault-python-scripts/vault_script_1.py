import hvac
import os 

# # Authentication without TLS 
# client = hvac.Client(url='http://localhost:8200', token=os.environ['VAULT_TOKEN'])
# print(client.is_authenticated())

# # Authentication with TLS with Client and Server Certs
# client = hvac.Client(
#     url='https://localhost:8200',
#     token=os.environ['VAULT_TOKEN'],
#     cert=("/opt/vault/tls/tls.crt", "/opt/vault/tls/tls.key"),
#     verify="/opt/vault/tls/tls-server.crt",
# )
# print(client.is_authenticated())

# # Authentication with TLS but skip verification
# client = hvac.Client(
#     url='https://127.0.0.1:8200',
#     token=os.environ['VAULT_TOKEN'],
#     verify=False
# )
# print(f"Vault Authenticated: {client.is_authenticated()}")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# def create_client(**kwargs):
#     return client(url='https://localhost:8200',
#                   cert=('test/client-cert.pem', 'test/client-key.pem'),
#                   verify='test/server-cert.pem',
#                   **kwargs)


# cacert = "self-signed.crt"
# cert=("self-signed.crt", "self-signed.key")

# client = hvac.Client(url="https://127.0.0.1:8200", token="s.Kqk7fRyUT3yI9hR1PStitRkJ", verify=cacert, cert=cert)
client = hvac.Client(url="https://127.0.0.1:8200", token="s.Kqk7fRyUT3yI9hR1PStitRkJ", verify=False)

try: 
    client.is_authenticated()
    print("Authenticated")
except: 
    print("Not Authenticated")

read_response = client.secrets.kv.v1.read_secret(path='lab-creds')
print(read_response)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

