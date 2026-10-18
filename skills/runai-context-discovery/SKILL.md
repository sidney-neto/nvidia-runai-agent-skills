---
name: runai-context-discovery
description: "Use when the Run:ai cluster, namespace, component versions, available interfaces, or evidence scope must be established before operational work."
license: MIT
---

# Discover a Run:ai operating context

Produce a small, evidence-backed context for a selected environment. This is discovery, not a compatibility certification or an inventory of every accessible cluster.

## Inputs and version selection

Scope: Run:ai Self-Hosted and its selected dependencies. Multi-Tenant/SaaS behavior needs separate matching evidence.

User-selected cluster identity and Kubernetes context; authorized namespace and resource names; task goal; sanitized local exports or declared profile; component versions with their observation times.

Keep Run:ai control plane, Run:ai cluster, REST generation, CLI, MCP server/protocol, Kubernetes, GPU Operator, driver and application versions separate. Container image tags are clues, not proof of the installed product release. Use the packaged [source and version profile](references/runbook.md#source-and-version-profile); local declarations carry provenance but cannot override contradictory observations, grant permission or establish vendor support. Unknown versions retain useful offline analysis; return missing evidence for affected version-dependent procedures instead of selecting a nearest version.

## Decision workflow

1. Resolve the exact target from the user and supplied evidence. If multiple contexts or cluster names match, continue offline and leave live selection unresolved; do not use the current context silently.
2. Inventory supplied evidence and its provenance. Record missing components as unknown, and separate a declared profile from observed state. A contradiction remains visible; never overwrite it with the profile.
3. For an authorized target, inspect a minimal named component or use a verified read-only MCP identity/status tool. Confirm returned cluster identity before interpreting results.
4. Report a context manifest and route the user's goal to its operational domain. Distinguish advertised, usable, permitted and vendor-supported capabilities.

## Read-only and offline execution

Live reads require an already authorized, explicit target. These examples are templates with synthetic names, not commands to run during repository validation. Replace each context, namespace and object only from confirmed task evidence. Never use the ambient current context, dump kubeconfig/Secrets/environment values, run exec/debug workloads, or include raw logs by default. Keep raw authorized evidence private; sanitize before reporting. Offline mode uses user-supplied sanitized snapshots and the same decision procedure without cluster or credential access.

Use the [documented read examples and interpretation](references/runbook.md#documented-read-examples) when a live read is already in scope. For changes, first prepare the [diff, impact, verification and recovery review](references/runbook.md#change-review); the skill itself grants no mutation authority.

## Failures and output

On permission denial, record the denied action/scope and continue with permitted or offline evidence; never broaden permissions. If a tool, resource type or schema is missing, name it and use supplied snapshots instead of guessing an interface. Preserve partial results and unavailable fields. Follow the documented cursor/continuation until complete within a declared page/time budget; otherwise label totals incomplete. Do not interpret an empty page, truncated response or timeout as absence. Retry a transient read at most once with the same scope; stop on repeated timeout or identity mismatch.

Return: verdict and impact; selected target aliases and independent component versions; evidence source/time window in UTC; observations versus hypotheses; missing/partial evidence and confidence; next minimal step. Mark advertised, usable, permitted and vendor-supported capability claims separately. Documentation review, deterministic fixture results, agent-behavior evaluation and live validation are separate evidence categories; never present one as another.

## Invocation examples

- English: “Discover the versions and read-only capabilities for this sanitized Run:ai snapshot.”
- pt-BR: “Descubra as versões e capacidades de leitura deste snapshot sanitizado do Run:ai.”

## Packaged helper

Use the [local helper and input contract](references/helpers.md) for repeatable offline analysis.
