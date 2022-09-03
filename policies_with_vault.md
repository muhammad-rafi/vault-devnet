
```s
path "secret/*" {
  		capabilities = ["list"]
}
path "secret/data/platform/*" {
  		capabilities = ["read", "list"]
}
```

path "secret/metadata" {
  		capabilities = ["list"]
}

