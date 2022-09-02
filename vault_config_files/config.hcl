# Enables the built-in web UI
ui = true

# Disables all caches within Vault
disable_cache = true

# Disables the server from executing the mlock
disable_mlock = true

# Configures how Vault is listening for API requests, HTTP or HTTPS
# HTTP listener
# listener "tcp" {
#  address = "127.0.0.1:8200"
#  tls_disable = 1
# }

# HTTPS listener
listener "tcp" {
  address       = "0.0.0.0:8200"
  tls_disable = "true"
#   tls_cert_file = "/opt/vault/tls/tls.crt"
#   tls_key_file  = "/opt/vault/tls/tls.key"
}

# Configures the storage backend where Vault data is stored, local or consul
storage "file" {
  path = "/opt/vault/data"
}

# storage "consul" {
#  address = "127.0.0.1:8500"
#  path    = "vault"
# }

# Specifies the telemetry reporting system
# telemetry {
#   statsite_address = "127.0.0.1:8125"
#   disable_hostname = true
# }

# Specifies the address (full URL) to advertise to other Vault servers in the cluster for client redirection
api_addr                = "http://127.0.0.1:8200"

# Specifies the maximum possible lease duration for tokens and secrets
max_lease_ttl           = "5h"

# Specifies the default lease duration for tokens and secrets, value cannot be larger than max_lease_ttl
default_lease_ttl       = "5h"

# Specifies the identifier for the Vault cluster
# cluster_name            = "vault"

# Enables the sys/raw endpoint which allows the decryption/encryption of raw data
# raw_storage_endpoint    = true

# Disables using seal wrapping for any value except the root key
# disable_sealwrap        = true

# Example AWS KMS auto unseal
# seal "awskms" {
#  region = "us-east-1"
#  kms_key_id = "REPLACE-ME"
# }

# Enterprise license_path
# This will be required for enterprise as of v1.8
# license_path = "/etc/vault.d/vault.hclic"

# Example HSM auto unseal
# seal "pkcs11" {
#  lib            = "/usr/vault/lib/libCryptoki2_64.so"
#  slot           = "0"
#  pin            = "AAAA-BBBB-CCCC-DDDD"
#  key_label      = "vault-hsm-key"
#  hmac_key_label = "vault-hsm-hmac-key"
# }