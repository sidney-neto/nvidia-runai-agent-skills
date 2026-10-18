---
name: runai-networking
description: "Use when Run:ai UI/API or workload endpoints are unreachable, or DNS, ingress/service routing, NetworkPolicy, proxy or cluster-to-control-plane connectivity needs review."
license: MIT
---

# Trace workload and platform networking

Map one failing connection and locate the routing, policy or TLS layer. It does not expose a service publicly, disable policies, open firewall ranges or run unbounded network probes.

## Inputs and version selection

Scope: Run:ai Self-Hosted and its selected dependencies. Multi-Tenant/SaaS behavior needs separate matching evidence.

Exact source/destination aliases, port/protocol/path, expected TLS host, failing time, namespace/service/ingress names, endpoint readiness, CNI/ingress versions and redacted network-policy/routing evidence.

Select networking requirements for the actual Run:ai release and deployment model, plus CNI/ingress versions. Do not assume that a current Gateway API or ingress example matches an older installation. Use the packaged [source and version profile](references/runbook.md#source-and-version-profile); local declarations carry provenance but cannot override contradictory observations, grant permission or establish vendor support. Unknown versions retain useful offline analysis; return missing evidence for affected version-dependent procedures instead of selecting a nearest version.

## Decision workflow

1. Draw the specific flow: client→DNS/LB→ingress→Service→ready backend, or agent→control plane. Keep inbound routing and outbound dependency access separate.
2. Inspect the selected Service ports/selector and ready EndpointSlice conditions, then the supplied ingress/route host and path. A Service object alone does not prove usable backends.
3. Compare source/destination NetworkPolicy selection, CNI enforcement and external firewall/proxy rules. Distinguish DNS failure, TCP timeout, TLS error and HTTP routing/application error.
4. Report the narrowest evidenced break and a minimal route/policy proposal. If active probing is outside authorization, provide an offline flow matrix with unknown edges.

## Read-only and offline execution

Live reads require an already authorized, explicit target. These examples are templates with synthetic names, not commands to run during repository validation. Replace each context, namespace and object only from confirmed task evidence. Never use the ambient current context, dump kubeconfig/Secrets/environment values, run exec/debug workloads, or include raw logs by default. Keep raw authorized evidence private; sanitize before reporting. Offline mode uses user-supplied sanitized snapshots and the same decision procedure without cluster or credential access.

Use the [documented read examples and interpretation](references/runbook.md#documented-read-examples) when a live read is already in scope. For changes, first prepare the [diff, impact, verification and recovery review](references/runbook.md#change-review); the skill itself grants no mutation authority.

## Failures and output

On permission denial, record the denied action/scope and continue with permitted or offline evidence; never broaden permissions. If a tool, resource type or schema is missing, name it and use supplied snapshots instead of guessing an interface. Preserve partial results and unavailable fields. Follow the documented cursor/continuation until complete within a declared page/time budget; otherwise label totals incomplete. Do not interpret an empty page, truncated response or timeout as absence. Retry a transient read at most once with the same scope; stop on repeated timeout or identity mismatch.

Return: verdict and impact; selected target aliases and independent component versions; evidence source/time window in UTC; observations versus hypotheses; missing/partial evidence and confidence; next minimal step. Mark advertised, usable, permitted and vendor-supported capability claims separately. Documentation review, deterministic fixture results, agent-behavior evaluation and live validation are separate evidence categories; never present one as another.

## Invocation examples

- English: “Trace why this inference endpoint is unreachable using the sanitized routing snapshot.”
- pt-BR: “Investigue por que este endpoint de inferência está inacessível usando o snapshot de roteamento sanitizado.”
