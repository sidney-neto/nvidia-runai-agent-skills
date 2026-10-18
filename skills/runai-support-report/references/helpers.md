# Packaged deterministic helper

```sh
python scripts/report.py incident.json
```

Run from this installed skill directory, or use its absolute script path.
No offline helper calls a network, cluster, MCP server or credential store.

Allowlisted fields: scope, captured_at, versions, findings, evidence, hypotheses,
attempted_actions and remaining_questions. Scope, timestamp and findings are
required. The input limit is 2 MB; unknown top-level fields are rejected. Input
must already be minimized. Raw log bundles and arbitrary Kubernetes objects are
not supported inputs.

Before emitting JSON, recursively redact credential-key values, bearer/basic
credentials, common inline/quoted assignments, PEM private keys, URL userinfo,
IPv4 addresses and internal/local/corp hostnames. No unredacted report artifact is
written. Human review remains required for organization identifiers, IPv6,
unknown credential formats and contextual secrets. Do not promise exhaustive
redaction. The JSON separates findings/evidence/hypotheses/actions/questions so
an executive summary and technical chronology can be generated without copying
raw secrets. Record original evidence timestamps and hypotheses explicitly.
