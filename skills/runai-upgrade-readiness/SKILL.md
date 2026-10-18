---
name: runai-upgrade-readiness
description: "Use when assessing a specific Run:ai source-to-target upgrade, prerequisite gaps, workload migrations, maintenance impact or recovery readiness."
license: MIT
---

# Assess an explicit upgrade transition

Produce a go/no-go evidence checklist for one explicit transition. This is not an upgrade executor or a claim that a numerically nearby version is supported.

## Inputs and version selection

Scope: Run:ai Self-Hosted and its selected dependencies. Multi-Tenant/SaaS behavior needs separate matching evidence.

Exact source and target control-plane/cluster releases; Kubernetes distribution/version; GPU Operator/driver/CUDA versions; topology; installed features; workload types; backup/restore evidence and maintenance objectives.

Require a reviewed source that covers the actual source→target transition and support entitlement/lifecycle, plus both endpoint prerequisites. A generic maximum-version-gap rule, ordered version comparison or local profile is insufficient proof. Use the packaged [source and version profile](references/runbook.md#source-and-version-profile); local declarations carry provenance but cannot override contradictory observations, grant permission or establish vendor support. Unknown versions retain useful offline analysis; return missing evidence for affected version-dependent procedures instead of selecting a nearest version.

## Decision workflow

1. Identify both endpoints and their installed feature usage. Separate product release from chart, CLI, REST and MCP versions; reject ambiguous version inputs for a definitive readiness verdict.
2. Find explicit transition evidence and dependency support for each endpoint. If the transition is unreviewed, return missing evidence while continuing offline workload/dependency analysis.
3. Compare affected features: fractions and dynamic-limit manifests, legacy workload controllers, swap assumptions, policy paths, storage, networking and authentication. Map every required interruption to workload owners.
4. Assess backup completeness, tested restore, change order, single-control-plane availability and validation gates. Return ready, blocked or unknown per item, with exact evidence and unresolved decisions.

## Read-only and offline execution

Live reads require an already authorized, explicit target. These examples are templates with synthetic names, not commands to run during repository validation. Replace each context, namespace and object only from confirmed task evidence. Never use the ambient current context, dump kubeconfig/Secrets/environment values, run exec/debug workloads, or include raw logs by default. Keep raw authorized evidence private; sanitize before reporting. Offline mode uses user-supplied sanitized snapshots and the same decision procedure without cluster or credential access.

Use the [documented read examples and interpretation](references/runbook.md#documented-read-examples) when a live read is already in scope. For changes, first prepare the [diff, impact, verification and recovery review](references/runbook.md#change-review); the skill itself grants no mutation authority.

## Failures and output

On permission denial, record the denied action/scope and continue with permitted or offline evidence; never broaden permissions. If a tool, resource type or schema is missing, name it and use supplied snapshots instead of guessing an interface. Preserve partial results and unavailable fields. Follow the documented cursor/continuation until complete within a declared page/time budget; otherwise label totals incomplete. Do not interpret an empty page, truncated response or timeout as absence. Retry a transient read at most once with the same scope; stop on repeated timeout or identity mismatch.

Return: verdict and impact; selected target aliases and independent component versions; evidence source/time window in UTC; observations versus hypotheses; missing/partial evidence and confidence; next minimal step. Mark advertised, usable, permitted and vendor-supported capability claims separately. Documentation review, deterministic fixture results, agent-behavior evaluation and live validation are separate evidence categories; never present one as another.

## Invocation examples

- English: “Assess this exact Run:ai source-to-target upgrade using the supplied offline inventory.”
- pt-BR: “Avalie esta atualização entre versões exatas do Run:ai com o inventário offline fornecido.”

## Packaged helper

Use the [local helper and input contract](references/helpers.md) for repeatable offline analysis.
