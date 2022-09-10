
# List of Secrets in default mount point 'secret'
$ curl -k -H "X-Vault-Request: true" -H "X-Vault-Token: $(vault print token)" \
https://localhost:8200/v1/secret/metadata?list=true | jq

$ curl --insecure --header "X-Vault-Token: $VAULT_TOKEN" \
--request GET $VAULT_ADDR/v1/secret/metadata?list=true | jq

# List of Secrets in custom mount point 'dev-creds'
$ curl -k -H "X-Vault-Request: true" -H "X-Vault-Token: $(vault print token)" \
https://localhost:8200/v1/dev-creds/metadata?list=true | jq 

$ curl --insecure --header "X-Vault-Token: $VAULT_TOKEN" \
--request GET $VAULT_ADDR/v1/dev-creds/metadata?list=true | jq

# List of Secrets in default mount point 'secret' and the path 'dnac-secrets'
$ curl --insecure --header "X-Vault-Token: $VAULT_TOKEN" \
$VAULT_ADDR/v1/secret/data/dnac-secrets | jq

# List of Secrets in custom mount point 'dev-creds' and the path 'nxos-creds'
$ curl --insecure --header "X-Vault-Token: $VAULT_TOKEN" \
$VAULT_ADDR/v1/dev-creds/data/nxos-creds | jq

# Enable new KV Secret Engine with new mount point of 'cisco-sandboxes' and get curl output 
$ curl -X POST -H "X-Vault-Request: true" -H "X-Vault-Token: $VAULT_TOKEN" \
-d '{
  "type": "kv",
  "description": "",
  "config": {
    "options": null,
    "default_lease_ttl": "0s",
    "max_lease_ttl": "0s",
    "force_no_cache": false
  },
  "local": false,
  "seal_wrap": false,
  "external_entropy_access": false,
  "options": {
    "version": "2"
  }
}' \
https://localhost:8200/v1/sys/mounts/cisco-sandboxes

