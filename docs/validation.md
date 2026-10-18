# Validation results — 2026-10-18

## Executed locally

- Python **3.12**, clean repository virtual environment.
- `python3.12 -m venv --clear .venv`
- `.venv/bin/python -m pip install -e .` — installed pinned lightweight toolchain.
- `make check PYTHON=.venv/bin/python` — **52 tests passed**.
- `.venv/bin/python -m pip check` — no broken requirements.
- Quota CLI with `examples/eight-gpu.snapshot.json --format text` — physical 8,
  finite project quota 12, department quota 8, oversubscription true, research
  over quota. No parent double-counting.
- Report and vLLM CLIs generated the committed synthetic report examples.
- Readiness CLI with `examples/upgrade-plan.json --upgrade` — expected exit 2,
  missing prerequisite evidence retained in the example report. This is a useful
  blocked change-plan result, not a test failure or a claim of readiness.
- `scripts/check_sources.py docs/sources.json` — an opt-in public-network run
  covered the then-current 90-source ledger: 65 unchanged, 5 changed, 1 unavailable,
  19 no-baseline. Changed hashes were GitHub HTML discovery entries; vLLM llms.txt
  was unavailable. No reviewed rules/evidence were overwritten. Two subsequent
  focused primary sources (permissions/Prometheus syntax) were fetched and hashed;
  they were not part of that earlier 90-source refresh run.

An initial attempt used macOS's Python 3.9 and old pip, which could not install
the declared toolchain. The local venv was recreated with 3.12. System Python was
not changed. Supported development Python is 3.11+ (stdlib TOML parser).

## Structural and packaging checks

Proper PyYAML frontmatter/naming checks cover all 22 skills. JSON/YAML/TOML examples
parse; references stay within their installed skill. Every skill is copied into a
temporary directory outside the repository, all packaged helpers execute `--help`,
and standalone snapshot validation executes there. Existing installations are
refused. Checked-in discovery symlinks target canonical folders. Shell examples
with wildcard fields are quoted; local zsh checks use a no-op kubectl function.
CI actions are commit-pinned, have contents-read permission, no persisted checkout
credential, and bounded job duration. Normal checks require no operational/model
credentials or hardware after dependency installation.

## Deterministic helper coverage

| Requirement | Evidence |
|---|---|
| Two documented families, incompatible combination, unknown newer release | test_compatibility baseline 2.26/3.0, K8s mismatch, 9.0 and unknown patches |
| Missing/ambiguous/prerelease/vendor versions; numeric ordering; conflicts | test_helpers and test_compatibility |
| Independent CP/cluster/CLI/MCP and mixed GPU-node versions | component fixtures and mixed-node regression |
| Capability absent/denied/disabled/deprecated/removed/experimental/unverified/unsupported | distinct-state tests and local contradiction tests |
| Unknown-version offline analysis, MCP-absent verified fallback | offline guard plus named kubectl adapter with fake results |
| Eight GPUs, hierarchy-safe quota overcommit | arithmetic tests and committed fixture |
| Unlimited/missing/zero quota, partial pools, page contradictions, duplicates | quota and pagination regressions |
| Pending despite aggregate capacity | complete per-device fragmentation and incomplete negative-knowledge tests |
| Host TLS success/application trust failure | TLS evidence tests, including strict boolean boundary |
| Supported staged upgrade, unknown transition, missing prerequisites | documented component stages; no fabricated historical hops |
| Release-specific breaking change stays bounded | 2.26 env versus 3.0 annotation selection; native CLI scope excluded |
| vLLM 32K/concurrency budget | 16 requested versus 2 full-length resident sequences |
| Single control plane | explicit no-HA finding |
| Changed/unavailable sources preserve reviewed evidence | pure freshness comparison tests |
| Redaction and read-only collection | nested/inline/quoted/escaped/basic/bearer/key tests; command/error/output-bound tests |

Offline guards fail on covered workflows attempting socket creation, live-tool
subprocesses, common credential-path access or home-directory discovery. Tests
also verify import paths do not instantiate a live adapter. This is targeted
coverage, not an OS sandbox or proof against every possible future network API.
Collector integration is tested with fake responses and harmless local Python
processes only. kubectl internally retrieves full named objects; its JSONPath
projection is client-side output minimization, not server-side field restriction.

Independent helper and catalog reviews found and fixed redaction edge cases,
unknown-quota false negatives, partial-inventory claims, workload/scope selection,
normalizer round trips, missing cluster policy scope and zsh quoting. The pinned
jsonschema dependency was deliberately retained to avoid a custom schema engine;
its installation is explicit and packaged.

## Not executed

- **Agent behavior suite:** 16 cases/rubrics in evals; not run against a model/fake
  tool harness. Code review is not a behavioral eval. Tests retaining injected
  text as data do not prove an agent resists instruction injection.
- **Live integration:** no Run:ai/Kubernetes/MCP, quotas, workloads, NIM/vLLM requests,
  upgrades, backups/restores, GPU enforcement or performance tests.
- **Vendor certification:** none. Documentation plus fixtures establish bounded
  procedure evidence only. Exact distribution/patch/edition/artifact availability
  and runtime permissions remain external requirements.

GitHub CI status is reported separately after publication; local results alone
do not establish that a remote workflow has run.
