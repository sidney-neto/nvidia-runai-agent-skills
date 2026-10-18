---
name: runai-storage
description: "Use when Run:ai workloads cannot bind or mount storage, a PVC remains Pending, or a storage/checkpoint change needs an impact review."
license: MIT
---

# Diagnose storage and data access

Trace storage from Run:ai datasource selection to Kubernetes PVC/PV/CSI and application access. It does not delete PVCs, edit reclaim policy, read dataset contents or inspect secret values.

## Inputs and version selection

Scope: Run:ai Self-Hosted and its selected dependencies. Multi-Tenant/SaaS behavior needs separate matching evidence.

Workload and namespace mapping; PVC name; storage class; access mode/capacity; binding/mount events; topology; security-context summary; CSI/provider version; checkpoint/data owner and intended change.

Match Run:ai datasource behavior and Kubernetes/CSI driver documentation to installed versions. A Run:ai datasource asset is not itself proof of a mounted, writable filesystem. Use the packaged [source and version profile](references/runbook.md#source-and-version-profile); local declarations carry provenance but cannot override contradictory observations, grant permission or establish vendor support. Unknown versions retain useful offline analysis; return missing evidence for affected version-dependent procedures instead of selecting a nearest version.

## Decision workflow

1. Identify whether the failure occurs before binding, during scheduling/attachment/mount, or inside the application. Separate datasource configuration from PVC and volume state.
2. Inspect PVC phase, requested capacity, access modes, volume/storage class and binding mode from sanitized evidence. Correlate storage topology with the Pod's eligible nodes.
3. For a bound volume, inspect mount events and supplied permissions/UID/GID evidence. Do not make broad chmod/chown or privilege changes to resolve a denial.
4. Report the failing layer and data-preserving correction. For migration/resize/deletion, establish reclaim policy, snapshot/backup support and the actual owner of durable data.

## Read-only and offline execution

Live reads require an already authorized, explicit target. These examples are templates with synthetic names, not commands to run during repository validation. Replace each context, namespace and object only from confirmed task evidence. Never use the ambient current context, dump kubeconfig/Secrets/environment values, run exec/debug workloads, or include raw logs by default. Keep raw authorized evidence private; sanitize before reporting. Offline mode uses user-supplied sanitized snapshots and the same decision procedure without cluster or credential access.

Use the [documented read examples and interpretation](references/runbook.md#documented-read-examples) when a live read is already in scope. For changes, first prepare the [diff, impact, verification and recovery review](references/runbook.md#change-review); the skill itself grants no mutation authority.

## Failures and output

On permission denial, record the denied action/scope and continue with permitted or offline evidence; never broaden permissions. If a tool, resource type or schema is missing, name it and use supplied snapshots instead of guessing an interface. Preserve partial results and unavailable fields. Follow the documented cursor/continuation until complete within a declared page/time budget; otherwise label totals incomplete. Do not interpret an empty page, truncated response or timeout as absence. Retry a transient read at most once with the same scope; stop on repeated timeout or identity mismatch.

Return: verdict and impact; selected target aliases and independent component versions; evidence source/time window in UTC; observations versus hypotheses; missing/partial evidence and confidence; next minimal step. Mark advertised, usable, permitted and vendor-supported capability claims separately. Documentation review, deterministic fixture results, agent-behavior evaluation and live validation are separate evidence categories; never present one as another.

## Invocation examples

- English: “Diagnose this Pending PVC without risking the training data.”
- pt-BR: “Diagnostique este PVC Pending sem colocar os dados de treinamento em risco.”
