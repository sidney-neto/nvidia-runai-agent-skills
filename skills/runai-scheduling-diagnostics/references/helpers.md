# Packaged deterministic helper

```sh
python scripts/fit.py snapshot.json
```

Run from this installed skill directory, or use its absolute script path.
No offline helper calls a network, cluster, MCP server or credential store.

Consumes captured_at, pagination, pending_request and nodes from local snapshot
v1. pending_request identifies node_pool, gpu_type and 0 < gpu_equivalents <= 1.
Matching nodes provide free_device_gpu_equivalents, each in [0,1]. These are
observed per-device compatible memory-capacity equivalents, never compute speed.

Checks a necessary single-device condition only. Sufficient aggregate capacity
with no individual fit establishes fragmentation within a complete supplied
inventory. Partial data cannot prove global absence of a fit. CPU/memory, taints,
affinity, gang, topology, borrowing and policies are unresolved independently.
Multi-GPU requests require topology-specific analysis outside this helper.
