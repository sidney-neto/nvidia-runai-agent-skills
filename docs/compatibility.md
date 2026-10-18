# Compatibility and evidence matrix

Evidence reviewed **2026-10-18**. This is procedure coverage, not a product support
promise or global release allowlist. All reported releases are accepted for
investigation. Match each workflow independently; unknown/newer versions retain
schema validation, arithmetic and evidence analysis. Unverified mutations and
interface-dependent commands remain unavailable until their evidence is found.

| Profile / scope | Documentation reviewed | Synthetic check | Agent evaluation | Live test | Limits |
|---|---|---|---|---|---|
| `fractions-226`: supported-workload YAML limit | Self-Hosted 2.26 dynamic fractions | exact baseline selection | Not run | Not run | Legacy container env ceiling; no automatic patch inheritance |
| `fractions-300`: supported-workload YAML limit | Self-Hosted 3.0 migration | exact baseline selection; older profile excluded | Not run | Not run | Legacy limit env ignored; container annotation required where applicable |
| Component-staged upgrade 2.26 → 3.0 | 3.0 upgrade, backup, matrix, fraction migration | CP-before-cluster; missing prereqs; incompatible K8s | Not run | Not run | No executable upgrade; no inferred historical hop chain |
| MCP read workflow | Self-Hosted 3.0 tools reference and pinned upstream | No live adapter; fallback paths checked | Not run | Not run | Tool schema, usability, permissions and server version require runtime verification |
| Kubernetes scalar reader | kubectl get/JSONPath documented interface | command construction, error handling, output bounds | Not run | Not run | Named pods/nodes only; requires already established kubectl/server compatibility |
| GPU Operator / NIM / vLLM guides | Per-skill exact source tables | Local serving-budget arithmetic only | Not run | Not run | Related-stack versions are independent of Run:ai |
| Local snapshot v1 | Repository-owned contract | validator, quota, health, fit, TLS, serving, redaction | Separate rubric | None needed | Not a Run:ai API schema; no vendor-support claim |

Machine profiles are packaged in
[the readiness skill](../skills/runai-upgrade-readiness/references/profiles.json).
`2.26`, `v2.26` and `2.26.0` normalize to the baseline identity. `2.26.1`, prereleases,
vendor suffixes and development builds do not inherit it. Raw value and origin
are preserved. Numeric components, never lexical string order, drive comparison.
An unambiguous prefix/omitted zero patch is the only normalization made.

The material difference is sourced from
[2.26 dynamic fractions](https://run-ai-docs.nvidia.com/self-hosted/platform-management/runai-scheduler/resource-optimization/dynamic-fractions)
and [3.0 migration](https://docs.nvidia.com/run-ai/self-hosted/v3.0/documentation/installation-and-configuration/upgrade/migrate-gpu-fractions).
`RUNAI_GPU_MEMORY_LIMIT` no longer sets the burst ceiling in 3.0 supported YAML.
The replacement depends on absolute versus proportional memory and the real
container name. Native UI/API/CLI fields are unchanged by that specific rule.
This rule is not applied to all releases or all workload submission paths.

The upgrade fixture represents **component stages**, not invented intermediate
product releases. The reviewed transition is 2.26 baseline to 3.0 baseline.
Source guidance orders control plane before cluster. Kubernetes 1.35/1.36 are
the minor-version intersection of the two published tables; exact distribution,
patches, artifacts and full stack still need checking. The published four-version
policy is not converted into arithmetic or a universal transition graph.

For fractions, the 3.0 migration prerequisite says GPU Operator 26.7.1 or later,
while the reviewed 3.0 support matrix caps its range at 26.7.1. This plan uses
26.7.1 and never promotes later Operator releases based on the minimum alone.
Driver, image CUDA runtime, NRI setting and every GPU node need separate evidence.

The current lifecycle policy applies to Support-Entitled Self-Hosted and its
agreement. Open Source source availability does not create support entitlement;
historical commercial licensing/artifact access must be investigated separately.
The legacy 2.26 alias still calls itself latest: resolve selectors and document
versions, not marketing labels. Multi-Tenant/SaaS needs its own documentation.

Local profiles live in ignored `.local/`. Record observed raw version, component,
scope, provenance, timestamp, exact capability semantics and a bounded source.
They may document a backport or feature flag; they cannot replace observations,
grant access or confer vendor support. Contradictions and multiple matches are
conflicts. Resolve only the affected procedure and continue independent analysis.

States are distinct: advertised, usable and permitted are separate checks;
absent, deprecated, removed, experimental, disabled, unavailable,
permission-denied, unverified and vendor-unsupported are not synonyms. Missing
permission proves nothing about feature existence. End of support does not stop
offline evidence analysis.

Before concrete changes run an opt-in freshness check and review affected
volatile sources. Offline output must cite evidence date and unresolved refresh
requirements. A changed hash or redirect reports a review need; it never changes
profiles automatically. See [sources.json](sources.json) and each packaged source
table for exact URLs and documentation identities.
