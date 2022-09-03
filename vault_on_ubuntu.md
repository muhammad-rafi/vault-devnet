## Install HashiCorp Vault on Ubuntu 20.04

### Download the Vault version 1.8.7 via `wget`, it will download the `.zip` file in your current directory
```bash
$ wget https://releases.hashicorp.com/vault/1.8.7/vault_1.8.7_linux_amd64.zip
```

### Unzip the .zip archive file you downloaded in previous step
```bash
$ unzip vault_1.8.7_linux_amd64.zip
```

### Move the file unzip file `unzip` from your current directory to /usr/bin
```bash
$ mv vault /usr/bin
```

### Create directories for the Hashicorp Vault Configuration, Data, TLS certs and Log
```bash
$ sudo mkdir /etc/vault 
$ sudo mkdir -p /opt/vault/{tls,data}
$ sudo mkdir -p /var/log/vault
```

### Create Vault Configuration file inside `/etc/vault` directory and name the file as `vault.hcl` or `config.hcl`

```bash
$ cd /etc/vault 
$ touch vault.hcl
$ cat vault.hcl

# Enables the built-in web UI
ui = true

# Disables all caches within Vault
disable_cache = true

# Disables the server from executing the mlock
disable_mlock = true

# Configures how Vault is listening for API requests, HTTP or HTTPS
# HTTP & HTTPS listener
listener "tcp" {
  address       = "127.0.0.1:8200"
  tls_disable   = 1 # or "true"
  # tls_disable   = 0 # or "false" 
  # tls_cert_file = "/opt/vault/tls/tls.crt"
  # tls_key_file  = "/opt/vault/tls/tls.key"
}

# Configures the storage backend where Vault data is stored, local or consul
storage "file" {
  path = "/opt/vault/data"
}

# Specifies the address (full URL) to advertise to other Vault servers in the cluster for client redirection
api_addr                = "http://127.0.0.1:8200"

# Specifies the maximum possible lease duration for tokens and secrets
max_lease_ttl           = "5h"

# Specifies the default lease duration for tokens and secrets, value cannot be larger than max_lease_ttl
default_lease_ttl       = "5h"
```
Full configuration options can be found at https://www.vaultproject.io/docs/configuration

Notice, I have disabled the TLS in the above config as this is only for demo purpose, however it is not recommended in the production environment. Therefore, make sure you have TLS enabled and you access the Vault via HTTPS with signed certificates by legitimate CA.

### Create Hashicorp Vault Service File `vault.service` and place this file in the services directory `/etc/systemd/system`

``` bash
[Unit]
Description="HashiCorp Vault - A tool for managing secrets"
Documentation=https://www.vaultproject.io/docs/
Requires=network-online.target
After=network-online.target
ConditionFileNotEmpty=/etc/vault/vault.hcl

[Service]
ProtectSystem=full
ProtectHome=read-only
PrivateTmp=yes
PrivateDevices=yes
SecureBits=keep-caps
AmbientCapabilities=CAP_IPC_LOCK
NoNewPrivileges=yes
ExecStart=/usr/bin/vault server -config=/etc/vault/vault.hcl
ExecReload=/bin/kill --signal HUP 
KillMode=process
KillSignal=SIGINT
Restart=on-failure
RestartSec=5
TimeoutStopSec=30
StartLimitBurst=3
LimitNOFILE=6553

[Install]
WantedBy=multi-user.target
```

### Enable and Start and Vault Service

```bash
$ systemctl daemon-reload
$ systemctl start vault.service
$ systemctl enable vault.service
$ systemctl status vault.service
```

### Connect to the HashiCorp Vault Web UI 
Go to your favourite browser, type http://127.0.0.1:8200 and initlize the vault. To see the intialization process, please refer to main [README](README.md) file.


## Install HashiCorp Vault on Ubuntu 20.04 with TLS enabled (Self-Signed Certificates)

To enable the TLS on your vault server, the process will be same as above except with these few changes below. 

