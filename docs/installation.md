# Installation and first use

The canonical folders follow the [Agent Skills specification](https://agentskills.io/specification).
Codex currently scans repository and user `.agents/skills` directories and follows
symlinked skill folders, as documented in [Build skills](https://learn.chatgpt.com/docs/build-skills).
Other compatible clients can install the same complete canonical directory.

## Repository-local

Clone this repository and open Codex in its root. Checked-in `.agents/skills/*`
symlinks resolve to `skills/*`; there is one canonical copy. Restart/reload skill
discovery if your client does not pick up the new tree. No global config edit.

For helper development (Python 3.11+, tested with 3.12):

```sh
python3.12 -m venv .venv
. .venv/bin/activate
python -m pip install -e .
make check
```

## Install one skill

From the cloned repository, use an explicitly chosen destination:

```sh
python scripts/install_skill.py runai-context-discovery --destination "$HOME/.agents/skills"
python -m pip install -r "$HOME/.agents/skills/runai-context-discovery/requirements.txt"
```

The installer copies the full folder, including references, scripts, schemas and
license. It refuses existing destinations; it never edits client configuration.
Use another project's `.agents/skills` as destination for project-local discovery.
All helpers except snapshot validation use the Python standard library. The
snapshot validator needs its pinned `jsonschema` requirement. Runtime dependencies
must be installed before an intentionally offline session. Installation tests copy
every skill outside the repository and execute helper help plus standalone
snapshot validation. They do not test every client implementation.

## First use without credentials

Ask Codex: “Use runai-context-discovery to analyze this exported snapshot:
examples/eight-gpu.snapshot.json.” Or run:

```sh
python skills/runai-context-discovery/scripts/snapshot.py examples/eight-gpu.snapshot.json
python skills/runai-quota-capacity-planning/scripts/quota.py examples/eight-gpu.snapshot.json --format text
python skills/runai-scheduling-diagnostics/scripts/fit.py examples/eight-gpu.snapshot.json
python skills/runai-vllm-serving/scripts/budget.py examples/vllm-budget.json
```

These commands are fully local. MCP, kubeconfig, GPU hardware and model credentials
are unnecessary. The optional live collector requires an already compatible
kubectl and explicit authorized context/namespace/named targets. Do not run it to
validate this repository. See its packaged reference for fields and permissions.
