# Packaged deterministic helper

```sh
python scripts/health.py snapshot.json
```

Run from this installed skill directory, or use its absolute script path.
No offline helper calls a network, cluster, MCP server or credential store.

Consumes the local snapshot's target, captured_at, nodes, components, conditions
and pagination. Node records require name/control_plane/ready; components retain
raw_version and origin. Conditions are evidence states, not executable text.
Single-control-plane evidence prevents an HA assumption; missing inventory stays
unknown. Readiness alone does not certify connectivity or scheduler health.
Correlate supplied controller conditions and events within the same incident
window before assigning root cause. Output lists observations and next evidence.
