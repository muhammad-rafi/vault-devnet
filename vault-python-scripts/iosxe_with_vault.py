from ensurepip import version
from scrapli.driver.core import IOSXEDriver
from rich import print 
import hvac
import os 

# make sure you have following environmental variable exported
client = hvac.Client(url=os.environ['VAULT_ADDR'],
                    token=os.environ['VAULT_TOKEN'], 
                    verify=os.environ['VAULT_CACERT']
                    )

read_response = client.secrets.kv.v2.read_secret_version(mount_point='cisco-sandboxes', 
                                                         path='iosxe-sandbox', version='2')
host = 'sandbox-iosxe-latest-1.cisco.com'
username = read_response['data']['data']['iosxe_username'] 
password = read_response['data']['data']['iosxe_password'] 

iosxe_sandbox = {
    "host": host,
    "auth_username": username,
    "auth_password": password,
    "auth_strict_key": False,
}

with IOSXEDriver(**iosxe_sandbox) as conn:
    response = conn.send_command("show version")

parse_output = response.textfsm_parse_output()
# print(parse_output)

print(f"""
      HOSTNAME: {parse_output[0]['hostname']}
      OS VERSION: {parse_output[0]['version']}
      SERIAL NO.: {parse_output[0]['serial'][0]}
      UPTIME: {parse_output[0]['uptime_days']} day(s) and {parse_output[0]['uptime_hours']} hours
      """)
