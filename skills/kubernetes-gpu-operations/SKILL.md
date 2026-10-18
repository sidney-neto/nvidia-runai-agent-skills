---
name: kubernetes-gpu-operations
description: "Use when diagnosing Kubernetes GPU-node readiness or planning bounded node maintenance, evacuation, return-to-service, or control-plane availability for a Run:ai environment."
license: MIT
---

# Plan Kubernetes GPU-node operations

Create a node-specific maintenance decision with workload and control-plane impact. It does not drain, taint, reboot, join or remove nodes during a read-only assessment.

## Inputs and version selection

Scope: Run:ai Self-Hosted and its selected dependencies. Multi-Tenant/SaaS behavior needs separate matching evidence.

Explicit context/node names; node roles; Kubernetes distribution/version; GPU resources; resident workload/PVC/checkpoint evidence; PodDisruptionBudgets; spare eligible capacity; maintenance window; control-plane/etcd topology.

Use distribution-specific Kubernetes maintenance procedures and the matching Run:ai release. Run:ai system nodes and Kubernetes control-plane nodes are different roles; a node may carry both. Use the packaged [source and version profile](references/runbook.md#source-and-version-profile); local declarations carry provenance but cannot override contradictory observations, grant permission or establish vendor support. Unknown versions retain useful offline analysis; return missing evidence for affected version-dependent procedures instead of selecting a nearest version.

## Decision workflow

1. Classify the selected node as worker, Run:ai system, Kubernetes control plane and/or etcd member. Identify quorum and whether the installation has a single control-plane node.
2. Inventory only authorized resident workloads and dependencies. Check checkpoints, local storage, restart semantics, disruption budgets and actual alternate-node fit; aggregate free GPUs do not prove evacuation can finish.
3. For a single control plane, plan API unavailability and recovery access explicitly. Do not present a rolling or zero-downtime procedure without redundant control-plane/etcd evidence.
4. Produce maintenance entry/exit criteria and a named-node change proposal. A failed prerequisite stops eviction/reboot planning, while offline risk analysis continues.

## Read-only and offline execution

Live reads require an already authorized, explicit target. These examples are templates with synthetic names, not commands to run during repository validation. Replace each context, namespace and object only from confirmed task evidence. Never use the ambient current context, dump kubeconfig/Secrets/environment values, run exec/debug workloads, or include raw logs by default. Keep raw authorized evidence private; sanitize before reporting. Offline mode uses user-supplied sanitized snapshots and the same decision procedure without cluster or credential access.

Use the [documented read examples and interpretation](references/runbook.md#documented-read-examples) when a live read is already in scope. For changes, first prepare the [diff, impact, verification and recovery review](references/runbook.md#change-review); the skill itself grants no mutation authority.

## Failures and output

On permission denial, record the denied action/scope and continue with permitted or offline evidence; never broaden permissions. If a tool, resource type or schema is missing, name it and use supplied snapshots instead of guessing an interface. Preserve partial results and unavailable fields. Follow the documented cursor/continuation until complete within a declared page/time budget; otherwise label totals incomplete. Do not interpret an empty page, truncated response or timeout as absence. Retry a transient read at most once with the same scope; stop on repeated timeout or identity mismatch.

Return: verdict and impact; selected target aliases and independent component versions; evidence source/time window in UTC; observations versus hypotheses; missing/partial evidence and confidence; next minimal step. Mark advertised, usable, permitted and vendor-supported capability claims separately. Documentation review, deterministic fixture results, agent-behavior evaluation and live validation are separate evidence categories; never present one as another.

## Invocation examples

- English: “Prepare maintenance for this GPU node and flag the single-control-plane impact.”
- pt-BR: “Prepare a manutenção deste nó GPU e destaque o impacto de um único nó de control plane.”
