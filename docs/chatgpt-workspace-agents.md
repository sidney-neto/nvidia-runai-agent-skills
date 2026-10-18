# ChatGPT Workspace Agents

[Português](chatgpt-workspace-agents.pt-BR.md) · [All clients](installation.md)

Workspace Agents combine agent-wide instructions, selected tools and reusable
skills. A skill supplies a focused procedure and supporting files; agent
instructions set the overall role and routing. Neither grants infrastructure
access. These packages are built and validated locally; **ChatGPT upload,
discovery and execution have not been tested**.

## Obtain one skill

When a maintainer publishes a [GitHub release](https://github.com/sidney-neto/nvidia-runai-agent-skills/releases),
download the chosen `nvidia-runai-<skill-name>.zip` plus `SHA256SUMS` and
`manifest.json`. Check its SHA-256 against the matching line, for example:

```sh
shasum -a 256 nvidia-runai-runai-context-discovery.zip
```

A checksum detects corruption; trust the repository and review the package too.
If there is no published package release, build locally. Do not upload GitHub's
source archive or the Actions artifact containing multiple skills.

For instruction-only use, no local Python setup is needed when downloading a ZIP.
Building and validating packages uses the [contributor environment](../CONTRIBUTING.md#development-setup):

```sh
python scripts/package_chatgpt_skills.py --list
python scripts/package_chatgpt_skills.py --skill runai-context-discovery --output dist/selected
python scripts/package_chatgpt_skills.py --all --validate-only --json
make package-chatgpt
make validate-chatgpt
```

Each `dist/chatgpt/<name>/skill.zip` has one `<name>/SKILL.md`, its existing
resources and legal notices, and generated `agents/openai.yaml`. Identical bytes
are available as uniquely named assets under `dist/chatgpt/release/`, with a
manifest and checksums. The builder discovers directories dynamically; no skill
count or Run:ai release list controls export.

Choose a fresh `--output` directory for a changed build; existing different files
are never overwritten. Repeating the same build into an identical output is safe.
Use `make package-chatgpt CHATGPT_OUTPUT=dist/review` to select another destination.
Generated output is ignored by Git. No dependency installation, helper execution,
network request, or credential-store access occurs during export; the CLI reads
local Git metadata for the manifest.

## Import and attach

In an eligible workspace, open **Plugins → Skills → Create → Upload from your
computer** and select one skill ZIP. Review any scan result. Workspace policy can
disable upload or require review; this repository cannot override it.
[Official Skills guidance](https://help.openai.com/en/articles/20001066-skills-in-chatgpt).

Open or create **NVIDIA Run:ai Infrastructure Expert** in Agents. In Agent Builder,
use the skills addition control (often **Add skill**) to select an available skill
or upload one. Test in **Preview** before saving changes; an existing live agent
uses **Update**. Exact labels may vary. The official guide confirms adding skills,
but does not establish every UI label or archive validation rule.
[Workspace Agents guide](https://help.openai.com/en/articles/20001143-chatgpt-workspace-agents-for-enterprise-and-business).

Start with context discovery. Attach only the workflows needed:

- `runai-context-discovery`, `runai-cluster-health`
- `runai-scheduling-diagnostics`, `runai-quota-capacity-planning`
- `runai-tls-oidc`, `nvidia-gpu-operator`
- `runai-vllm-serving`, `runai-upgrade-readiness`

The optional [agent instructions template](../examples/chatgpt-agent-instructions.md)
provides routing and response conventions. Each skill is uploaded separately so
its identity, review, attachment and updates remain independent.

## First use and runtime limits

Ask: “Analyze the packaged `assets/example.snapshot.json` offline. Identify the
environment, independent component versions and missing evidence.” Then try
“Explain why this workload stays Pending” with a sanitized snapshot. These test
automatic selection; explicitly name a skill when investigating routing errors.

Instruction-only review works from supplied evidence. Optional helpers need an
available Python 3.11+ execution tool; context snapshot validation also needs its
packaged `jsonschema==4.25.1` dependency. Do not assume ChatGPT installs it. Without
execution, reason through the runbook and clearly say schema validation or
deterministic calculations were not executed. Users can run the packaged helper
locally and supply sanitized results. See [helper setup](installation.md#offline-helpers-and-first-use).

The collector additionally needs an authorized compatible kubectl environment.
Installing a ZIP creates no Run:ai, Kubernetes, SSH or MCP connection. External
tools, network, credentials and permissions must be established separately for
the exact operation; do not enable them merely to test an import.

## Compatibility profile: chatgpt-conservative-v1

Reviewed **2026-10-18**. These are bounded packaging rules, not product support
certification. Source evidence is retained in [the ledger](sources.json).

| Surface | Verified documentation | Export decision / limit |
|---|---|---|
| ChatGPT Skills | Upload and workspace review are documented in the Help Center | ZIP acceptance for these packages, exact allowed types/limits and dependency installation remain unverified |
| Workspace Agents | Builder can attach existing/uploaded skills and Preview them | No import, automatic routing, helper execution or live connection claimed |
| Codex / ChatGPT desktop | [Build skills](https://learn.chatgpt.com/docs/build-skills) documents folder discovery and `agents/openai.yaml` | Keep canonical sources and discovery symlinks; generated interface fields are display name, short description and default prompt. Workspace web consumption of that metadata is unverified |
| OpenAI API-hosted Skills | [API guide](https://developers.openai.com/api/docs/guides/tools-skills) documents 50 MB ZIP, 500 files and 25 MB per uncompressed file | API limits are **not** Workspace Agents limits; no API upload integration is added |
| Agent Skills standard | [Specification](https://agentskills.io/specification) requires name/description and permits optional license/metadata | Normalize YAML serialization only; preserve supported optional fields, instructions, LICENSE and NOTICE files |

Local conservative limits: **25,000,000 bytes per ZIP**, **250 file entries**,
**10,000,000 bytes per file**, **50,000,000 bytes total uncompressed**. The profile
allows UTF-8 `.md`, `.txt`, `.py`, `.json`, `.yaml`, `.yml`, `.toml`, and extensionless
`LICENSE`/`NOTICE`. Other formats require a reviewed profile change, not silent
omission. This is intentionally narrower than the general standard.

Validation rejects unsafe paths, duplicate/case-colliding names, additional
entrypoints, symlinks, special files, encrypted entries, caches in exports,
undeclared Python imports, unpinned requirements and recognizable sensitive data.
It checks Markdown links, conventional resource paths and structured-file syntax.
Export skips source Python caches. It never runs bundled code or extracts an
untrusted ZIP. Static reference/import checks cannot prove every dynamically
constructed path or detect every secret: review source and test helpers too.

ZIP ordering, timestamps and regular-file permissions are fixed; stored entries
avoid compression-version differences. The manifest records source commit,
working-tree dirty state, release version, profile, descriptions, runtime limits,
sizes and hashes. A dirty build is not represented as a clean release artifact.

`openai/skills` now points to [openai/plugins](https://github.com/openai/plugins)
for current distribution examples. This adapter exports individual skills, not a
plugin or marketplace; native Codex installation remains available.

## Validate, update and troubleshoot

```sh
make check
make check-chatgpt
python scripts/validate_chatgpt_skill.py dist/chatgpt/runai-context-discovery/skill.zip --json
python scripts/validate_chatgpt_skill.py --release dist/chatgpt/release --json
```

Both CLIs return nonzero on failure. The validator also accepts an extracted skill
directory. Package tests extract every generated ZIP into temporary directories,
check resource preservation and run representative helpers on synthetic inputs.
These are packaging/helper tests, not agent behavior tests.

For an update, review the new release diff and checksum, keep the previous ZIP,
and test the replacement in a private agent draft. Use the editor/replacement
controls actually offered by your workspace; an in-place ZIP update contract is
not established by the reviewed docs. If necessary, upload separately and replace
the agent attachment after Preview. Confirm which revision is active before
retiring the old skill. Removing an attachment does not revoke tool credentials.

| Symptom | Next step |
|---|---|
| Upload control absent | Check workspace availability and upload permissions |
| ZIP rejected | Verify checksum, one skill root, profile results and the UI's exact error; do not bypass a security block |
| Needs Review / Blocked | Inspect source and follow workspace review; local validation does not override the scan |
| Missing helper or import error | Check packaged resources, execution tool and pinned dependency; use evidence-only analysis if unavailable |
| Skill not selected | Confirm attachment and inspect name/description; test explicit invocation |

Manual acceptance checklist, **not yet executed**:

1. Upload context discovery and record package SHA, workspace/date and scan result.
2. Attach it to a private draft and use Preview with the packaged synthetic snapshot.
3. Confirm independent versions and unknowns are retained, with no live calls.
4. Test another relevant skill implicitly, and an unrelated request as a negative control.
5. Record whether a helper actually ran, or whether the answer used instructions only.
6. Test replacement/removal in the draft before publishing changes to shared users.

## Maintainer distribution

The dedicated workflow validates PRs, main pushes and manual runs, then uploads a
temporary Actions artifact. A `vMAJOR.MINOR.PATCH` tag (optional prerelease suffix)
builds assets and creates/updates an **unpublished draft release** only after
validation. Only that tag-only job has `contents: write`. A maintainer must review
and explicitly publish it. Normal commits publish no release; no workflow uploads
anything into a ChatGPT account. Re-run `make check` after adding a canonical skill;
discovery and packaging pick it up automatically. Extend the local profile and
negative fixtures only when authoritative evidence justifies a new format.
