---
name: runai-tls-oidc
description: "Use when Run:ai HTTPS, certificate validation, OIDC issuer/audience/claims, SSO redirects, or Kubernetes authentication fails."
license: MIT
---

# Diagnose TLS and OIDC trust

Locate the trust or identity mismatch using sanitized evidence and propose a precise correction. It does not disable TLS validation, extract tokens or modify a control plane during diagnosis.

## Inputs and version selection

Scope: Run:ai Self-Hosted and its selected dependencies. Multi-Tenant/SaaS behavior needs separate matching evidence.

Exact failing hop and client; public certificate PEM/chain and metadata; expected DNS alias; observed UTC time; sanitized issuer/audience/redirect/claim configuration; component versions; error text with tokens removed.

Select Run:ai SSO and cluster-authentication instructions separately. OIDC client configuration, Kubernetes distribution flags, TLS library and container trust stores vary independently. Use the packaged [source and version profile](references/runbook.md#source-and-version-profile); local declarations carry provenance but cannot override contradictory observations, grant permission or establish vendor support. Unknown versions retain useful offline analysis; return missing evidence for affected version-dependent procedures instead of selecting a nearest version.

## Decision workflow

1. Map the actual hop: browser→ingress, Run:ai→IdP, cluster→control plane or CLI→Kubernetes API. Locate where the presented certificate is verified.
2. Offline, inspect certificate validity, SAN and chain relationships against the expected name/time. Distinguish a wrong leaf, missing intermediate and untrusted root; do not treat a valid date as full chain verification.
3. Compare OIDC issuer, audience/client ID, redirect URI and subject/group claim mapping from redacted configuration. Record clock skew and signing-key discovery availability without collecting a bearer token.
4. Check the failing process's trust store and deployment mount/reload path. Host trust changes do not automatically update containers, Java stores or application-specific CA bundles.

## Read-only and offline execution

Live reads require an already authorized, explicit target. These examples are templates with synthetic names, not commands to run during repository validation. Replace each context, namespace and object only from confirmed task evidence. Never use the ambient current context, dump kubeconfig/Secrets/environment values, run exec/debug workloads, or include raw logs by default. Keep raw authorized evidence private; sanitize before reporting. Offline mode uses user-supplied sanitized snapshots and the same decision procedure without cluster or credential access.

Use the [documented read examples and interpretation](references/runbook.md#documented-read-examples) when a live read is already in scope. For changes, first prepare the [diff, impact, verification and recovery review](references/runbook.md#change-review); the skill itself grants no mutation authority.

## Failures and output

On permission denial, record the denied action/scope and continue with permitted or offline evidence; never broaden permissions. If a tool, resource type or schema is missing, name it and use supplied snapshots instead of guessing an interface. Preserve partial results and unavailable fields. Follow the documented cursor/continuation until complete within a declared page/time budget; otherwise label totals incomplete. Do not interpret an empty page, truncated response or timeout as absence. Retry a transient read at most once with the same scope; stop on repeated timeout or identity mismatch.

Return: verdict and impact; selected target aliases and independent component versions; evidence source/time window in UTC; observations versus hypotheses; missing/partial evidence and confidence; next minimal step. Mark advertised, usable, permitted and vendor-supported capability claims separately. Documentation review, deterministic fixture results, agent-behavior evaluation and live validation are separate evidence categories; never present one as another.

## Invocation examples

- English: “Diagnose this OIDC certificate error using only the public certificate and redacted configuration.”
- pt-BR: “Diagnostique este erro de certificado OIDC usando apenas o certificado público e a configuração sanitizada.”

## Packaged helper

Use the [local helper and input contract](references/helpers.md) for repeatable offline analysis.
