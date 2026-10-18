# NVIDIA Run:ai Agent Skills

[![Offline validation](https://github.com/sidney-neto/nvidia-runai-agent-skills/actions/workflows/check.yml/badge.svg?branch=main)](https://github.com/sidney-neto/nvidia-runai-agent-skills/actions/workflows/check.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Helpers: Python 3.11+](https://img.shields.io/badge/helpers-Python%203.11%2B-3776AB.svg)](CONTRIBUTING.md#development-setup)
[![Format: Agent Skills](https://img.shields.io/badge/format-Agent%20Skills-76B900.svg)](https://agentskills.io/specification)

Version-aware agent skills for NVIDIA Run:ai Self-Hosted administration, GPU quotas, governance, and troubleshooting across Kubernetes, GPU Operator, NVIDIA NIM, and vLLM.

**22 focused skills · Offline evidence analysis · Version-aware procedures**

Inspect infrastructure, understand GPU capacity and prepare reviewable changes.
Start with sanitized snapshots; connect official tools only when the task requires
them. Independent community project, not endorsed by NVIDIA.

[Português](README.pt-BR.md) · [Skill catalog](docs/catalog.md) ·
[Installation](docs/installation.md) · [Compatibility](docs/compatibility.md) ·
[Contributing](CONTRIBUTING.md)

## Quick start

From your destination project, with Node/npm available:

```sh
npx skills@1.7.2 add sidney-neto/nvidia-runai-agent-skills \
  --skill runai-context-discovery --agent codex --copy
```

Review existing same-name skills before installing. This copies instructions and
resources; Python is only needed to run optional helpers and validation.
Use the client identifier below with `--agent` or follow its native setup guide.

| Client | Installation route |
|---|---|
| Codex | `--agent codex` |
| Claude Code | `--agent claude-code` |
| OpenClaw · Hermes Agent | `--agent openclaw` / `--agent hermes-agent`; native installers also documented |
| Gemini CLI · GitHub Copilot · Cursor · OpenCode | `--agent gemini-cli` / `github-copilot` / `cursor` / `opencode` |
| NVIDIA NemoClaw | Install into the selected runtime in an existing sandbox |
| Grok Bot | Manual adaptation with supplied files; package import unverified |

The [installation guide](docs/installation.md) covers project/user scope,
installation without npm, native commands, updates and removal. File placement
was tested for the eight CLI targets; agent execution was not. NemoClaw and Grok
Bot instructions have separate, documented limitations.

For repository-local Codex use, clone the repository and open it in Codex.
Checked-in `.agents/skills` links point to the canonical `skills/` directories.
Every skill can also be copied individually with its references, scripts, schemas
and legal notices; no mandatory repository runtime is required.

## First use

Select `$runai-context-discovery` in Codex CLI/IDE, or
`/runai-context-discovery` in Claude Code, and ask:

> Analyze this skill's packaged assets/example.snapshot.json offline. Preserve
> missing versions and identify evidence gaps. Do not access a cluster.

## Choose a workflow

| What you need | Start here |
|---|---|
| Identify versions, interfaces and evidence gaps | [Context discovery](skills/runai-context-discovery/SKILL.md) |
| Explain degraded nodes or cluster connectivity | [Cluster health](skills/runai-cluster-health/SKILL.md) |
| Audit project/department quotas without changes | [Quota and capacity](skills/runai-quota-capacity-planning/SKILL.md) |
| Explain why a workload remains Pending | [Scheduling diagnostics](skills/runai-scheduling-diagnostics/SKILL.md) |
| Diagnose OIDC x509 errors after certificate replacement | [TLS and OIDC](skills/runai-tls-oidc/SKILL.md) |
| Plan an installed-to-target upgrade, preserving workloads and volumes | [Upgrade readiness](skills/runai-upgrade-readiness/SKILL.md) |
| Review a 32K context and GPU memory budget | [vLLM serving](skills/runai-vllm-serving/SKILL.md) |

[Explore all 22 skills →](docs/catalog.md), including RBAC, policies, GPU sharing,
NIM, distributed workloads, storage, networking and recovery.

Supply sanitized evidence files and exact targets. See the guide for
[English/Portuguese prompts and optional Python helpers](docs/installation.md#offline-helpers-and-first-use).
Snapshot validation needs the skill's pinned jsonschema dependency; other helpers
use the standard library. The [synthetic eight-GPU snapshot](examples/eight-gpu.snapshot.json)
and [example report](examples/executive-report.md) need no live credentials or GPU.

## Scope and evidence

Any reported release can be investigated. Unknown versions retain useful offline
analysis; they never inherit the newest profile. Initial bounded profiles cover
Self-Hosted 2.26/3.0 fraction-limit differences and a documented component-staged
2.26 → 3.0 plan. These examples are not a global release allowlist. Related-stack
versions and documentation/fixture/agent/live evidence are separate in the
[compatibility matrix](docs/compatibility.md).

Official MCP is optional. Live operations require verified interfaces, explicit
targets and authorized scope. No credentials, writes or connections are enabled
by installation. Keep private snapshots/reports in ignored `.local/`; report
redaction is heuristic and requires review before sharing.

To add coverage, review the exact release's sources, add a bounded profile/reference
and positive/negative fixtures, then run `make check`. Do not rename the skill catalog.

## Contribute

[Development setup and validation](CONTRIBUTING.md) describe the optional Python
toolchain and `make check`. Tests are synthetic and offline after dependency setup;
agent behavior and live integration have not been tested. Source refresh is a
separate opt-in network operation.

[Security](SECURITY.md) · [Source ledger](docs/sources.json) ·
[Upstream provenance](docs/upstream-provenance.md) · [License](LICENSE) ·
[Attribution](THIRD_PARTY_NOTICES.md)
