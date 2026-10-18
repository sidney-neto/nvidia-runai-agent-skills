---
name: runai-gpu-sharing
description: "Use when planning or diagnosing Run:ai GPU memory fractions, compute sharing, MIG interaction, device accounting, or fraction migration."
license: MIT
---

# Review GPU sharing and fractions

Separate memory allocation, compute behavior and device accounting, then assess the exact supported sharing path. It does not assume that a memory fraction grants the same compute percentage.

## Inputs and version selection

Scope: Run:ai Self-Hosted and its selected dependencies. Multi-Tenant/SaaS behavior needs separate matching evidence.

Run:ai/driver/CUDA/GPU Operator versions per node; GPU model and usable VRAM; workload/container type; actual submission path; requested/limited memory, device count, compute mode and current occupants.

The packaged Run:ai evidence is v3.0; its CUDA-based fractions must not be projected onto v2.x. The separate GPU Operator 25.3.4 time-slicing reference is not a v3.0 Run:ai compatibility endorsement. Use the packaged [source and version profile](references/runbook.md#source-and-version-profile); local declarations carry provenance but cannot override contradictory observations, grant permission or establish vendor support. Unknown versions retain useful offline analysis; return missing evidence for affected version-dependent procedures instead of selecting a nearest version.

## Decision workflow

1. Identify the mechanism: Run:ai fractions, MIG, GPU Operator time-slicing or another layer. Preserve units and per-device counts; do not combine replicas and physical cards.
2. Check exact hardware/software and node prerequisites against the selected release. For v3.0 fractions, review CUDA 13.4+, driver r615+, GPU Operator 26.7.1+, cgroup v2 and NRI-plugin requirements in the linked source. These are minimum prerequisites, not a supported-version range; the reviewed v3.0 support matrix caps GPU Operator at 26.7.1.
3. Calculate memory per requested device with reserve/headroom, then evaluate compute mode independently. For reviewed v3.0 behavior, the occupied GPU's compute mode can exclude a different-mode workload despite spare memory.
4. Compare submission-path annotations/fields, container naming and effective policy. For upgrades, identify dynamic-fraction manifests needing migration and workloads requiring planned interruption.

## Read-only and offline execution

Live reads require an already authorized, explicit target. These examples are templates with synthetic names, not commands to run during repository validation. Replace each context, namespace and object only from confirmed task evidence. Never use the ambient current context, dump kubeconfig/Secrets/environment values, run exec/debug workloads, or include raw logs by default. Keep raw authorized evidence private; sanitize before reporting. Offline mode uses user-supplied sanitized snapshots and the same decision procedure without cluster or credential access.

Use the [documented read examples and interpretation](references/runbook.md#documented-read-examples) when a live read is already in scope. For changes, first prepare the [diff, impact, verification and recovery review](references/runbook.md#change-review); the skill itself grants no mutation authority.

## Failures and output

On permission denial, record the denied action/scope and continue with permitted or offline evidence; never broaden permissions. If a tool, resource type or schema is missing, name it and use supplied snapshots instead of guessing an interface. Preserve partial results and unavailable fields. Follow the documented cursor/continuation until complete within a declared page/time budget; otherwise label totals incomplete. Do not interpret an empty page, truncated response or timeout as absence. Retry a transient read at most once with the same scope; stop on repeated timeout or identity mismatch.

Return: verdict and impact; selected target aliases and independent component versions; evidence source/time window in UTC; observations versus hypotheses; missing/partial evidence and confidence; next minimal step. Mark advertised, usable, permitted and vendor-supported capability claims separately. Documentation review, deterministic fixture results, agent-behavior evaluation and live validation are separate evidence categories; never present one as another.

## Invocation examples

- English: “Explain whether a half-memory GPU fraction meets this serving workload's requirements.”
- pt-BR: “Explique se uma fração de metade da memória da GPU atende a este workload de inferência.”
