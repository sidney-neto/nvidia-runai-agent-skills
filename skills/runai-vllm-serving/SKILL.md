---
name: runai-vllm-serving
description: "Use when planning or diagnosing vLLM serving on Run:ai, especially GPU memory fit, KV cache, concurrency, context length, tensor parallelism or readiness."
license: MIT
---

# Budget and review vLLM serving

Create a memory and placement budget plus a small serving-config proposal. It does not launch a model, download weights, spend GPU capacity or promise throughput from an offline estimate.

## Inputs and version selection

Scope: Run:ai Self-Hosted and its selected dependencies. Multi-Tenant/SaaS behavior needs separate matching evidence.

Pinned vLLM/image and model revision; architecture/layers/KV heads/head size; weight and KV dtype; quantization evidence; usable per-device VRAM or fraction; TP/PP; context/concurrency targets; measured overhead and latency objectives.

The packaged argument reference is vLLM 0.10.2. Run:ai, CUDA/driver, GPU model and model architecture compatibility require separate evidence. Do not apply these flags to an unknown vLLM build. Use the packaged [source and version profile](references/runbook.md#source-and-version-profile); local declarations carry provenance but cannot override contradictory observations, grant permission or establish vendor support. Unknown versions retain useful offline analysis; return missing evidence for affected version-dependent procedures instead of selecting a nearest version.

## Decision workflow

1. Resolve model/image revisions and the actual per-device memory boundary, including Run:ai fraction and driver reserve. Weight precision does not determine KV-cache precision.
2. Budget weights, KV cache, runtime/activation/graph overhead and headroom separately per device. Include concurrent prompt plus generated tokens, not only one request or the advertised context limit.
3. Check TP/PP sharding and replicated components against the architecture and engine. TP does not automatically divide every byte equally; KV heads may be replicated and topology can dominate latency.
4. Compare proposed context, sequence limit and memory controls with the budget. Return fits estimate, exceeds budget or unknown; identify the authorized canary needed to validate memory and performance.

## Read-only and offline execution

Live reads require an already authorized, explicit target. These examples are templates with synthetic names, not commands to run during repository validation. Replace each context, namespace and object only from confirmed task evidence. Never use the ambient current context, dump kubeconfig/Secrets/environment values, run exec/debug workloads, or include raw logs by default. Keep raw authorized evidence private; sanitize before reporting. Offline mode uses user-supplied sanitized snapshots and the same decision procedure without cluster or credential access.

Use the [documented read examples and interpretation](references/runbook.md#documented-read-examples) when a live read is already in scope. For changes, first prepare the [diff, impact, verification and recovery review](references/runbook.md#change-review); the skill itself grants no mutation authority.

## Failures and output

On permission denial, record the denied action/scope and continue with permitted or offline evidence; never broaden permissions. If a tool, resource type or schema is missing, name it and use supplied snapshots instead of guessing an interface. Preserve partial results and unavailable fields. Follow the documented cursor/continuation until complete within a declared page/time budget; otherwise label totals incomplete. Do not interpret an empty page, truncated response or timeout as absence. Retry a transient read at most once with the same scope; stop on repeated timeout or identity mismatch.

Return: verdict and impact; selected target aliases and independent component versions; evidence source/time window in UTC; observations versus hypotheses; missing/partial evidence and confidence; next minimal step. Mark advertised, usable, permitted and vendor-supported capability claims separately. Documentation review, deterministic fixture results, agent-behavior evaluation and live validation are separate evidence categories; never present one as another.

## Invocation examples

- English: “Budget this vLLM model for the given GPU fraction, context and concurrency.”
- pt-BR: “Calcule o orçamento de memória deste modelo vLLM para a fração GPU, contexto e concorrência informados.”

## Packaged helper

Use the [local helper and input contract](references/helpers.md) for repeatable offline analysis.
