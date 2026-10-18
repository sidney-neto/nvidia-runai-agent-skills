---
name: runai-mcp-integration
description: "Use when connecting an AI client to the official Run:ai MCP server, checking available read tools, or diagnosing MCP identity, transport, schema, or authorization problems."
license: MIT
---

# Validate optional MCP access

Assess an optional MCP connection and produce a scoped configuration proposal. It is not a custom MCP server implementation, credential provisioner or prerequisite for the other skills.

## Inputs and version selection

Scope: Run:ai Self-Hosted and its selected dependencies. Multi-Tenant/SaaS behavior needs separate matching evidence.

Client/version; official server source/revision and version; transport; expected Run:ai cluster; authorized read scope; sanitized configuration with secret values omitted; observed tool schemas.

Record MCP protocol, server build and Run:ai product versions independently. A v3.0 tools page documents names and intent, not universal argument schemas or availability on older servers. Use the packaged [source and version profile](references/runbook.md#source-and-version-profile); local declarations carry provenance but cannot override contradictory observations, grant permission or establish vendor support. Unknown versions retain useful offline analysis; return missing evidence for affected version-dependent procedures instead of selecting a nearest version.

## Decision workflow

1. Verify server provenance and the exact deployment/connection documentation. Separate the documentation-search MCP endpoint from the operational Run:ai server; a docs connector has no cluster authority.
2. Inspect advertised tool names and input/output schemas. Categorize read, write and credential tools before invoking anything. Never infer safety from a read-like name alone.
3. Use an authorized read identity check, then one bounded cluster-specific read using the observed schema. Confirm principal, returned cluster, pagination and permissions. Do not test a mutation to prove connectivity.
4. Report advertised, usable, permitted and vendor-supported status separately. If MCP is absent, continue with sanitized snapshots or authorized Kubernetes reads.

## Read-only and offline execution

Live reads require an already authorized, explicit target. These examples are templates with synthetic names, not commands to run during repository validation. Replace each context, namespace and object only from confirmed task evidence. Never use the ambient current context, dump kubeconfig/Secrets/environment values, run exec/debug workloads, or include raw logs by default. Keep raw authorized evidence private; sanitize before reporting. Offline mode uses user-supplied sanitized snapshots and the same decision procedure without cluster or credential access.

Use the [documented read examples and interpretation](references/runbook.md#documented-read-examples) when a live read is already in scope. For changes, first prepare the [diff, impact, verification and recovery review](references/runbook.md#change-review); the skill itself grants no mutation authority.

## Failures and output

On permission denial, record the denied action/scope and continue with permitted or offline evidence; never broaden permissions. If a tool, resource type or schema is missing, name it and use supplied snapshots instead of guessing an interface. Preserve partial results and unavailable fields. Follow the documented cursor/continuation until complete within a declared page/time budget; otherwise label totals incomplete. Do not interpret an empty page, truncated response or timeout as absence. Retry a transient read at most once with the same scope; stop on repeated timeout or identity mismatch.

Return: verdict and impact; selected target aliases and independent component versions; evidence source/time window in UTC; observations versus hypotheses; missing/partial evidence and confidence; next minimal step. Mark advertised, usable, permitted and vendor-supported capability claims separately. Documentation review, deterministic fixture results, agent-behavior evaluation and live validation are separate evidence categories; never present one as another.

## Invocation examples

- English: “Check whether my Run:ai MCP connection can safely read the selected project.”
- pt-BR: “Verifique se a conexão MCP do Run:ai pode ler o projeto selecionado.”
