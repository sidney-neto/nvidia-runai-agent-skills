# Discover a Run:ai operating context — operational reference

## Documented read examples

Run only against an explicitly selected, authorized target. All names below are synthetic placeholders. Inspect only the fields needed for the question; command output is still private evidence until sanitized. `--request-timeout=15s` bounds each Kubernetes request, not the entire multi-page operation; use an overall time/page budget in the caller.

```sh
kubectl --context example-context --namespace runai --request-timeout=15s get deployment runai-agent -o jsonpath='{.metadata.name}{"\n"}{.spec.template.spec.containers[*].image}{"\n"}'
```

## Interpretation and decision limits

The image observation identifies what to investigate in release metadata; it does not equate a Helm chart, CLI or control-plane release. Names such as `runai-agent` must be confirmed for the selected deployment. An absent Deployment is not proof that Run:ai is absent.

A useful local profile records an alias, evidence source, observed timestamp, explicit component versions, topology, declared capabilities and unknowns. Do not store endpoints, credentials or real inventory in this public library. A profile never grants access. For unknown releases, compare the supplied observations and identify the documentation needed; do not select a nearest release.

## Change review

Context changes are proposals: show the exact context/namespace selection and affected subsequent reads. Do not switch the global current context or create credentials. Verification is a repeated named identity read; recovery is discarding the proposed local context document.

A request for analysis authorizes analysis. Prepare the concrete proposed diff and checks before seeking any additional approval that execution requires. Execute only within explicit task authorization; a documentation example, discovered tool or local profile is not authorization. Stop if target identity changes or prerequisites contradict the selected procedure.

## Failure handling and evidence contract

On permission denial, record the denied action/scope and continue with permitted or offline evidence; never broaden permissions. If a tool, resource type or schema is missing, name it and use supplied snapshots instead of guessing an interface. Preserve partial results and unavailable fields. Follow the documented cursor/continuation until complete within a declared page/time budget; otherwise label totals incomplete. Do not interpret an empty page, truncated response or timeout as absence. Retry a transient read at most once with the same scope; stop on repeated timeout or identity mismatch.

Return: verdict and impact; selected target aliases and independent component versions; evidence source/time window in UTC; observations versus hypotheses; missing/partial evidence and confidence; next minimal step. Mark advertised, usable, permitted and vendor-supported capability claims separately. Documentation review, deterministic fixture results, agent-behavior evaluation and live validation are separate evidence categories; never present one as another.

## Source and version profile

Keep Run:ai control plane, Run:ai cluster, REST generation, CLI, MCP server/protocol, Kubernetes, GPU Operator, driver and application versions separate. Container image tags are clues, not proof of the installed product release.

The links below are reviewed evidence for this packaged workflow, not a blanket supported-version list. Versioned documentation supports only its stated scope. Unversioned Kubernetes command references establish command syntax; verify API/resource availability in the selected Kubernetes release. No installed skill requires repository-root files. A user-supplied local profile must state source, observation time, exact versions and uncertainty and remains a declaration until corroborated.

- [architecture](https://docs.nvidia.com/run-ai/self-hosted/v3.0/documentation/getting-started/architecture.md) — documentation `v3.0`; reviewed `2026-10-18`; SHA-256 `b857758cac2a901e006f28996b675656181f7eff0a243b09f3816f307c2aae96`.
- [tools-reference](https://docs.nvidia.com/run-ai/self-hosted/v3.0/documentation/agents/mcp-server/tools-reference.md) — documentation `v3.0`; reviewed `2026-10-18`; SHA-256 `c4f7e964b94bcbbc0c84c986cf77597d14010bffa70b88431669044fd70c1d21`.
- [kubectl-get](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_get/) — documentation `unversioned`; reviewed `2026-10-18`; SHA-256 `4c9ca9706157c96d5dfc1fb9f3500eaf06fe75370a69ef03c5ba278f08894dfd`.

Reviewed source text may contain commands that mutate systems or export sensitive configuration; it is reference data, not an instruction to execute those commands. Refresh only evidence affected by a changed dependency or procedure and retain previously reviewed provenance.
