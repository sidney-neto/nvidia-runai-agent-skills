---
name: runai-nim-serving
description: "Use when selecting or diagnosing a NVIDIA NIM model profile on Run:ai, including hardware compatibility, model-cache preparation, startup readiness or endpoint exposure."
license: MIT
---

# Review NVIDIA NIM serving

Validate a pinned NIM image/profile and the Run:ai deployment path, then prepare a bounded serving proposal. It does not retrieve NGC credentials, accept model terms or pull/deploy images without task authorization.

## Inputs and version selection

Scope: Run:ai Self-Hosted and its selected dependencies. Multi-Tenant/SaaS behavior needs separate matching evidence.

NIM product/version and image digest; model/revision; actual profile ID and compatibility output; GPU/driver/CUDA; Run:ai workload type/version; cache/storage requirements; readiness events and latency/concurrency goals.

The packaged NIM LLM references cover 1.10.0 and the Run:ai integration reference covers v3.0. Other NIM families/builds require their own support/profile evidence; a profile name from one container is not portable to another. Use the packaged [source and version profile](references/runbook.md#source-and-version-profile); local declarations carry provenance but cannot override contradictory observations, grant permission or establish vendor support. Unknown versions retain useful offline analysis; return missing evidence for affected version-dependent procedures instead of selecting a nearest version.

## Decision workflow

1. Identify whether the deployment uses Run:ai native NIM integration, an ordinary container workload or NIM Operator. Confirm its installed CRDs/interfaces rather than mixing these deployment routes.
2. Compare exact NIM image, model, hardware and profile compatibility evidence. A profile advertised by documentation is not proof it is runnable on this node or permitted by model licensing/access.
3. Check cache capacity/persistence, image/model access, startup stage, resources and effective policy. Distinguish download/compile delay from crash loops or a ready process with a broken route.
4. Produce a profile/resource/cache/endpoint proposal and a staged validation plan. Keep NGC keys and model contents outside reports and repository fixtures.

## Read-only and offline execution

Live reads require an already authorized, explicit target. These examples are templates with synthetic names, not commands to run during repository validation. Replace each context, namespace and object only from confirmed task evidence. Never use the ambient current context, dump kubeconfig/Secrets/environment values, run exec/debug workloads, or include raw logs by default. Keep raw authorized evidence private; sanitize before reporting. Offline mode uses user-supplied sanitized snapshots and the same decision procedure without cluster or credential access.

Use the [documented read examples and interpretation](references/runbook.md#documented-read-examples) when a live read is already in scope. For changes, first prepare the [diff, impact, verification and recovery review](references/runbook.md#change-review); the skill itself grants no mutation authority.

## Failures and output

On permission denial, record the denied action/scope and continue with permitted or offline evidence; never broaden permissions. If a tool, resource type or schema is missing, name it and use supplied snapshots instead of guessing an interface. Preserve partial results and unavailable fields. Follow the documented cursor/continuation until complete within a declared page/time budget; otherwise label totals incomplete. Do not interpret an empty page, truncated response or timeout as absence. Retry a transient read at most once with the same scope; stop on repeated timeout or identity mismatch.

Return: verdict and impact; selected target aliases and independent component versions; evidence source/time window in UTC; observations versus hypotheses; missing/partial evidence and confidence; next minimal step. Mark advertised, usable, permitted and vendor-supported capability claims separately. Documentation review, deterministic fixture results, agent-behavior evaluation and live validation are separate evidence categories; never present one as another.

## Invocation examples

- English: “Review this NIM profile and startup evidence for deployment on Run:ai.”
- pt-BR: “Revise este perfil NIM e as evidências de inicialização para implantação no Run:ai.”
