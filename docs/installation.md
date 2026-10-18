# Installation and usage

Reviewed **2026-10-18** against the official sources linked below. Client docs are
moving references, not promises about every installed release. Check your client's
version and policy. Skills supply instructions; tools, permissions and dependencies
come from the execution environment. Installing these skills enables no MCP server
or cluster access.

## Choose a client

**D** = mechanism documented; **P** = selected-skill file placement tested with
`skills@1.7.2 --copy` in a temporary project; **A** = agent execution. No A tests
were run. P does not establish native discovery, trust approval or tool execution.

| Client / official reference | Project location | User location | Evidence |
|---|---|---|---|
| [Codex](https://learn.chatgpt.com/docs/build-skills) | `.agents/skills/` | `~/.agents/skills/` | D, P |
| [Claude Code](https://code.claude.com/docs/en/skills) | `.claude/skills/` | `~/.claude/skills/` | D, P |
| [OpenClaw](https://docs.openclaw.ai/tools/skills) | Selected workspace `skills/` | `~/.openclaw/skills/` | D, P; native installer untested |
| [Hermes Agent](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills) | `.hermes/skills/` or `.agents/skills/` | Profile `~/.hermes/skills/` | D, P; native installer untested |
| [NVIDIA NemoClaw](https://github.com/NVIDIA/NemoClaw) | Selected runtime inside existing sandbox | Not a host-global skill installation | D only |
| [Grok Bot](https://docs.x.ai/grok-bot/skills-routines-and-automations) | None established | Account-wide private library across Bots, managed in the app | Manual adaptation only |
| [Gemini CLI](https://geminicli.com/docs/cli/using-agent-skills/) | `.gemini/skills/` or `.agents/skills/` | `~/.gemini/skills/` or `~/.agents/skills/` | D, P |
| [GitHub Copilot](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills) | `.github/skills/`, `.claude/skills/` or `.agents/skills/` | `~/.copilot/skills/` or `~/.agents/skills/` | D, P |
| [Cursor](https://cursor.com/docs/skills) | `.cursor/skills/` or `.agents/skills/` | `~/.cursor/skills/` or `~/.agents/skills/` | D, P; local files only |
| [OpenCode](https://opencode.ai/docs/skills/) | `.opencode/skills/` or `.agents/skills/` | `~/.config/opencode/skills/` or `~/.agents/skills/` | D, P |

## Selected-skill installation

Run from the **destination project**, not this library's checkout. With Node/npm
available, the [skills CLI](https://github.com/vercel-labs/skills) can install one
complete skill. Review existing same-name skills first: this external installer
can replace them. Leave confirmation prompts enabled.

```sh
npx skills@1.7.2 add sidney-neto/nvidia-runai-agent-skills \
  --skill runai-context-discovery --agent codex --copy
```

Use `--agent claude-code`, `openclaw`, `hermes-agent`, `gemini-cli`,
`github-copilot`, `cursor` or `opencode` for another client. For OpenClaw the current
directory must be the intended workspace; prefer its native installer below when
selecting an agent. Add `--global` only for a deliberate user-scope installation.
Use `--list` to inspect available skills; omit `--skill` to choose interactively.
Python packages are unnecessary for instruction-only consumption.

For a CLI-managed project installation, review changes before updating; select
the same installation scope and agent when removing:

```sh
npx skills@1.7.2 update runai-context-discovery --project
```

To remove that selected installation:

```sh
npx skills@1.7.2 remove runai-context-discovery --agent codex
```

Use `--global` instead of `--project` for user-scope updates, and add `--global`
for user-scope removals. Do not use an all-skills removal. The CLI makes network
requests; `DISABLE_TELEMETRY=1` disables its telemetry. It is optional tooling,
not a repository dependency.

### Without Node/npm

Clone or download a reviewed revision. Our existing stdlib copy helper refuses
to overwrite a destination and does not edit client configuration:

```sh
git clone https://github.com/sidney-neto/nvidia-runai-agent-skills.git
cd nvidia-runai-agent-skills
python3 scripts/install_skill.py runai-context-discovery --destination /path/to/project/.agents/skills
```

For Codex user scope use `--destination "$HOME/.agents/skills"`; for Claude Code
use `/path/to/project/.claude/skills` or `"$HOME/.claude/skills"`. The table supplies
other documented roots. Copy the **whole canonical folder**, including references,
schemas, scripts and legal notices, if using a file manager instead.

For manual copies, update by reviewing a new checkout, backing up the installed
folder outside any skill discovery root, then installing into the vacant target.
Removal means moving only that named installed folder out of the discovery root.
Restart/reload the client and confirm it is absent. These copies are not tracked
by a native hub or the skills CLI; do not mix update mechanisms.

### Codex and Claude Code

In Codex CLI/IDE, inspect `/skills` or select `$runai-context-discovery`; ask it to
analyze the packaged `assets/example.snapshot.json` offline. In the library checkout,
Codex can use the checked-in `.agents/skills` links without copying. Restart if
discovery has not refreshed. A repository path is not a deployment to a remote
Codex environment; make files available there separately.

For Claude Code, the explicit CLI example is:

```sh
npx skills@1.7.2 add sidney-neto/nvidia-runai-agent-skills \
  --skill runai-context-discovery --agent claude-code --copy
```

Run `/reload-skills`, then `/runai-context-discovery Analyze the packaged synthetic
snapshot offline.` Project trust and managed policy still apply. Local personal
skills do not automatically appear in Claude.ai/Cowork or cloud sessions.
[Claude.ai custom-skill uploads](https://support.claude.com/en/articles/12512180-use-skills-in-claude)
and [Claude API skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
are separate mechanisms; neither was tested here. Supply all referenced files and
check runtime/dependency restrictions before using helpers. No plugin is required
for the local folder installations above.

### OpenClaw

From a reviewed clone, target an existing agent explicitly:

```sh
openclaw skills install ./skills/runai-context-discovery --agent <agent-id>
openclaw skills info runai-context-discovery --agent <agent-id>
openclaw skills check --agent <agent-id>
```

Use `--global` instead of `--agent` for shared scope. Invoke `Use
$runai-context-discovery to analyze the packaged synthetic snapshot offline.`
Source roots must contain SKILL.md. Project symlinks escaping their configured
skill root may be rejected; use canonical directories or copies, not this
repository's `.agents/skills` links. Eligibility does not grant tool permission.

ClawHub updates do not update local/Git installs. Review and back up local changes
before explicitly reinstalling the named skill with `--force`. No local-install
uninstall command is established by the [CLI reference](https://docs.openclaw.ai/cli/skills);
move only its installed folder outside discovery and verify absence. Supporting
files and helper dependencies must be available inside any execution sandbox.

### Hermes Agent

For Nous Research's agent runtime (not Hermes model weights), the native hub path is:

```sh
hermes skills inspect sidney-neto/nvidia-runai-agent-skills/skills/runai-context-discovery
hermes skills install sidney-neto/nvidia-runai-agent-skills/skills/runai-context-discovery
hermes skills list --source hub
```

For a later update, run `hermes skills update runai-context-discovery`. To remove
that hub installation, run `hermes skills uninstall runai-context-discovery`.

These manage the current user/profile installation. Preserve community-source
scanner decisions; do not bypass them. Updates normally preserve locally changed
skills. Project copies require `hermes skills trust` from the reviewed project;
`hermes skills untrust` revokes that trust. Invoke `/runai-context-discovery Analyze
the packaged synthetic snapshot offline.` Do not change global external-directory
configuration just to consume this library. Native commands are documented, untested.

### NVIDIA NemoClaw

NemoClaw wraps agents in NVIDIA OpenShell. Use an **existing** sandbox and identify
its runtime first; this library does not provision one. For OpenClaw:

```sh
nemoclaw <sandbox-name> skill install ./skills/runai-context-discovery
nemoclaw <sandbox-name> skill list
```

To remove it later, run `nemoclaw <sandbox-name> skill remove runai-context-discovery`.

The [OpenClaw commands](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/reference/commands)
place skills under `/sandbox/.openclaw/workspace/skills/`. Install can replace the
same name: back up reviewed local changes first. For a Hermes sandbox, use the
same actions through `nemohermes`; its root is `/sandbox/.hermes/skills/`, and an
existing name must be explicitly removed before replacement. See
[NemoHermes commands](https://docs.nvidia.com/nemoclaw/user-guide/hermes/reference/commands).

Use canonical source folders: staging rejects symlinks. Confirm native discovery
and invoke the runtime's prompt above in a fresh session; placement alone does not
prove activation. Removal can leave other copies active. Dependencies are not
installed with the skill. [Sandbox constraints](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/reference/architecture)
restrict writable locations and network egress; prepare helpers through an approved
in-sandbox environment/image workflow. Never loosen policy as an installation fix.

### Grok Bot and other hosted surfaces

Grok Bot documents saving private workflows and selecting them with `/`. Its guide
does **not** establish arbitrary GitHub/ZIP Agent Skills import, automatic relative
reference loading or Python helper dependency installation. Use this limited
manual adaptation, supplying the required files through
[attachments](https://docs.x.ai/grok-bot/files-and-results):

> Read the attached runai-context-discovery instructions, referenced runbook and
> synthetic snapshot. Analyze only these files. Do not access a cluster or infer
> missing versions. List any unavailable resources. Do not claim helper validation
> unless you can actually run the packaged validator with its dependencies.

Review the result before asking Grok Bot to save the workflow as a private skill.
Manage it under **Connect apps → Your plugins → Manage plugins and skills → Private
skills**. Exact update/delete commands are not documented in the reviewed guide;
use controls available in your account. This is not native package installation.

[Grok Build](https://docs.x.ai/build/features/skills-plugins-marketplaces) separately
supports `.grok/skills/` and `~/.grok/skills/`, `/skills` and `/<skill-name>`. Those
paths do not establish Grok Bot, ordinary Grok chat or xAI API support. Similarly,
local Codex skill placement is not a ChatGPT web plugin installation. This project
ships no hosted-client plugin manifests or API integration.

### Other local clients

Use the selected-skill command with the table's CLI identifier. Gemini CLI exposes
`/skills list` and `/skills reload`; workspace trust is required. Cursor shows
skills in **Customize → Skills**; its GitHub marketplace import requires a separate
plugin, which this repository does not ship. Local files are not automatically
available in cloud agents. Copilot and OpenCode can discover `.agents/skills`;
request the skill by name and check the client actually loaded it. Honor client
trust/tool restrictions. CLI-managed update/removal follows the common commands.

## Offline helpers and first use

All helpers require Python 3.11+; snapshot validation additionally needs the
packaged jsonschema dependency. Install dependencies before going offline, in an
environment visible to the agent's Python process. For a selected installed skill:

```sh
python3.12 -m venv /path/to/helper-venv
/path/to/helper-venv/bin/python -m pip install -r /path/to/runai-context-discovery/requirements.txt
/path/to/helper-venv/bin/python /path/to/runai-context-discovery/scripts/snapshot.py \
  /path/to/runai-context-discovery/assets/example.snapshot.json
```

This is local validation, not an agent execution test. Other helpers use the
standard library. From a clone, examples include:

```sh
python3 skills/runai-quota-capacity-planning/scripts/quota.py examples/eight-gpu.snapshot.json --format text
python3 skills/runai-scheduling-diagnostics/scripts/fit.py examples/eight-gpu.snapshot.json
python3 skills/runai-tls-oidc/scripts/tls_evidence.py examples/tls-evidence.json
python3 skills/runai-vllm-serving/scripts/budget.py examples/vllm-budget.json
python3 skills/runai-upgrade-readiness/scripts/readiness.py examples/upgrade-plan.json --upgrade
python3 skills/runai-support-report/scripts/report.py examples/incident.json
```

The readiness example intentionally exits 2 for missing prerequisites. The eight-GPU
example has project quotas totaling 12, separately reported department quota 8,
fragmentation and one non-HA control plane. Inputs are synthetic local contracts,
not deployment manifests. See [example report](../examples/executive-report.md).

| Workflow | English prompt | Prompt em português |
|---|---|---|
| Discovery | Use runai-context-discovery to analyze this exported snapshot offline. | Detecte a versão deste snapshot e indique lacunas sem acessar o cluster. |
| Quotas | Use runai-quota-capacity-planning to audit project and department quotas without changes. | Audite as quotas por projeto e departamento sem alterar o cluster. |
| Scheduling | Use runai-scheduling-diagnostics to explain why this workload remains Pending. | Explique por que este workload continua Pending. |
| TLS/OIDC | Use runai-tls-oidc to diagnose this OIDC x509 error after certificate replacement. | Diagnostique o erro x509 no OIDC após a troca do certificado. |
| Upgrade | Use runai-upgrade-readiness to plan the installed-to-target transition, preserving workloads and volumes. | Prepare um plano da versão instalada para a versão-alvo informada, preservando workloads e volumes. |
| vLLM | Use runai-vllm-serving to review this 32K context and memory budget. | Revise esta configuração do vLLM para contexto de 32K. |

Supply exact file paths in the agent's environment. For unknown releases, request
version-independent analysis and explicit limitations. Live integrations require
separate authorization, verified interfaces and scoped credentials; never obtain
those just to run the examples.

## Validation status

On 2026-10-18, `skills@1.7.2` discovered all 22 skills from the local checkout and
copied `runai-context-discovery` for the eight P clients in one temporary project.
The copies were checked byte-for-byte against canonical resources; scoped removal
preserved other clients' copies. Standalone snapshot validation also ran in a fresh
Python environment with only the skill's requirements. No global client configuration
was edited. Native OpenClaw/Hermes/NemoClaw installers and Grok Bot UI were not run.

`make check` independently copies **every** skill outside the repository, checks
packaged resources and runs helper checks. See [contributor validation](../CONTRIBUTING.md#what-the-checks-establish).
Agent invocation, sandbox behavior, hosted uploads, live clusters and GPU workflows
remain untested. Installation evidence is not operational compatibility evidence.
