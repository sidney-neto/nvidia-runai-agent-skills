# Packaged deterministic helper

```sh
python scripts/tls_evidence.py tls-evidence.json
```

Run from this installed skill directory, or use its absolute script path.
No offline helper calls a network, cluster, MCP server or credential store.

Input object: administrator_tls_verified and application_tls_verified are
boolean or null; application_error is optional sanitized evidence. Reports
application trust as unverified unless its own evidence is true. It never opens
a TLS connection or enters a container. A TLS success does not establish OIDC
userinfo authentication, authorization, audience, issuer, proxy or routing.
Compare the actual ingress-served chain/SNI/hostname and application CA bundle,
not merely the certificate uploaded to an ingress object. Keep certificate
public data separate from private keys. Retesting inside a container requires
separate authorization and an established image/tool interface.
