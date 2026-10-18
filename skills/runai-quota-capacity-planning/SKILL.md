---
name: runai-quota-capacity-planning
description: "Use when planning Run:ai GPU quota, department/project capacity, borrowing headroom, or explaining apparent quota starvation within a node pool."
license: MIT
---

# Plan quota and capacity

Build a per-pool capacity and demand ledger, then propose an auditable quota change. This is not a utilization optimization verdict or automatic quota rebalance.

## Inputs and version selection

Scope: Run:ai Self-Hosted and its selected dependencies. Multi-Tenant/SaaS behavior needs separate matching evidence.

Exact cluster and node pool; department/project parent map; deserved/allocated/limit values and units; pending reasons; physical and schedulable capacity; preemptibility; timestamp; desired change.

Use the matching release semantics for quota and fractions. Do not convert scheduler-accounted devices into physical cards or infer memory/compute fractions from quota decimals. Use the packaged [source and version profile](references/runbook.md#source-and-version-profile); local declarations carry provenance but cannot override contradictory observations, grant permission or establish vendor support. Unknown versions retain useful offline analysis; return missing evidence for affected version-dependent procedures instead of selecting a nearest version.

## Decision workflow

1. Normalize each (cluster, node pool, organizational unit) cell with its unit and snapshot time. Missing, unlimited and zero are separate states. Reject mixed timestamps or units for a definitive total.
2. Compare child project quotas with their department quota and physical pool capacity in separate ledgers. Sum leaf allocations once; never add parent allocation to the same children. Count independent top-level commitments once when assessing physical oversubscription.
3. Compute borrowing=max(0, allocated-deserved), deficit=max(0, deserved-allocated) and headroom only where limit semantics are known. A deficit plus Pending is not starvation: inspect eligible pool, pending reason and preemptibility.
4. Model before/after quotas and demand. Separate oversubscription, placement limits and reclaimable borrowing; no borrower means no reclaim recommendation.

## Read-only and offline execution

Live reads require an already authorized, explicit target. These examples are templates with synthetic names, not commands to run during repository validation. Replace each context, namespace and object only from confirmed task evidence. Never use the ambient current context, dump kubeconfig/Secrets/environment values, run exec/debug workloads, or include raw logs by default. Keep raw authorized evidence private; sanitize before reporting. Offline mode uses user-supplied sanitized snapshots and the same decision procedure without cluster or credential access.

Use the [documented read examples and interpretation](references/runbook.md#documented-read-examples) when a live read is already in scope. For changes, first prepare the [diff, impact, verification and recovery review](references/runbook.md#change-review); the skill itself grants no mutation authority.

## Failures and output

On permission denial, record the denied action/scope and continue with permitted or offline evidence; never broaden permissions. If a tool, resource type or schema is missing, name it and use supplied snapshots instead of guessing an interface. Preserve partial results and unavailable fields. Follow the documented cursor/continuation until complete within a declared page/time budget; otherwise label totals incomplete. Do not interpret an empty page, truncated response or timeout as absence. Retry a transient read at most once with the same scope; stop on repeated timeout or identity mismatch.

Return: verdict and impact; selected target aliases and independent component versions; evidence source/time window in UTC; observations versus hypotheses; missing/partial evidence and confidence; next minimal step. Mark advertised, usable, permitted and vendor-supported capability claims separately. Documentation review, deterministic fixture results, agent-behavior evaluation and live validation are separate evidence categories; never present one as another.

## Invocation examples

- English: “Check whether this eight-GPU quota plan double-counts departments and projects.”
- pt-BR: “Verifique se este plano de cotas de oito GPUs conta departamentos e projetos duas vezes.”

## Packaged helper

Use the [local helper and input contract](references/helpers.md) for repeatable offline analysis.
