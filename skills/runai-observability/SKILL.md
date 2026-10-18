---
name: runai-observability
description: "Use when Run:ai metrics, alerts or workload monitoring are missing or contradictory, or when distinguishing GPU allocation, utilization and memory use over a defined window."
license: MIT
---

# Interpret operational telemetry

Validate telemetry meaning and freshness before drawing an operational conclusion. It does not scrape arbitrary endpoints, collect all logs or configure external alert destinations.

## Inputs and version selection

Scope: Run:ai Self-Hosted and its selected dependencies. Multi-Tenant/SaaS behavior needs separate matching evidence.

Cluster/project/workload scope; time zone/window; metric names and units; query/aggregation; scrape/exporter status; sample interval; missing-series behavior; selected component versions and sanitized series.

Metric names, labels and per-container attribution are release/mode-specific. Select matching Run:ai and exporter/GPU Operator evidence; a graph label is not a stable API contract. Use the packaged [source and version profile](references/runbook.md#source-and-version-profile); local declarations carry provenance but cannot override contradictory observations, grant permission or establish vendor support. Unknown versions retain useful offline analysis; return missing evidence for affected version-dependent procedures instead of selecting a nearest version.

## Decision workflow

1. Define the question and time window. Distinguish configured quota, scheduled allocation, compute utilization, GPU memory used and requested/limited memory.
2. Check collection freshness, scrape health, label scope and aggregation before interpreting low/empty values. Missing, stale, zero and filtered-out series are different states.
3. Correlate observed peaks and alerts with workload history and node conditions in the same window. Do not infer measured peaks from resource limits or causal relationships from coincidence.
4. Report scope, query semantics, sample gaps and uncertainty. Recommend a narrower telemetry check or alert change only when the evidence supports it.

## Read-only and offline execution

Live reads require an already authorized, explicit target. These examples are templates with synthetic names, not commands to run during repository validation. Replace each context, namespace and object only from confirmed task evidence. Never use the ambient current context, dump kubeconfig/Secrets/environment values, run exec/debug workloads, or include raw logs by default. Keep raw authorized evidence private; sanitize before reporting. Offline mode uses user-supplied sanitized snapshots and the same decision procedure without cluster or credential access.

Use the [documented read examples and interpretation](references/runbook.md#documented-read-examples) when a live read is already in scope. For changes, first prepare the [diff, impact, verification and recovery review](references/runbook.md#change-review); the skill itself grants no mutation authority.

## Failures and output

On permission denial, record the denied action/scope and continue with permitted or offline evidence; never broaden permissions. If a tool, resource type or schema is missing, name it and use supplied snapshots instead of guessing an interface. Preserve partial results and unavailable fields. Follow the documented cursor/continuation until complete within a declared page/time budget; otherwise label totals incomplete. Do not interpret an empty page, truncated response or timeout as absence. Retry a transient read at most once with the same scope; stop on repeated timeout or identity mismatch.

Return: verdict and impact; selected target aliases and independent component versions; evidence source/time window in UTC; observations versus hypotheses; missing/partial evidence and confidence; next minimal step. Mark advertised, usable, permitted and vendor-supported capability claims separately. Documentation review, deterministic fixture results, agent-behavior evaluation and live validation are separate evidence categories; never present one as another.

## Invocation examples

- English: “Explain whether this GPU-utilization report is valid despite missing samples.”
- pt-BR: “Explique se este relatório de utilização de GPU é válido apesar das amostras ausentes.”
