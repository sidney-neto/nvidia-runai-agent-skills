# Packaged deterministic helper

```sh
python scripts/quota.py snapshot.json --format json
```

Run from this installed skill directory, or use its absolute script path.
No offline helper calls a network, cluster, MCP server or credential store.

Input is local snapshot v1 with captured_at, target.cluster, nodes, quotas and
pagination. Nodes require unique name, node_pool, gpu_type, physical_gpus and
allocatable_gpu_equivalents. Quotas require scope (project/department), id,
node_pool, gpu_type, quota and allocated; parent_id is optional metadata. Quota
is a finite nonnegative GPU-equivalent number, "unlimited", or null (unknown).
Allocated is a nonnegative number or null. Keep the same capture window.

The helper rejects duplicate nodes/quotas rather than double-counting pages.
Merge pages explicitly, with pagination.complete/pages/expected_pages. Partial
pool inventory cannot prove complete capacity. Unknown and unlimited quotas
prevent a negative oversubscription verdict; a known subtotal above complete
capacity still proves configured oversubscription. Departments remain separate
from child projects. Results partition cluster/pool/GPU type and retain physical,
allocatable, entitlement and allocation quantities separately. No activity or
GPU-memory usage is inferred. `--format text` prints the same summary for humans.

Trend review requires comparable timestamped snapshots and complete scope at
each point; do not infer trends from one capture. A recommendation includes the
current quota, proposed quota, affected pool, borrowing implications and workload
owner review. No low-utilization finding authorizes preemption or termination.
