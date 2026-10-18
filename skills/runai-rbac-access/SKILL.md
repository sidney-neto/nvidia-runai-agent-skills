---
name: runai-rbac-access
description: "Use when Run:ai or Kubernetes access is denied, a role is being reviewed, or least-privilege access to a specific project/resource must be planned."
license: MIT
---

# Explain access and RBAC

Identify the authorization plane, principal, action and scope responsible for a denial. This is not credential retrieval, impersonation or automatic privilege escalation.

## Inputs and version selection

Scope: Run:ai Self-Hosted and its selected dependencies. Multi-Tenant/SaaS behavior needs separate matching evidence.

Sanitized error/status; timestamp; principal alias; exact action and resource; Run:ai scope; Kubernetes context/namespace; role/access-rule evidence; selected release.

Run:ai role names and permission sets are release-specific. Kubernetes RBAC is a separate decision even when Run:ai provisions related cluster permissions. Use the packaged [source and version profile](references/runbook.md#source-and-version-profile); local declarations carry provenance but cannot override contradictory observations, grant permission or establish vendor support. Unknown versions retain useful offline analysis; return missing evidence for affected version-dependent procedures instead of selecting a nearest version.

## Decision workflow

1. Locate the failure layer: TLS/transport, authentication, Run:ai authorization, Kubernetes authorization or admission. A 403 alone does not identify the enforcing system.
2. For Run:ai, inspect the subject-role-scope assignment and enabled role permissions. For Kubernetes, evaluate the exact verb/resource/namespace for the current authorized principal; do not impersonate another user.
3. Compare the requested action with the smallest existing permission set. Check inheritance and cluster mapping without printing membership lists or tokens.
4. Report the denied operation, enforcing plane and missing evidence. Offer a minimal access-rule or RoleBinding proposal only within the requested scope.

## Read-only and offline execution

Live reads require an already authorized, explicit target. These examples are templates with synthetic names, not commands to run during repository validation. Replace each context, namespace and object only from confirmed task evidence. Never use the ambient current context, dump kubeconfig/Secrets/environment values, run exec/debug workloads, or include raw logs by default. Keep raw authorized evidence private; sanitize before reporting. Offline mode uses user-supplied sanitized snapshots and the same decision procedure without cluster or credential access.

Use the [documented read examples and interpretation](references/runbook.md#documented-read-examples) when a live read is already in scope. For changes, first prepare the [diff, impact, verification and recovery review](references/runbook.md#change-review); the skill itself grants no mutation authority.

## Failures and output

On permission denial, record the denied action/scope and continue with permitted or offline evidence; never broaden permissions. If a tool, resource type or schema is missing, name it and use supplied snapshots instead of guessing an interface. Preserve partial results and unavailable fields. Follow the documented cursor/continuation until complete within a declared page/time budget; otherwise label totals incomplete. Do not interpret an empty page, truncated response or timeout as absence. Retry a transient read at most once with the same scope; stop on repeated timeout or identity mismatch.

Return: verdict and impact; selected target aliases and independent component versions; evidence source/time window in UTC; observations versus hypotheses; missing/partial evidence and confidence; next minimal step. Mark advertised, usable, permitted and vendor-supported capability claims separately. Documentation review, deterministic fixture results, agent-behavior evaluation and live validation are separate evidence categories; never present one as another.

## Invocation examples

- English: “Explain this access denial without granting broader permissions.”
- pt-BR: “Explique esta negação de acesso sem ampliar permissões.”
