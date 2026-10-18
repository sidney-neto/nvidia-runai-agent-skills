# Implementation plan — 2026-10-18

The user supplied the complete architectural brief and explicitly requested
continuation through implementation and publication. This plan records execution;
it does not introduce an additional approval gate.

1. Research primary sources, selectors, upstream skills and licensing. Record
   URLs, redirects, revisions, coverage and explicit exclusions. Reuse upstream
   diagnostic/audit intent through compatible optional delegation; extend under
   distinct local names.
2. Author all 22 goal-oriented SKILL.md files and packaged decision references.
   Each includes input, selection, read-only/offline path, documented commands,
   failures, output, change review, recovery limits, and English/Portuguese prompts.
3. Implement the smallest useful helpers in owning skills: local schema validator,
   quota calculator, profile/readiness evaluation, bounded Kubernetes collector,
   TLS/scheduling/vLLM offline checks, and sanitized incident report. Tests first
   for trust boundaries and arithmetic; no general compatibility language.
4. Add synthetic generic/eight-GPU environments and negative fixtures. Validate
   profiles, YAML, links, per-skill installation and all required regressions.
5. Add root English/Portuguese documentation, contribution/security/license,
   source freshness reporting, eval cases and CI with read-only permissions.
6. Run make check, review for invented interfaces and private data, independently
   review high-risk helpers and skill decisions, fix failures, then commit/push.
   Verify the published tree and CI; report unexecuted live/agent checks honestly.

Scope reaches skills, references, helper callers, schemas, fixtures, tests,
installation links, source ledger, examples, README files, CI and publishing.
The initial tree has no user code. Risks are inaccurate operational claims,
credential leakage, accidental mutation and broken individual installation;
validation prioritizes those over coverage counts.

Implementation ledger:
- Inspection complete: empty local/remote; no applicable ancestor AGENTS.md.
- Source discovery complete; focused release/source review in progress.
- Ruling: work in the empty checkout; no competing work or history to isolate.
- Ruling: keep the existing PUBLIC visibility as required by the brief.
- Ruling: no plugin packaging; core skills do not require a plugin adapter.
- Skill catalog complete: 22 canonical skills, packaged runbooks and English/PT prompts.
- Helpers complete: scoped collector and offline normalization/accounting/readiness/triage.
- Reviews: fixed credential encodings, partial inventory, workload/local scope gates,
  normalized schema round trip, cluster policy scope and shell quoting.
- Ruling: retain pinned jsonschema for runtime schema validation; a hand-written
  schema engine would be larger and weaker. Standalone installation declares it.
- Ruling: describe kubectl JSONPath as client-side output filtering; no unsupported
  server-side field authorization claim. Full-object retrieval needs authorization.
- Validation: 53 tests passing; separate agent/live suites explicitly not run.
