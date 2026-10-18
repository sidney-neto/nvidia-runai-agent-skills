---
name: runai-scheduling-diagnostics
description: "Use when a Run:ai workload is Pending or unschedulable and quota, eligible nodes, gang scheduling, topology or resource fragmentation may block placement."
license: MIT
---

# Diagnose scheduling and placement

Find the first evidenced placement constraint and distinguish it from startup failure. It does not reclaim GPUs, relax policies or delete workloads.

## Inputs and version selection

Scope: Run:ai Self-Hosted and its selected dependencies. Multi-Tenant/SaaS behavior needs separate matching evidence.

Exact workload/cluster/project and mapped namespace; current attempt UID; pending reasons/events; scheduler name; effective resource requests; selectors/tolerations; pool quotas; node allocatable/occupancy; timestamp.

Confirm scheduler implementation and release before interpreting Run:ai-specific events. A KAI-Scheduler upstream feature is not proof that the installed Run:ai release exposes it. Use the packaged [source and version profile](references/runbook.md#source-and-version-profile); local declarations carry provenance but cannot override contradictory observations, grant permission or establish vendor support. Unknown versions retain useful offline analysis; return missing evidence for affected version-dependent procedures instead of selecting a nearest version.

## Decision workflow

1. Confirm the current attempt and whether it is unscheduled. ImagePullBackOff, FailedMount and crashed containers belong to startup/runtime diagnosis even if the workload headline says Pending.
2. Evaluate constraints in order: scheduler selection and admission, project/pool eligibility, quota/preemptibility, per-node GPU/CPU/RAM fit, topology and complete distributed-group fit.
3. Use scheduler reasons to rank causes. A pool can have enough aggregate GPUs while no eligible node fits one worker; available memory fractions cannot satisfy a whole-device request automatically.
4. Return the blocked constraint, a counterfactual fit calculation and the smallest evidence-supported change. Label the local fit calculation necessary but not sufficient for actual scheduling.

## Read-only and offline execution

Live reads require an already authorized, explicit target. These examples are templates with synthetic names, not commands to run during repository validation. Replace each context, namespace and object only from confirmed task evidence. Never use the ambient current context, dump kubeconfig/Secrets/environment values, run exec/debug workloads, or include raw logs by default. Keep raw authorized evidence private; sanitize before reporting. Offline mode uses user-supplied sanitized snapshots and the same decision procedure without cluster or credential access.

Use the [documented read examples and interpretation](references/runbook.md#documented-read-examples) when a live read is already in scope. For changes, first prepare the [diff, impact, verification and recovery review](references/runbook.md#change-review); the skill itself grants no mutation authority.

## Failures and output

On permission denial, record the denied action/scope and continue with permitted or offline evidence; never broaden permissions. If a tool, resource type or schema is missing, name it and use supplied snapshots instead of guessing an interface. Preserve partial results and unavailable fields. Follow the documented cursor/continuation until complete within a declared page/time budget; otherwise label totals incomplete. Do not interpret an empty page, truncated response or timeout as absence. Retry a transient read at most once with the same scope; stop on repeated timeout or identity mismatch.

Return: verdict and impact; selected target aliases and independent component versions; evidence source/time window in UTC; observations versus hypotheses; missing/partial evidence and confidence; next minimal step. Mark advertised, usable, permitted and vendor-supported capability claims separately. Documentation review, deterministic fixture results, agent-behavior evaluation and live validation are separate evidence categories; never present one as another.

## Invocation examples

- English: “Diagnose why this workload is Pending despite four free GPUs.”
- pt-BR: “Diagnostique por que este workload está Pending apesar de quatro GPUs livres.”

## Packaged helper

Use the [local helper and input contract](references/helpers.md) for repeatable offline analysis.
