---
name: nvidia-gpu-operator
description: "Use when NVIDIA GPU Operator components, GPU device resources, driver/toolkit integration, MIG or device-plugin configuration are preventing workloads from using GPUs."
license: MIT
---

# Diagnose GPU Operator readiness

Locate the failing GPU enablement component and propose a version-matched correction. It does not install drivers, change sharing modes or run GPU stress workloads during diagnosis.

## Inputs and version selection

Scope: Run:ai Self-Hosted and its selected dependencies. Multi-Tenant/SaaS behavior needs separate matching evidence.

Operator/chart/version and installation mode; GPU/OS/kernel/runtime versions; namespace and named component Pods/DaemonSets; node resource observations; sanitized component status; relevant Run:ai release.

The packaged Operator reference covers 25.3.4 concepts. Any concrete procedure for a different installed version needs its own reviewed support and configuration sources; do not treat latest docs or the Run:ai v3.0 minimum as a tested operator configuration. Use the packaged [source and version profile](references/runbook.md#source-and-version-profile); local declarations carry provenance but cannot override contradictory observations, grant permission or establish vendor support. Unknown versions retain useful offline analysis; return missing evidence for affected version-dependent procedures instead of selecting a nearest version.

## Decision workflow

1. Map the dependency chain from driver through container toolkit/runtime, device plugin or DRA path, feature discovery and monitoring. Confirm which installation owns each component.
2. Compare selected component desired/ready status and node-advertised resources. Driver availability, resource advertisement and successful container access are separate observations.
3. Check GPU mode, MIG/sharing configuration and runtime requirements against exact versions. A time-slicing replica count is not a physical GPU count or memory-isolation guarantee.
4. Identify the first failed dependency and propose the smallest component-specific next check. Do not reinstall the full operator to mask an unresolved driver/kernel or permission problem.

## Read-only and offline execution

Live reads require an already authorized, explicit target. These examples are templates with synthetic names, not commands to run during repository validation. Replace each context, namespace and object only from confirmed task evidence. Never use the ambient current context, dump kubeconfig/Secrets/environment values, run exec/debug workloads, or include raw logs by default. Keep raw authorized evidence private; sanitize before reporting. Offline mode uses user-supplied sanitized snapshots and the same decision procedure without cluster or credential access.

Use the [documented read examples and interpretation](references/runbook.md#documented-read-examples) when a live read is already in scope. For changes, first prepare the [diff, impact, verification and recovery review](references/runbook.md#change-review); the skill itself grants no mutation authority.

## Failures and output

On permission denial, record the denied action/scope and continue with permitted or offline evidence; never broaden permissions. If a tool, resource type or schema is missing, name it and use supplied snapshots instead of guessing an interface. Preserve partial results and unavailable fields. Follow the documented cursor/continuation until complete within a declared page/time budget; otherwise label totals incomplete. Do not interpret an empty page, truncated response or timeout as absence. Retry a transient read at most once with the same scope; stop on repeated timeout or identity mismatch.

Return: verdict and impact; selected target aliases and independent component versions; evidence source/time window in UTC; observations versus hypotheses; missing/partial evidence and confidence; next minimal step. Mark advertised, usable, permitted and vendor-supported capability claims separately. Documentation review, deterministic fixture results, agent-behavior evaluation and live validation are separate evidence categories; never present one as another.

## Invocation examples

- English: “Find why this node is Ready but advertises no NVIDIA GPU resources.”
- pt-BR: “Identifique por que este nó está Ready, mas não anuncia recursos de GPU NVIDIA.”
