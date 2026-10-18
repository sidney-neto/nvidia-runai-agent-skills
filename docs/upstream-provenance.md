# Run:ai release and upstream skill research

Reviewed 2026-10-18. Research only; no repository files or installations changed.

## Recommended bounded families

Use **Self-Hosted 2.26** and **Self-Hosted 3.0** as the two reviewed documentation families. These are procedural evidence labels, not a claim that every patch, MCP tool, installation variant, or future release is supported.

The [NVIDIA entry point](https://docs.nvidia.com/run-ai/) redirects to `/run-ai/self-hosted/documentation/home` and labels its content v3.0. Its [v2.26 selector](https://docs.nvidia.com/run-ai/self-hosted/v2.26/documentation/archived-documentation) redirects to `https://run-ai-docs.nvidia.com/self-hosted`; [v2.25](https://docs.nvidia.com/run-ai/self-hosted/v2.25/documentation/archived-documentation) redirects to `/self-hosted/2.25`. The legacy [lifecycle page](https://run-ai-docs.nvidia.com/self-hosted/support-policy/product-version-life-cycle) still calls 2.26 latest, so never treat that alias as the global latest release. The JSON records requested/final URLs and version provenance.

## Material differences to encode

1. **Fraction limits:** [2.26 Dynamic GPU Fractions](https://run-ai-docs.nvidia.com/self-hosted/platform-management/runai-scheduler/resource-optimization/dynamic-fractions) uses `gpu-fraction` or `gpu-memory` pod requests plus container environment variable `RUNAI_GPU_MEMORY_LIMIT`. In [3.0 migration](https://docs.nvidia.com/run-ai/self-hosted/documentation/installation-and-configuration/upgrade/migrate-gpu-fractions), supported-workload YAML replaces that environment variable with `nvidia.com/container.<container>.gpu-memory.limit` for absolute memory or `kai.scheduler/container.<container>.gpu-memory.portion.limit` for a portion. The old variable is silently ignored, removing the burst ceiling. Native UI/API/CLI fields stay unchanged. Request-only manifests need no limit migration.
2. **Quota API field:** [3.0 removals](https://docs.nvidia.com/run-ai/self-hosted/documentation/getting-started/whats-new/deprecation-notifications) explicitly removes project/department `resources[].priority`: responses omit it and requests using it fail; use `rank`. This is a stronger task-specific release gate than blindly assuming API fields persist.
3. **Installation identity:** [3.0 release notes](https://docs.nvidia.com/run-ai/self-hosted/documentation/getting-started/whats-new/whats-new-3-0) replaces `controlPlane.clientSecret` with `controlPlane.bootstrapToken`. The generated token lasts two hours; 3.0 control planes no longer return `clientSecret`.
4. **Removed behavior:** 3.0 disables node-level scheduling and GPU memory swap. Older quota/swap explanations cannot be used as 3.0 operating instructions. See the removals source above.

## Concrete upgrade stages and prerequisites

The reviewed transition is **2.26 → 3.0**. [3.0 Upgrade](https://docs.nvidia.com/run-ai/self-hosted/documentation/installation-and-configuration/upgrade/upgrade-nvidia-run-ai) expressly distinguishes upgrades from 2.26 or earlier. It does not establish a mandatory stop at 2.26 for all older installations.

Stage 0: record exact control-plane, cluster, CLI, distribution, GPU stack, workload types and edition. [Plan the Upgrade](https://docs.nvidia.com/run-ai/self-hosted/documentation/installation-and-configuration/upgrade/plan-the-upgrade) permits at most four versions per hop, requires a successful stage before the next, and requires target-compatible Kubernetes/OpenShift before Run:ai. Its table gives 2.26: Kubernetes 1.34–1.36 / OpenShift 4.18–4.22; 3.0: Kubernetes 1.35–1.37 / OpenShift 4.20–4.22. Choose exact distribution versions from the table; do not invent supported intermediate patches.

Stage 1: [back up](https://docs.nvidia.com/run-ai/self-hosted/documentation/installation-and-configuration/upgrade/back-up-before-upgrading) cluster Helm values and runtime `runaiconfig`, control-plane values, database, and metrics storage. Retain artifacts outside the affected deployment. Native fractional workloads must be suspended; supported fractional workloads deleted while retaining manifests. Migrate applicable manifests before resubmission.

Stage 2: fractions require CUDA 13.4+, driver r615+ on every GPU node, GPU Operator 26.7.1+, and `cdi.nriPluginEnabled=false`. Explicitly set the driver version. The [3.0 support matrix](https://docs.nvidia.com/run-ai/self-hosted/documentation/installation-and-configuration/support-matrix) caps GPU Operator at 26.7.1; use 26.7.1 for this reviewed plan, not an unsupported open-ended “or later” range. The migration procedure permits GPU stack first or Run:ai first; the latter leaves fractions unavailable until the stack meets requirements.

Stage 3: manually upgrade **control plane 2.26 → 3.0**, verify success, then **cluster 2.26 → 3.0**, verify Connected state and expected version. The documented ordering is control plane first, cluster second. Helm minimum is 3.14; Guided Installation cannot upgrade. NGC replaces JFrog. Select OSS versus Support-Entitled instructions: the latter introduces explicit `supportEntitled`, telemetry, and image-pull-secret settings. Do not add entitlement settings to an OSS plan.

Stage 4: align CLI with cluster. Resubmit fractional workloads and verify enforced ceilings, not only Running state. Native suspended fractional workloads need a differently named copy/resubmission; verify replacement before deleting originals. Legacy native workloads may need resubmission for restored capabilities.

No primary source was found requiring a synthetic chain such as 2.24 → 2.26 → 3.0. For an older starting version, gather its exact archived prerequisites and applicable lifecycle evidence before generating hops; the four-version policy alone is not a certified migration graph.

## Edition and lifecycle limits

The [3.0 lifecycle policy](https://docs.nvidia.com/run-ai/self-hosted/documentation/getting-started/support-lifecycle-and-deprecation-policy) is for **Support-Entitled Self-Hosted**, with the applicable agreement governing support. Its stated compatibility rule is control plane ≥ cluster and CLI = cluster. It lists 2.26 release/full-support-end/extended-end as 2026-07-12 / 2027-04-12 / 2027-07-12; 3.0 as 2026-10-13 / 2027-07-13 / 2027-10-13. Do not extend this enterprise entitlement to OSS or SaaS.

## Upstream review and decision

Pin: `dsx-ai-factory/run-ai@8190247dc97cd67538e8d4ab383d13b22da5037b` (commit timestamp 2026-10-18T12:12:13Z). Both SKILL.md files, both linked references, and skills/LICENSE were fetched at that revision; JSON contains SHA-256 checksums and local snapshots. Official [3.0 Agent Skills](https://docs.nvidia.com/run-ai/self-hosted/documentation/agents/agent-skills) links these two read workflows and requires Run:ai MCP. It does not certify their current MCP contracts on 2.26.

- [runai-diagnose-failed-workload](https://github.com/dsx-ai-factory/run-ai/blob/8190247dc97cd67538e8d4ab383d13b22da5037b/skills/runai-diagnose-failed-workload/SKILL.md): **adapt**, preserving its read-only evidence order, exact cluster/workload resolution, preemption routing, and UNKNOWN result on insufficient evidence. It requires MCP and only optionally Kubernetes. Extend with bounded version evidence and an offline evidence fallback if the new skill needs those; do not silently claim its tool names exist on older servers.
- [runai-audit-assigned-quota](https://github.com/dsx-ai-factory/run-ai/blob/8190247dc97cd67538e8d4ab383d13b22da5037b/skills/runai-audit-assigned-quota/SKILL.md): **adapt/extend**, preserving same-pool capacity evidence, legitimate borrowing, pending-reason checks, and separation of oversubscription from borrowing. Its [quota reference](https://github.com/dsx-ai-factory/run-ai/blob/8190247dc97cd67538e8d4ab383d13b22da5037b/skills/runai-audit-assigned-quota/references/quota-accounting.md) ends with an open-item claim that `nodePoolName` works for pending counts, contradicting the main skill's explicit prohibition because pending pods are unassigned. Do not carry this contradiction into a new skill. Establish target-pool eligibility from pending workload evidence rather than a count alone. Its swap discussion also requires a legacy-only gate.
- The upstream provides operational read workflows, not a reviewed cross-version upgrade planner. An upgrade planning skill should be an **extension** grounded in the versioned sources above; no need to duplicate unmodified upstream workflows.

[skills/LICENSE](https://github.com/dsx-ai-factory/run-ai/blob/8190247dc97cd67538e8d4ab383d13b22da5037b/skills/LICENSE) assigns executable code to Apache-2.0 and SKILL.md/references/prose to CC-BY-4.0. If adapting prose, retain attribution to NVIDIA/Run:ai, link the pinned source and license, and identify modifications. Do not label copied prose Apache-only or imply NVIDIA endorsement.

Skipped: live cluster, MCP execution, and patch-specific runtime validation. Risk: archived aliases can move; recheck exact docs and entitlement before performing upgrades.