- Generate self-signed CA certificate and the key.
- Export environment variable with `https`.
- Edit `vault.hcl` or `config.hcl` disable the `http` section and enable `https` section.
- Restart the vault server. 

### Generate self-signed CA certificate and the key

To enable the HTTPS, you first need to generate .cert and .key (or .pem) files by using following command and place them to the "/opt/vault/tls/" directory which we created in earlier steps above if you have not created this directory, you can create now.  

I have mentioned three methods to create self-singed certificate, you can choose whichever you like.

*METHOD_1: To generate the self-signed certificate with prompts*

```bash
$ sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /opt/vault/tls/selfsigned-client.key -out /opt/vault/tls/selfsigned-client.crt
```

*METHOD_2: To generate the self-signed certificate with no prompts*
```bash
openssl req -out ca-cert.crt -new -keyout ca-key.key -newkey rsa:2048 -nodes -sha256 -x509 -subj "/O=HashiCorp/CN=Vault" -addext "subjectAltName=IP:127.0.0.1,DNS:localhost" -days 365
```

*METHOD_3: To generate the self-signed certificate using the `.conf` file and `.pem` extension*

```bash
$ openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ca-key.pem -out ca-cert.pem -config ssl.conf
```

`$ cat ssl.conf`

```s
[req]
distinguished_name = req_distinguished_name
req_extensions = v3_req
prompt = no

[req_distinguished_name]
countryName                 = GB
stateOrProvinceName         = England
localityName                = Birmingham
organizationName            = DevnetBro
commonName                  = localhost

[v3_req]
subjectAltName = @alt_names

[alt_names]
IP.1 = 127.0.0.1
DNS.1   = localhost
```
__Note: I have set the parameters as I needed, but you can choose your own parameter values as you require.__

*To check the certificate information in human readable format*
```s
$ sudo openssl x509 -in /opt/vault/tls/ca-cert.crt -noout -text
```

*change the ownership of the TLS certificate to `vault`*
```s
$ sudo chown vault: /opt/vault/tls/*
```

### Export environment variable with `https`.

You need to set below environment variable with `https`

```s
export VAULT_ADDR=<your-vault-server-ip-or-dns>
export VAULT_API_ADDR=<your-vault-server-ip-or-dns>
export VAULT_CACERT=<path_to_cacert>
export VAULT_SKIP_VERIFY=false # this should be a default, unless you changed it to `true` before.
```

examples:
```s
$ export VAULT_ADDR='https://localhost:8200'
$ export VAULT_API_ADDR='https://127.0.0.1:8200'
$ export VAULT_CACERT="/opt/vault/tls/ca-cert.crt"
$ export VAULT_SKIP_VERIFY=false
```

__Note: If you don't export the VAULT_CACERT env variable, you will need to run the commands like below.__

```s
$ vault status -ca-cert="/opt/vault/tls/ca-cert.crt"
```

### Edit `vault.hcl` or `config.hcl`

*Enbale the HTTPS section in the `config.hcl` or `vault.hcl` file and disable HTTP.*
```s
# HTTPS listener
listener "tcp" {
  address       = "0.0.0.0:8200"
  tls_disable   = false
  tls_cert_file = "/opt/vault/tls/ca-cert.crt"
  tls_key_file  = "/opt/vault/tls/ca-key.key"
}
```

### Restart the Vault Server 

*Restart the Vault service and check the status.*
```s
$ systemctl restart vault.service
$ systemctl status vault.service
```

##### NOTE: if you have enabled Vault with self-signed certificate and like to skip the TLS verification, then you have to run the command like below; e.g. check the vault status and try login to vault.

*If you like to skip the TLS verifcation*
```s
$ vault status -tls-skip-verify
$ vault login -tls-skip-verify
```

*or you can export the environment variable* 
`export VAULT_SKIP_VERIFY=true`

There is also currently a bug for this `VAULT_SKIP_VERIFY` as it doesn't work as expected, checkout [link](https://github.com/hashicorp/vault/issues/14316) as I have been caught by this bug as well.

__This is only for lab or testing environment, however you should use proper signed certifcates in the production environment.__

