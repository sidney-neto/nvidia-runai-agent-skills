# nvidia-runai-agent-skills

Version-aware agent skills for NVIDIA Run:ai Self-Hosted administration, GPU quotas, governance, and troubleshooting across Kubernetes, GPU Operator, NVIDIA NIM, and vLLM.

**22 portable skills**, with inspection and planning as the default. Independent
community project; not endorsed by NVIDIA. No server or cluster deployment.

[Português](README.pt-BR.md) · [Skill catalog](docs/catalog.md) ·
[Installation and clients](docs/installation.md) · [Compatibility](docs/compatibility.md)

## Install a skill

From your destination project, with Node/npm available:

```sh
npx skills@1.7.2 add sidney-neto/nvidia-runai-agent-skills \
  --skill runai-context-discovery --agent codex --copy
```

Review existing same-name skills before installing. Replace `codex` with
`claude-code`, `openclaw`, `hermes-agent`, `gemini-cli`, `github-copilot`, `cursor`
or `opencode` as appropriate. This installs instructions and packaged resources;
Python development dependencies are not needed just to install a skill.

The [installation guide](docs/installation.md) covers user/project scope,
installation without npm, native OpenClaw/Hermes commands, existing NemoClaw
sandboxes, updates and removal. Grok Bot has a documented manual adaptation path;
GitHub package import there is unverified. Client file placement tests do not
establish agent execution or universal compatibility.

For repository-local Codex use, clone the repository and open it in Codex.
Checked-in `.agents/skills` links point to the canonical `skills/` directories.
Every skill can also be copied individually with its references, scripts, schemas
and legal notices; no mandatory repository runtime is required.

## First use

Select `$runai-context-discovery` in Codex CLI/IDE, or
`/runai-context-discovery` in Claude Code, and ask:

> Analyze this skill's packaged assets/example.snapshot.json offline. Preserve
> missing versions and identify evidence gaps. Do not access a cluster.

Ask for other focused workflows by name:

- **Quotas:** “Use runai-quota-capacity-planning to audit project and department quotas without changes.”
- **Pending:** “Use runai-scheduling-diagnostics to explain why this workload remains Pending.”
- **TLS/OIDC:** “Use runai-tls-oidc to diagnose this x509 error after certificate replacement.”
- **Upgrade:** “Use runai-upgrade-readiness to plan the installed-to-target transition, preserving workloads and volumes.”
- **vLLM:** “Use runai-vllm-serving to review this 32K context and memory budget.”

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
