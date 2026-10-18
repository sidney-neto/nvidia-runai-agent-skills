---
name: runai-workload-policies
description: "Use when a Run:ai submission is rejected or altered by policy, or when reviewing defaults, constraints, inheritance and enforcement for a specific workload submission path."
license: MIT
---

# Evaluate effective workload policy

Explain the effective policy and produce a targeted policy/spec diff. This does not assume that every Kubernetes submission passes through Run:ai policy enforcement.

## Inputs and version selection

Scope: Run:ai Self-Hosted and its selected dependencies. Multi-Tenant/SaaS behavior needs separate matching evidence.

Cluster/product versions; project and parent scopes; native or supported workload type/GVK; actual UI/API/CLI/direct-Kubernetes submission path; requested spec; effective spec; rejection and policy revisions.

Choose documentation for both control-plane and cluster releases. Policy location and enforcement changed across releases; the reviewed v3.0 docs describe different paths for native and supported types. Do not transfer those rules to an unknown release. Use the packaged [source and version profile](references/runbook.md#source-and-version-profile); local declarations carry provenance but cannot override contradictory observations, grant permission or establish vendor support. Unknown versions retain useful offline analysis; return missing evidence for affected version-dependent procedures instead of selecting a nearest version.

## Decision workflow

1. Identify the actual submission route and workload type before selecting a policy. Preserve the submitted spec separately from defaults and admission mutations.
2. Resolve cluster, department and project scope policy plus the effective combination for the relevant workload type; include tenant scope only where that selected policy interface supports it. Prefer a documented effective-policy read or supplied effective export over guessing precedence.
3. Compare each changed/rejected field with its rule, source scope and enforcement point. Distinguish policy validation from Kubernetes admission and runtime resource availability.
4. Explain whether the observed path is covered. For external direct-Kubernetes submissions, do not promise control-plane policy enforcement; report the separate admission controls evidenced.

## Read-only and offline execution

Live reads require an already authorized, explicit target. These examples are templates with synthetic names, not commands to run during repository validation. Replace each context, namespace and object only from confirmed task evidence. Never use the ambient current context, dump kubeconfig/Secrets/environment values, run exec/debug workloads, or include raw logs by default. Keep raw authorized evidence private; sanitize before reporting. Offline mode uses user-supplied sanitized snapshots and the same decision procedure without cluster or credential access.

Use the [documented read examples and interpretation](references/runbook.md#documented-read-examples) when a live read is already in scope. For changes, first prepare the [diff, impact, verification and recovery review](references/runbook.md#change-review); the skill itself grants no mutation authority.

## Failures and output

On permission denial, record the denied action/scope and continue with permitted or offline evidence; never broaden permissions. If a tool, resource type or schema is missing, name it and use supplied snapshots instead of guessing an interface. Preserve partial results and unavailable fields. Follow the documented cursor/continuation until complete within a declared page/time budget; otherwise label totals incomplete. Do not interpret an empty page, truncated response or timeout as absence. Retry a transient read at most once with the same scope; stop on repeated timeout or identity mismatch.

Return: verdict and impact; selected target aliases and independent component versions; evidence source/time window in UTC; observations versus hypotheses; missing/partial evidence and confidence; next minimal step. Mark advertised, usable, permitted and vendor-supported capability claims separately. Documentation review, deterministic fixture results, agent-behavior evaluation and live validation are separate evidence categories; never present one as another.

## Invocation examples

- English: “Explain which effective policy changed this submission and whether direct YAML is covered.”
- pt-BR: “Explique qual política efetiva alterou esta submissão e se o YAML direto é coberto.”
