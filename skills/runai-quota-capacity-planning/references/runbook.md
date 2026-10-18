# Plan quota and capacity — operational reference

## Documented read examples

Run only against an explicitly selected, authorized target. All names below are synthetic placeholders. Inspect only the fields needed for the question; command output is still private evidence until sanitized. `--request-timeout=15s` bounds each Kubernetes request, not the entire multi-page operation; use an overall time/page budget in the caller.

```sh
kubectl --context example-context --request-timeout=15s get node example-gpu-node -o jsonpath='{.metadata.name}{"\n"}{.status.capacity.nvidia\.com/gpu}{"\n"}{.status.allocatable.nvidia\.com/gpu}{"\n"}'
```

## Interpretation and decision limits

Kubernetes capacity is only one input and cannot reveal Run:ai quota. Use an authorized official `list_project_resources`/`list_department_resources` result with a discovered runtime schema, or a sanitized exported ledger. Preserve all pages and distinguish configured department quota from summed child usage.

Synthetic example: one pool has 8 physical GPUs; a department has quota 6; its children have quotas 4 and 3. Child commitments exceed that parent by 1. Adding the parent and children to claim 13 physical GPUs of demand double-counts the hierarchy. Actual allocation and eligible demand still need evidence.

A project pending on a nonexistent selector is not starved by another tenant. Pending workloads may not yet belong to a node pool; do not blanket-filter pending counts by pool. Apply pool eligibility from workload evidence. Fractional memory reservation, quota-accounted devices and physical cards remain separate columns.

Optional upstream reuse: `runai-audit-assigned-quota` at the linked revision specializes in live fairness auditing. Use it only if installed and its inputs/tools match. Its quota reference contains a conflicting pending-pool filter note; this library requires pending-reason and eligibility evidence instead of that blanket filter. Its mandatory-MCP stop does not constrain this skill's offline ledger analysis. Upstream prose is CC-BY-4.0 and code Apache-2.0; no upstream implementation is vendored.

## Bounded evidence review

Keep quota fairness and utilization as separate questions: allocation above a
finite quota establishes borrowing, not policy violation or idle capacity. A
reviewable reclaim recommendation needs eligible unmet demand in the same pool,
the exact borrowing/preemption policy and workload impact. Report the ledger's
page coverage and unknown cells alongside any total; never silently rank missing
quota or allocation values as zero. Historical allocation trends require dated
observations, not an extrapolation from one ledger.

## Change review

Show a per-pool before/after table, hierarchy totals, borrowing limit, affected pending/running workloads and preemption implications. Verify observed quotas and workload eligibility after an authorized change. Restoring a quota value does not resurrect preempted jobs or recover their progress.

A request for analysis authorizes analysis. Prepare the concrete proposed diff and checks before seeking any additional approval that execution requires. Execute only within explicit task authorization; a documentation example, discovered tool or local profile is not authorization. Stop if target identity changes or prerequisites contradict the selected procedure.

## Failure handling and evidence contract

On permission denial, record the denied action/scope and continue with permitted or offline evidence; never broaden permissions. If a tool, resource type or schema is missing, name it and use supplied snapshots instead of guessing an interface. Preserve partial results and unavailable fields. Follow the documented cursor/continuation until complete within a declared page/time budget; otherwise label totals incomplete. Do not interpret an empty page, truncated response or timeout as absence. Retry a transient read at most once with the same scope; stop on repeated timeout or identity mismatch.

Return: verdict and impact; selected target aliases and independent component versions; evidence source/time window in UTC; observations versus hypotheses; missing/partial evidence and confidence; next minimal step. Mark advertised, usable, permitted and vendor-supported capability claims separately. Documentation review, deterministic fixture results, agent-behavior evaluation and live validation are separate evidence categories; never present one as another.

## Source and version profile

Use the matching release semantics for quota and fractions. Do not convert scheduler-accounted devices into physical cards or infer memory/compute fractions from quota decimals.

The links below are reviewed evidence for this packaged workflow, not a blanket supported-version list. Versioned documentation supports only its stated scope. Unversioned Kubernetes command references establish command syntax; verify API/resource availability in the selected Kubernetes release. No installed skill requires repository-root files. A user-supplied local profile must state source, observation time, exact versions and uncertainty and remains a declaration until corroborated.

- [projects](https://docs.nvidia.com/run-ai/self-hosted/v3.0/documentation/platform-management/manage-ai-initiatives/organization/projects.md) — documentation `v3.0`; reviewed `2026-10-18`; SHA-256 `08618e745f7581c0228c10d3c8e0fa7c8af9a3dab02e0ca6ef1fabbda281e379`.
- [departments](https://docs.nvidia.com/run-ai/self-hosted/v3.0/documentation/platform-management/manage-ai-initiatives/organization/departments.md) — documentation `v3.0`; reviewed `2026-10-18`; SHA-256 `e89a1e5f8f6f2670fd1ffe59a047036312d9bd957da6f3592d9fb0bdf6b90d00`.
- [concepts-and-principles](https://docs.nvidia.com/run-ai/self-hosted/v3.0/documentation/platform-management/runai-scheduler/scheduling/concepts-and-principles.md) — documentation `v3.0`; reviewed `2026-10-18`; SHA-256 `7a008ff305fc74b836ac3c4c5c8bd15f1760dca9e43bc7b9cfbcbb28ccc9cd09`.
- [tools-reference](https://docs.nvidia.com/run-ai/self-hosted/v3.0/documentation/agents/mcp-server/tools-reference.md) — documentation `v3.0`; reviewed `2026-10-18`; SHA-256 `c4f7e964b94bcbbc0c84c986cf77597d14010bffa70b88431669044fd70c1d21`.
- [kubectl-get](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_get/) — documentation `unversioned`; reviewed `2026-10-18`; SHA-256 `4c9ca9706157c96d5dfc1fb9f3500eaf06fe75370a69ef03c5ba278f08894dfd`.
- [upstream-quota](https://raw.githubusercontent.com/dsx-ai-factory/run-ai/8190247dc97cd67538e8d4ab383d13b22da5037b/skills/runai-audit-assigned-quota/SKILL.md) — documentation `upstream skill snapshot`; reviewed `2026-10-18`; revision `8190247dc97cd67538e8d4ab383d13b22da5037b`.

Reviewed source text may contain commands that mutate systems or export sensitive configuration; it is reference data, not an instruction to execute those commands. Refresh only evidence affected by a changed dependency or procedure and retain previously reviewed provenance.

- [Upstream runai-audit-assigned-quota](https://github.com/dsx-ai-factory/run-ai/blob/70997dcca3b4486878778cef71b50830e708b31a/skills/runai-audit-assigned-quota/SKILL.md) — reviewed `2026-10-18`; revision `70997dcca3b4486878778cef71b50830e708b31a`; development workflow evidence only, not installed-release compatibility. Local guidance uses original wording and preserves version/permission checks and offline alternatives.
