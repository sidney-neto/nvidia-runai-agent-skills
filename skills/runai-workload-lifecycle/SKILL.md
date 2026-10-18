---
name: runai-workload-lifecycle
description: "Use when identifying a Run:ai workload attempt, explaining failure versus suspension/preemption/completion, or planning a targeted submit, resume, stop, update or delete operation."
license: MIT
---

# Review workload lifecycle

Build the correct lifecycle diagnosis and a concrete change proposal for one workload. It does not restart or resubmit merely because a workload is unhealthy.

## Inputs and version selection

Scope: Run:ai Self-Hosted and its selected dependencies. Multi-Tenant/SaaS behavior needs separate matching evidence.

Cluster ID, project, workload ID or exact name with attempt/time, mapped namespace/Pod UID, workload type, state/history, sanitized requested spec, persistence/checkpoint strategy and intended operation.

Confirm native/supported workload type and matching lifecycle interface for the installed release. Do not reuse legacy CRD names or operation support from another product version. Use the packaged [source and version profile](references/runbook.md#source-and-version-profile); local declarations carry provenance but cannot override contradictory observations, grant permission or establish vendor support. Unknown versions retain useful offline analysis; return missing evidence for affected version-dependent procedures instead of selecting a nearest version.

## Decision workflow

1. Resolve one workload attempt by ID and verify cluster/project. With a name, compare candidates and phase times instead of silently taking the newest item.
2. Classify completion, suspension, preemption, admission/startup failure and application failure from direct signals and history. Running can coexist with container crash loops; exit 137 alone does not prove OOM.
3. Compare desired operation with the current state and documented type capabilities. Establish checkpoint/PVC ownership and retry/idempotency implications before proposing resubmission.
4. Produce a precise operation plan or a read-only failure verdict with recurrence, owner and missing evidence. Never conflate requested memory with observed peak usage.

## Read-only and offline execution

Live reads require an already authorized, explicit target. These examples are templates with synthetic names, not commands to run during repository validation. Replace each context, namespace and object only from confirmed task evidence. Never use the ambient current context, dump kubeconfig/Secrets/environment values, run exec/debug workloads, or include raw logs by default. Keep raw authorized evidence private; sanitize before reporting. Offline mode uses user-supplied sanitized snapshots and the same decision procedure without cluster or credential access.

Use the [documented read examples and interpretation](references/runbook.md#documented-read-examples) when a live read is already in scope. For changes, first prepare the [diff, impact, verification and recovery review](references/runbook.md#change-review); the skill itself grants no mutation authority.

## Failures and output

On permission denial, record the denied action/scope and continue with permitted or offline evidence; never broaden permissions. If a tool, resource type or schema is missing, name it and use supplied snapshots instead of guessing an interface. Preserve partial results and unavailable fields. Follow the documented cursor/continuation until complete within a declared page/time budget; otherwise label totals incomplete. Do not interpret an empty page, truncated response or timeout as absence. Retry a transient read at most once with the same scope; stop on repeated timeout or identity mismatch.

Return: verdict and impact; selected target aliases and independent component versions; evidence source/time window in UTC; observations versus hypotheses; missing/partial evidence and confidence; next minimal step. Mark advertised, usable, permitted and vendor-supported capability claims separately. Documentation review, deterministic fixture results, agent-behavior evaluation and live validation are separate evidence categories; never present one as another.

## Invocation examples

- English: “Determine whether this stopped workload failed or was preempted and prepare a recovery plan.”
- pt-BR: “Determine se este workload parado falhou ou sofreu preempção e prepare um plano de recuperação.”
