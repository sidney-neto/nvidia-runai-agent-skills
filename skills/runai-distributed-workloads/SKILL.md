---
name: runai-distributed-workloads
description: "Use when Run:ai distributed training or inference cannot place all workers, initialize rendezvous, communicate, recover checkpoints or meet topology requirements."
license: MIT
---

# Diagnose distributed workloads

Separate group placement from process rendezvous and collective communication. It does not launch benchmarks, exec into workers or tune network/kernel parameters speculatively.

## Inputs and version selection

Scope: Run:ai Self-Hosted and its selected dependencies. Multi-Tenant/SaaS behavior needs separate matching evidence.

Exact workload/group and role topology; framework/version; worker count and resources; TP/PP/data-parallel design; rank/world-size/rendezvous configuration with secrets removed; node placement; interconnect; timestamp and checkpoint strategy.

Select the installed Run:ai workload/controller API and framework version. Training and distributed inference can have different role and lifecycle contracts; a sample for one is not a universal manifest. Use the packaged [source and version profile](references/runbook.md#source-and-version-profile); local declarations carry provenance but cannot override contradictory observations, grant permission or establish vendor support. Unknown versions retain useful offline analysis; return missing evidence for affected version-dependent procedures instead of selecting a nearest version.

## Decision workflow

1. Validate the expected group shape and per-role resources. Confirm whether all required workers are admitted/placed and whether aggregate capacity also satisfies per-node and topology constraints.
2. If placement succeeds, compare rank/world-size and rendezvous host/port agreement. Identify the first failing rank/time; downstream timeout cascades do not identify the original cause.
3. Correlate startup states, storage access, DNS/NetworkPolicy and interconnect evidence. Separate unavailable RDMA/topology from application collective mismatch or data-loader stalls.
4. Assess retry/checkpoint consistency across the whole group. Return the smallest corrected group configuration or next read, with limits on offline throughput claims.

## Read-only and offline execution

Live reads require an already authorized, explicit target. These examples are templates with synthetic names, not commands to run during repository validation. Replace each context, namespace and object only from confirmed task evidence. Never use the ambient current context, dump kubeconfig/Secrets/environment values, run exec/debug workloads, or include raw logs by default. Keep raw authorized evidence private; sanitize before reporting. Offline mode uses user-supplied sanitized snapshots and the same decision procedure without cluster or credential access.

Use the [documented read examples and interpretation](references/runbook.md#documented-read-examples) when a live read is already in scope. For changes, first prepare the [diff, impact, verification and recovery review](references/runbook.md#change-review); the skill itself grants no mutation authority.

## Failures and output

On permission denial, record the denied action/scope and continue with permitted or offline evidence; never broaden permissions. If a tool, resource type or schema is missing, name it and use supplied snapshots instead of guessing an interface. Preserve partial results and unavailable fields. Follow the documented cursor/continuation until complete within a declared page/time budget; otherwise label totals incomplete. Do not interpret an empty page, truncated response or timeout as absence. Retry a transient read at most once with the same scope; stop on repeated timeout or identity mismatch.

Return: verdict and impact; selected target aliases and independent component versions; evidence source/time window in UTC; observations versus hypotheses; missing/partial evidence and confidence; next minimal step. Mark advertised, usable, permitted and vendor-supported capability claims separately. Documentation review, deterministic fixture results, agent-behavior evaluation and live validation are separate evidence categories; never present one as another.

## Invocation examples

- English: “Determine whether this distributed job is blocked by gang placement or rendezvous.”
- pt-BR: “Determine se este job distribuído está bloqueado pelo posicionamento do grupo ou pelo rendezvous.”
