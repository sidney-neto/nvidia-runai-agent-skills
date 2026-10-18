---
name: runai-backup-recovery
description: "Use when planning Run:ai backup/restore, reviewing recovery evidence, or assessing data and configuration protection before maintenance or an upgrade."
license: MIT
---

# Assess backup and recovery readiness

Build a recovery inventory and evidence-based restore plan. It does not export secrets/databases, run restore commands or promise that Helm state covers application data.

## Inputs and version selection

Scope: Run:ai Self-Hosted and its selected dependencies. Multi-Tenant/SaaS behavior needs separate matching evidence.

Exact deployment/release/topology; recovery objective and incident cutoff; control-plane database and external services; Helm/runtime configuration inventory; Kubernetes/etcd ownership; PVC/dataset/checkpoint owners; backup timestamps, retention and restore-test records.

Use Run:ai backup guidance matching the installed release and separately match PostgreSQL, metrics store, CSI and Kubernetes/etcd tooling. A backup from another schema/version is not automatically restorable. Use the packaged [source and version profile](references/runbook.md#source-and-version-profile); local declarations carry provenance but cannot override contradictory observations, grant permission or establish vendor support. Unknown versions retain useful offline analysis; return missing evidence for affected version-dependent procedures instead of selecting a nearest version.

## Decision workflow

1. Map each recovery domain: control-plane data, deployment/runtime config, Kubernetes state, external identity/metrics services, workload PVCs and application checkpoints. Assign one owner and recovery source to each.
2. Assess consistency, snapshot time, encryption/access, retention, off-cluster availability and dependency order from metadata. Do not read backup payloads or credentials just to build the inventory.
3. Compare the latest successful restore drill with current versions and target topology. A successful backup job or file checksum proves capture/integrity, not a usable application restore.
4. Produce a restore sequence, isolated validation targets and irreversible cutover points, with missing domains explicitly blocking a complete recovery claim.

## Read-only and offline execution

Live reads require an already authorized, explicit target. These examples are templates with synthetic names, not commands to run during repository validation. Replace each context, namespace and object only from confirmed task evidence. Never use the ambient current context, dump kubeconfig/Secrets/environment values, run exec/debug workloads, or include raw logs by default. Keep raw authorized evidence private; sanitize before reporting. Offline mode uses user-supplied sanitized snapshots and the same decision procedure without cluster or credential access.

Use the [documented read examples and interpretation](references/runbook.md#documented-read-examples) when a live read is already in scope. For changes, first prepare the [diff, impact, verification and recovery review](references/runbook.md#change-review); the skill itself grants no mutation authority.

## Failures and output

On permission denial, record the denied action/scope and continue with permitted or offline evidence; never broaden permissions. If a tool, resource type or schema is missing, name it and use supplied snapshots instead of guessing an interface. Preserve partial results and unavailable fields. Follow the documented cursor/continuation until complete within a declared page/time budget; otherwise label totals incomplete. Do not interpret an empty page, truncated response or timeout as absence. Retry a transient read at most once with the same scope; stop on repeated timeout or identity mismatch.

Return: verdict and impact; selected target aliases and independent component versions; evidence source/time window in UTC; observations versus hypotheses; missing/partial evidence and confidence; next minimal step. Mark advertised, usable, permitted and vendor-supported capability claims separately. Documentation review, deterministic fixture results, agent-behavior evaluation and live validation are separate evidence categories; never present one as another.

## Invocation examples

- English: “Audit whether these backups can restore the Run:ai platform and training checkpoints.”
- pt-BR: “Audite se estes backups conseguem restaurar a plataforma Run:ai e os checkpoints de treinamento.”
