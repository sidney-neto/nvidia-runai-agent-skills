---
name: runai-projects-departments
description: "Use when designing, auditing, or changing Run:ai projects, parent departments, namespace mappings, node-pool assignments, or organizational ownership."
license: MIT
---

# Review projects and departments

Produce a scoped organizational mapping and a change proposal with workload impact. It does not create identities, infer namespace names or delete projects during discovery.

## Inputs and version selection

Scope: Run:ai Self-Hosted and its selected dependencies. Multi-Tenant/SaaS behavior needs separate matching evidence.

Cluster, project/department IDs and names, confirmed namespace mapping, parent/child relationships, node pools, owners, access rules, workloads and desired organizational change.

Use organization documentation for the installed Run:ai release. A project name is not a Kubernetes namespace contract; confirm the mapping from selected environment evidence. Use the packaged [source and version profile](references/runbook.md#source-and-version-profile); local declarations carry provenance but cannot override contradictory observations, grant permission or establish vendor support. Unknown versions retain useful offline analysis; return missing evidence for affected version-dependent procedures instead of selecting a nearest version.

## Decision workflow

1. Resolve stable IDs, cluster and parent relationships, including projects with no configured quota. Do not use a quota-only list as a complete organization inventory.
2. Check the confirmed namespace creation state, workload ownership, access-rule scope, policy inheritance and node-pool eligibility. Record inaccessible children as unknown, not absent.
3. Assess a proposed move/creation/deletion against both parent quota accounting and inherited access/policy. Detect duplicate names across clusters and do not merge them.
4. Prepare the smallest organizational diff and an owner-by-owner impact summary. Deletion requires explicit workload/data disposition; a recreated name is not the same identity.

## Read-only and offline execution

Live reads require an already authorized, explicit target. These examples are templates with synthetic names, not commands to run during repository validation. Replace each context, namespace and object only from confirmed task evidence. Never use the ambient current context, dump kubeconfig/Secrets/environment values, run exec/debug workloads, or include raw logs by default. Keep raw authorized evidence private; sanitize before reporting. Offline mode uses user-supplied sanitized snapshots and the same decision procedure without cluster or credential access.

Use the [documented read examples and interpretation](references/runbook.md#documented-read-examples) when a live read is already in scope. For changes, first prepare the [diff, impact, verification and recovery review](references/runbook.md#change-review); the skill itself grants no mutation authority.

## Failures and output

On permission denial, record the denied action/scope and continue with permitted or offline evidence; never broaden permissions. If a tool, resource type or schema is missing, name it and use supplied snapshots instead of guessing an interface. Preserve partial results and unavailable fields. Follow the documented cursor/continuation until complete within a declared page/time budget; otherwise label totals incomplete. Do not interpret an empty page, truncated response or timeout as absence. Retry a transient read at most once with the same scope; stop on repeated timeout or identity mismatch.

Return: verdict and impact; selected target aliases and independent component versions; evidence source/time window in UTC; observations versus hypotheses; missing/partial evidence and confidence; next minimal step. Mark advertised, usable, permitted and vendor-supported capability claims separately. Documentation review, deterministic fixture results, agent-behavior evaluation and live validation are separate evidence categories; never present one as another.

## Invocation examples

- English: “Review the impact of moving this project to another department.”
- pt-BR: “Revise o impacto de mover este projeto para outro departamento.”
