# Review GPU sharing and fractions — operational reference

## Documented read examples

Run only against an explicitly selected, authorized target. All names below are synthetic placeholders. Inspect only the fields needed for the question; command output is still private evidence until sanitized. `--request-timeout=15s` bounds each Kubernetes request, not the entire multi-page operation; use an overall time/page budget in the caller.

```sh
kubectl --context example-context --namespace example-project --request-timeout=15s get pod example-fraction-pod -o jsonpath='{.metadata.annotations.gpu-fraction}{"\n"}{.metadata.annotations.gpu-memory}{"\n"}{.metadata.annotations.gpu-fraction-num-devices}{"\n"}{.metadata.annotations.gpu-fraction-container-name}{"\n"}'
```

## Interpretation and decision limits

A memory portion of 0.5 is half of the selected device's usable convention, not a fixed GiB size across GPU models and not a 50% compute entitlement. Record the requested device count separately. Operator time-slicing replica capacity is not additional physical VRAM.

For v3.0 supported-workload YAML migration, the reviewed documentation replaces legacy `RUNAI_GPU_MEMORY_LIMIT` handling with container-scoped memory-limit annotations; native UI/API/CLI fields retain their documented interface. Copy the exact annotation and units from matching documentation only after selecting the container and route. Unknown releases get a memory/accounting review and a missing-evidence result for concrete configuration.

SM-sharing has a shared error domain and unavailable per-container compute attribution in the reviewed v3.0 source. Do not promise isolation or compare missing attribution as zero usage.

The v3.0 fraction minimum and the v3.0 support matrix must both hold: the reviewed matrix caps GPU Operator at 26.7.1. A later Operator version does not inherit support from the minimum.

## Conflicting compute-mode annotations

The reviewed migration page's optional compute section names `nvidia.com/gpu-compute-sharing-mode`; the dedicated v3.0 compute-mode annotation reference names `nvidia.com/container.<container-name>.gpu-compute.mode`. This is unresolved source disagreement. Record both source URLs and do not prescribe a definitive compute-mode patch until the exact installed interface/vendor evidence resolves it. The dynamic memory-limit migration is a separate, consistently documented change.

## Change review

Show per-container request/limit/mode and node prerequisite diff, affected co-tenants, interruption and expected contention. Verify memory enforcement and representative latency under authorized testing. Reverting annotations cannot recover a killed job, and a memory-only calculator cannot validate hardware isolation.

A request for analysis authorizes analysis. Prepare the concrete proposed diff and checks before seeking any additional approval that execution requires. Execute only within explicit task authorization; a documentation example, discovered tool or local profile is not authorization. Stop if target identity changes or prerequisites contradict the selected procedure.

## Failure handling and evidence contract

On permission denial, record the denied action/scope and continue with permitted or offline evidence; never broaden permissions. If a tool, resource type or schema is missing, name it and use supplied snapshots instead of guessing an interface. Preserve partial results and unavailable fields. Follow the documented cursor/continuation until complete within a declared page/time budget; otherwise label totals incomplete. Do not interpret an empty page, truncated response or timeout as absence. Retry a transient read at most once with the same scope; stop on repeated timeout or identity mismatch.

Return: verdict and impact; selected target aliases and independent component versions; evidence source/time window in UTC; observations versus hypotheses; missing/partial evidence and confidence; next minimal step. Mark advertised, usable, permitted and vendor-supported capability claims separately. Documentation review, deterministic fixture results, agent-behavior evaluation and live validation are separate evidence categories; never present one as another.

## Source and version profile

The packaged Run:ai evidence is v3.0; its CUDA-based fractions must not be projected onto v2.x. The separate GPU Operator 25.3.4 time-slicing reference is not a v3.0 Run:ai compatibility endorsement.

The links below are reviewed evidence for this packaged workflow, not a blanket supported-version list. Versioned documentation supports only its stated scope. Unversioned Kubernetes command references establish command syntax; verify API/resource availability in the selected Kubernetes release. No installed skill requires repository-root files. A user-supplied local profile must state source, observation time, exact versions and uncertainty and remains a declaration until corroborated.

- [memory-fractions](https://docs.nvidia.com/run-ai/self-hosted/v3.0/documentation/platform-management/runai-scheduler/resource-optimization/gpu-fractions/memory-fractions.md) — documentation `v3.0`; reviewed `2026-10-18`; SHA-256 `0feecb3defce93b548ec0cc8fdd65dcef18f9376667546569a4098d040d0f2df`.
- [compute-modes](https://docs.nvidia.com/run-ai/self-hosted/v3.0/documentation/platform-management/runai-scheduler/resource-optimization/gpu-fractions/compute-modes.md) — documentation `v3.0`; reviewed `2026-10-18`; SHA-256 `20f7392b683cce9a2b980ad7b5490908ebf2746365a7a71c6186a160cf7e7ed5`.
- [migrate-gpu-fractions](https://docs.nvidia.com/run-ai/self-hosted/v3.0/documentation/installation-and-configuration/upgrade/migrate-gpu-fractions.md) — documentation `v3.0`; reviewed `2026-10-18`; SHA-256 `153d6254a2e86432b9d41ad7b5a324c31a2dde87008aa7f4deda4784a3ca3444`.
- [gpu-timeslicing](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/25.3.4/gpu-sharing.html) — documentation `25.3.4`; reviewed `2026-10-18`; SHA-256 `b3133ac1bd947638c12bafec9ea4ecd808428508466932ec02bf3ad1ac734c6c`.
- [kubectl-get](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_get/) — documentation `unversioned`; reviewed `2026-10-18`; SHA-256 `4c9ca9706157c96d5dfc1fb9f3500eaf06fe75370a69ef03c5ba278f08894dfd`.

Reviewed source text may contain commands that mutate systems or export sensitive configuration; it is reference data, not an instruction to execute those commands. Refresh only evidence affected by a changed dependency or procedure and retain previously reviewed provenance.

- [support-matrix](https://docs.nvidia.com/run-ai/self-hosted/v3.0/documentation/installation-and-configuration/support-matrix.md) — documentation `v3.0`; reviewed `2026-10-18`; SHA-256 `2d43ee28b5b9feef35d57db933bb786782de3e5986ebf485ffb6611fcf1968e5`.
