---
name: runai-cluster-health
description: "Use when a Run:ai cluster appears unhealthy, disconnected, degraded, or unable to admit workloads and a bounded health assessment is needed."
license: MIT
---

# Assess cluster health

Locate the failing layer across control-plane synchronization, Kubernetes nodes, GPU capacity and workload admission. Do not turn a health check into a repair, stress test or cluster-wide log dump.

## Inputs and version selection

Scope: Run:ai Self-Hosted and its selected dependencies. Multi-Tenant/SaaS behavior needs separate matching evidence.

Cluster/context, Run:ai and system namespaces, incident window, selected nodes/components, observed versions, sanitized status/events and known baseline.

Select sources for the observed Run:ai cluster and control-plane releases separately. GPU health also depends on the exact GPU Operator/driver combination; Kubernetes Ready alone does not establish accelerator readiness. Use the packaged [source and version profile](references/runbook.md#source-and-version-profile); local declarations carry provenance but cannot override contradictory observations, grant permission or establish vendor support. Unknown versions retain useful offline analysis; return missing evidence for affected version-dependent procedures instead of selecting a nearest version.

## Decision workflow

1. Check evidence freshness and whether control-plane and cluster observations refer to the same environment. A disconnected or stale dashboard cannot establish current workload health.
2. Inspect selected node Ready/pressure conditions, Run:ai component availability and advertised versus allocatable GPU resources. Keep physical GPU count, scheduler allocation and utilization distinct.
3. Correlate the earliest failing layer with affected workloads: absent GPU capacity, unschedulable requests, failed admission and stale synchronization are different failures.
4. Return healthy, degraded or unknown per layer, with impact and the smallest next discriminating read. Do not mark a whole cluster healthy from one successful response.

## Read-only and offline execution

Live reads require an already authorized, explicit target. These examples are templates with synthetic names, not commands to run during repository validation. Replace each context, namespace and object only from confirmed task evidence. Never use the ambient current context, dump kubeconfig/Secrets/environment values, run exec/debug workloads, or include raw logs by default. Keep raw authorized evidence private; sanitize before reporting. Offline mode uses user-supplied sanitized snapshots and the same decision procedure without cluster or credential access.

Use the [documented read examples and interpretation](references/runbook.md#documented-read-examples) when a live read is already in scope. For changes, first prepare the [diff, impact, verification and recovery review](references/runbook.md#change-review); the skill itself grants no mutation authority.

## Failures and output

On permission denial, record the denied action/scope and continue with permitted or offline evidence; never broaden permissions. If a tool, resource type or schema is missing, name it and use supplied snapshots instead of guessing an interface. Preserve partial results and unavailable fields. Follow the documented cursor/continuation until complete within a declared page/time budget; otherwise label totals incomplete. Do not interpret an empty page, truncated response or timeout as absence. Retry a transient read at most once with the same scope; stop on repeated timeout or identity mismatch.

Return: verdict and impact; selected target aliases and independent component versions; evidence source/time window in UTC; observations versus hypotheses; missing/partial evidence and confidence; next minimal step. Mark advertised, usable, permitted and vendor-supported capability claims separately. Documentation review, deterministic fixture results, agent-behavior evaluation and live validation are separate evidence categories; never present one as another.

## Invocation examples

- English: “Assess cluster health from these node and Run:ai status snapshots.”
- pt-BR: “Avalie a saúde do cluster com estes snapshots de nós e do Run:ai.”

## Packaged helper

Use the [local helper and input contract](references/helpers.md) for repeatable offline analysis.
