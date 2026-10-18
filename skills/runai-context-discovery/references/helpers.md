# Packaged deterministic helper

```sh
python scripts/snapshot.py snapshot.json
```

Run from this installed skill directory, or use its absolute script path.
No offline helper calls a network, cluster, MCP server or credential store.

Validate `assets/snapshot.schema.json` (our local contract, not a Run:ai API). Install
`requirements.txt` in the helper's Python environment before going offline. The
input limit is 2 MB. Unknown fields and negative quantities fail without echoing
input. Raw versions and origin remain intact; derived version states are
round-trip valid. Missing versions are not a schema failure.

Required top-level fields: schema_version=1, captured_at (UTC timestamp), target
(cluster/context/deployment/edition), components, nodes, quotas and pagination.
Optional conditions and pending_request support focused analysis. Empty lists
are allowed and must be labeled incomplete when inventory is unknown. Numeric
GPU-equivalents and physical device counts are distinct. Components preserve
name/raw_version/origin and optional node; no complete inventory is required.

An example is packaged at `assets/example.snapshot.json`. Names/versions are
synthetic and imply no hardware or vendor-support requirement.

The separate live helper `scripts/collect.py --context example-context --namespace
example-project --pod example-pod --node example-node` accepts at most twenty
explicit targets. It uses documented kubectl get JSONPath output with a 15-second
request timeout, 20-second process deadline and 8 KiB combined output limit per
field. It emits phase, kubelet/runtime version and allocatable nvidia.com/gpu only.
The latter is a Kubernetes resource count, not physical GPU count or automatically
a GPU-equivalent. The adapter returns field/state/value evidence, not a completed
snapshot. Manually map values with their provenance; supply unknown fields as
unknown, never infer quotas or physical devices from logical resource counts.

Requires read/get permission on only those named pods (namespace scoped) and
nodes (cluster scoped); kubectl uses its configured verified TLS transport.
**JSONPath is client-side:** kubectl retrieves full named objects internally;
only projected scalar output enters this helper. No Secret resource, raw object,
container environment, log, kubeconfig or stderr is retained. If full-object
retrieval is outside scope, use an approved sanitized export instead. Offline
snapshot validation never imports or instantiates the live collector.
