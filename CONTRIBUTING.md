# Contributing and validation

Use a branch and pull request. Preserve the 22 goal-oriented skill entry points,
individual installation, and unrelated changes. Start with a reproducing
synthetic fixture. Keep temporary/private artifacts in `.local/`.

## Development setup

Python 3.11+ is required; CI uses 3.12. From the repository root:

```sh
python3.12 -m venv .venv
. .venv/bin/activate
python -m pip install -e .
make check
python -m pip check
```

Instruction-only skill installation does not need this development environment.
Normal checks work offline after dependencies are installed. They need no
Run:ai/Kubernetes/model credentials, GPU, or MCP server.

## Design and maintenance

Use modular Agent Skills with optional official tools. Documentation alone cannot
validate snapshots or repeat quota arithmetic; a custom agent framework would
add unnecessary services and credential handling. Keep deterministic helpers
inside the skill owning their contract. No repository imports in installed skills,
replacement SDK/MCP server, daemon, or client-specific copies of canonical skills.

Resolve the exact target, relevant independent component versions, bounded
profile, settings, submission path, permissions, and source conflicts before an
interface-dependent operation. Prefer compatible official MCP; a verified
CLI/API/Kubernetes or offline fallback must retain the same scope. Present concrete
changes, impact, prerequisites, verification and recovery limits before execution.
Use dry-run only where documented. Skill text does not enforce runtime security.

The collector uses named Kubernetes objects and client-side scalar projection.
kubectl retrieves full objects internally; this is output minimization, not
server-side field authorization. It does not request Secrets, logs, environments,
exec, probes, or mutations. See [security](SECURITY.md).

To add release coverage, find exact version/edition/workflow sources. Record final
URL, document version, review date/revision and conflicts in the packaged reference
and [source ledger](docs/sources.json). Add bounded profiles and positive,
incompatible and adjacent unknown-version fixtures. Never widen a range from one
success or infer support from upstream main. See [compatibility](docs/compatibility.md).

Source review is opt-in and networked:

```sh
mkdir -p .local
python scripts/check_sources.py docs/sources.json > .local/source-review.json
```

Review changed, redirected, aging and unavailable sources before affected change
plans. The helper preserves reviewed evidence and never promotes new compatibility.
Hashes detect byte changes, not semantic changes. Keep source refresh outside
normal CI; the manual workflow produces a temporary report artifact.

## What the checks establish

| Layer | Coverage | Limits |
|---|---|---|
| Structure / packaging | YAML frontmatter, 22 names, local links, schemas, discovery symlinks, individual copies, packaged helper help and standalone snapshot validation | Does not establish client discovery or agent decisions |
| Deterministic helpers | Quota hierarchy/unknowns, partial pages, fragmentation, health, TLS trust locations, serving budgets, redaction, independent versions, bounded profiles and staged upgrades | Synthetic evidence; no vendor certification |
| Offline / collector boundaries | Covered offline paths reject network, live subprocesses and credential access; collector uses fake responses and harmless local processes | Targeted tests, not an OS sandbox or live Kubernetes integration |
| Agent behavior | [Prompt/rubric suite](evals/README.md) | Not executed; code review and retained injection text do not prove agent resistance |
| Live integration | Run:ai, Kubernetes, MCP, NIM/vLLM, GPU enforcement, upgrade and restore | Not executed; requires separate environment authorization |

Run `make check` for the current count and result; GitHub Actions records each
commit's run. [Client installation evidence](docs/installation.md#validation-status)
is separate from the offline helper suite. Do not report unexecuted agent/live
checks as passed. Keep pinned CI actions, read-only permissions, timeouts and
synthetic examples when changing validation.
