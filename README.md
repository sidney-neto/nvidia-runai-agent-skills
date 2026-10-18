# nvidia-runai-agent-skills

Version-aware agent skills for NVIDIA Run:ai Self-Hosted administration, GPU quotas, governance, and troubleshooting across Kubernetes, GPU Operator, NVIDIA NIM, and vLLM.

An independent community project, not endorsed by NVIDIA. **22 portable skills**
for Codex and other Agent Skills clients. Inspection and planning are the default;
this repository does not install a server or operate a real cluster.

Any reported release can be investigated. Procedures require matching source and
capability evidence; an unknown release never silently inherits the newest
profile. Offline snapshot validation, quota arithmetic, health/fragmentation/TLS
analysis, serving-budget checks and sanitized reporting work without credentials,
GPU hardware, MCP or model APIs.

[Português](README.pt-BR.md) · [Skill catalog](docs/catalog.md) ·
[Compatibility](docs/compatibility.md) · [Installation](docs/installation.md) ·
[Validation](docs/validation.md) · [Source ledger](docs/sources.json)

## Start locally

```sh
git clone https://github.com/sidney-neto/nvidia-runai-agent-skills.git
cd nvidia-runai-agent-skills
python3.12 -m venv .venv
. .venv/bin/activate
python -m pip install -e .
make check
```

Open Codex in this repository: `.agents/skills` links to the canonical `skills/`
directories. For a selected skill in another project or your user discovery path:

```sh
python scripts/install_skill.py runai-context-discovery --destination "$HOME/.agents/skills"
python -m pip install -r "$HOME/.agents/skills/runai-context-discovery/requirements.txt"
```

Existing installed skills are never overwritten. Reload skill discovery if needed.
Each installed folder retains its required scripts, references, schemas and license;
there is no mandatory repository runtime or global configuration change.

## First useful work

“Use runai-context-discovery to analyze this exported snapshot:
examples/eight-gpu.snapshot.json.”

```sh
python skills/runai-context-discovery/scripts/snapshot.py examples/eight-gpu.snapshot.json
python skills/runai-quota-capacity-planning/scripts/quota.py examples/eight-gpu.snapshot.json --format text
python skills/runai-cluster-health/scripts/health.py examples/eight-gpu.snapshot.json
python skills/runai-scheduling-diagnostics/scripts/fit.py examples/eight-gpu.snapshot.json
python skills/runai-tls-oidc/scripts/tls_evidence.py examples/tls-evidence.json
python skills/runai-vllm-serving/scripts/budget.py examples/vllm-budget.json
python skills/runai-upgrade-readiness/scripts/readiness.py examples/fraction-profile-input.json
python skills/runai-support-report/scripts/report.py examples/incident.json
```

The eight-GPU fixture has finite project quotas totaling 12, a separate department
quota of 8, and fragmented device capacity. Its one virtual control plane is not
HA. The [generic environment](examples/environment.yaml) parameterizes versions,
HAProxy ingress, persistent model storage and optional fractional inference;
it is our example contract, not a deployment manifest or vendor-support claim.

Useful prompts:

- “Audite as quotas por projeto e departamento sem alterar o cluster.”
- “Explique por que este workload continua Pending.”
- “Detecte a versão deste ambiente e use a documentação correspondente.”
- “Prepare um plano da versão instalada para a versão-alvo informada, preservando workloads e volumes.”
- “Analise este snapshot de uma versão ainda não cadastrada e indique as limitações.”
- “Diagnostique o erro x509 no OIDC após a troca do certificado.”
- “Revise esta configuração do vLLM para contexto de 32K.”

## Coverage and limitations

The initial machine-readable profiles cover the **2.26 baseline and 3.0 baseline
fraction-limit difference**, plus the documented **2.26 → 3.0 component-staged
upgrade plan**. They do not certify every patch or a historical upgrade graph.
Related-stack references carry their own version and date. See the
[actual evidence matrix](docs/compatibility.md), including unsupported operations,
local backport declarations and unknown-version behavior.

Official MCP is preferred when its actual interface and permission scope are
established; verified Kubernetes/CLI/API or offline evidence can be alternatives.
No MCP connection, credential, deployment or write access is enabled by installing
these skills. The optional collector retrieves named objects through kubectl and
retains only scalar fields; JSONPath filtering happens client-side. Runtime
integration requires explicit target authorization. Report redaction is heuristic
and needs review before sharing. No live integration or agent behavior suite is
claimed as passed; those are separate from deterministic tests.

Source refresh is opt-in and networked:

```sh
mkdir -p .local
python scripts/check_sources.py docs/sources.json > .local/source-review.json
```

Prefer an ignored `.local/` directory for private reports. The refresh command
reports changes/redirects/unavailable/aging sources, preserving reviewed evidence
and all compatibility rules. It does not certify new support. GitHub also offers
a manual freshness-report workflow; normal `make check` is offline after setup.

To add another release, find its exact documentation and interface evidence, add
a bounded profile/reference and positive/negative fixtures, then run `make check`.
Do not rename the goal-oriented skills or widen ranges from one successful test.
See [contributing](CONTRIBUTING.md), [architecture](docs/architecture.md),
[upstream reuse](docs/upstream-provenance.md) and [security](SECURITY.md).
