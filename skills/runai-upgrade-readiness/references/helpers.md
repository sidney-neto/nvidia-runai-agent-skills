# Packaged deterministic helper

```sh
python scripts/readiness.py environment.json --workflow fraction-limit
```

Run from this installed skill directory, or use its absolute script path.
No offline helper calls a network, cluster, MCP server or credential store.

This helper reads `references/profiles.json` and local JSON only. It does not
refresh sources or execute commands. Default mode selects a fraction procedure;
`--upgrade` evaluates the bounded component-staged transition. Exit 2 means
invalid input or an affected operation with missing/incompatible evidence, not
that all offline analysis failed.

Selection input: deployment, components (map from component name to raw_version
and origin), workload_type, settings (required setting names mapped to observed
booleans), and capabilities (name → state/advertised/usable/permitted). For the
shipped profiles, workload_type is "supported-workload YAML" and settings are
"fractional GPU workload" and "observed effective memory limit". Both must be
verified. The caller still verifies exact semantic and permission evidence.
Native CLI/API paths must not receive the YAML migration rule.

Upgrade input: current/target raw baseline releases, deployment, edition,
kubernetes version, fractions boolean, prerequisites map, and independent
components.runai-control-plane / components.runai-cluster records with raw_version
and origin. Current refers to the observed cluster; contradictory values conflict.
An already-target control plane is verified rather than upgraded again. See the packaged
transition record for the required checks. A true prerequisite is an operator's
recorded evidence, not a new verification performed by this helper. It returns
missing checks, sourced stage order and recovery limitations. All GPU nodes and
exact distribution support require separate review. No historical release hops
are generated from version arithmetic.

To investigate a backport, pass `--profiles /path/to/local-profiles.json` with the
same simple records. Local records use provenance_type="local", exact_raw,
provenance, captured_at and scope (matching environment.scope), plus normal
workflow/component/settings/workload_types/capability fields. versions can be
empty for an exact custom identity. The result is local-procedure with vendor
support unset; it never inherits a release baseline. Multiple matches conflict.
An optional environment.local_profile declaration can reveal contradictions in
the affected workflow/component; unrelated findings do not block other work.
