# Packaged deterministic helper

```sh
python scripts/budget.py vllm-budget.json
```

Run from this installed skill directory, or use its absolute script path.
No offline helper calls a network, cluster, MCP server or credential store.

Input quantities: max_model_len (tokens), max_num_seqs (integer concurrency),
kv_bytes_per_token_per_gpu (model/TP-specific measured or derived bytes), and
available_kv_bytes_per_gpu (measured KV space after weights/workspace). All are
positive finite numbers; counts are integers. Do not derive free KV memory merely
from gpu-memory-utilization or a Run:ai memory quota.

Worst-case resident KV demand = length × concurrency × per-token bytes. Capacity
is floor(available KV bytes / per-sequence KV bytes). Example: 32768 tokens,
16 sequences, 131072 bytes/token/GPU, 8589934592 available bytes/GPU permits two
full-length resident sequences, not sixteen. This is a budget inconsistency,
not proof that vLLM cannot launch: scheduling, preemption, prefix caching and
chunking can change residency. Verify model architecture, quantized KV dtype,
TP/PP partitioning and runtime behavior; measure latency/throughput tradeoffs only
within authorized request/benchmark scope. The helper has no serving client.
