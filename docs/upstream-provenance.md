# Upstream provenance

Reviewed 2026-10-18. Original guidance is independently written and MIT licensed;
no upstream skill files or documentation mirrors are vendored. See
[attribution](../THIRD_PARTY_NOTICES.md) and the [source ledger](sources.json).

## Run:ai workflows

Inspected `dsx-ai-factory/run-ai` revision
`8190247dc97cd67538e8d4ab383d13b22da5037b`, including both skills, their references
and [license](https://github.com/dsx-ai-factory/run-ai/blob/8190247dc97cd67538e8d4ab383d13b22da5037b/skills/LICENSE).
Executable code is Apache-2.0; SKILL.md/references/prose are CC-BY-4.0. Preserve the
applicable license and attribution inside any skill that incorporates upstream
expression. Current local NOTICE files acknowledge conceptual adaptation.

| Upstream | Decision and local extension |
|---|---|
| [runai-diagnose-failed-workload](https://github.com/dsx-ai-factory/run-ai/blob/8190247dc97cd67538e8d4ab383d13b22da5037b/skills/runai-diagnose-failed-workload/SKILL.md) | Adapt evidence ordering, exact workload resolution, preemption routing and uncertainty. Extend under distinct names with version gates and offline evidence. |
| [runai-audit-assigned-quota](https://github.com/dsx-ai-factory/run-ai/blob/8190247dc97cd67538e8d4ab383d13b22da5037b/skills/runai-audit-assigned-quota/SKILL.md) | Extend same-pool accounting and legitimate borrowing with hierarchy-safe arithmetic, partial data and fragmentation. |

These are optional compatible specialists, not installed dependencies. Their MCP
requirements do not establish compatibility on historical servers. The quota
reference's final `nodePoolName` advice conflicts with its main skill: pending
pods are unassigned. Establish pool eligibility from workload evidence instead of
pending counts. Its memory-swap discussion is legacy-only; v3.0 removes swap.

## Source interpretation

Run:ai's unversioned selector currently identifies v3.0; the v2.26 selector
redirects to the legacy Self-Hosted root and v2.25 to `/self-hosted/2.25`. The legacy
lifecycle page still calls 2.26 latest. A moving alias never establishes the
installed release. Use exact identities from [compatibility](compatibility.md)
and packaged source tables.

The ledger retains requested/final URLs, versions, review dates, revisions and
hashes. Domain records include their consuming skills. llms.txt/Markdown were
preferred where available; unavailable vLLM llms.txt fell back to versioned HTML.
KAI-Scheduler's redirect remains a development reference unless tied to a release.
Keep entry-point discovery separate from procedural evidence.

Known conflicts remain bounded: upstream pending-pool filtering, legacy swap,
fraction GPU Operator minimum versus support-matrix maximum, and differing v3.0
compute-sharing annotations. The relevant packaged runbook records each decision;
only the affected procedure is blocked, not independent offline analysis.
