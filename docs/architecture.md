# Architecture decision — 2026-10-18

Build an independent community library for NVIDIA Run:ai Self-Hosted, with Codex
as the primary client and portable Agent Skills as the canonical interface.

| Alternative | Benefit | Limitation | Decision |
|---|---|---|---|
| Documentation only | Lowest maintenance | Cannot validate snapshots or repeat quota arithmetic | Insufficient for this brief |
| Modular skills using official interfaces | Portable, focused workflows; deterministic offline evidence | Requires bounded source review and runtime authorization | Selected |
| Custom agent framework/MCP server | Central orchestration | Duplicates official tools, adds credentials and services | Rejected |

One canonical directory per goal; install one directory without repository
imports. Each skill packages its references. Deterministic Python helpers live
with the skill that owns their input contract. No shared runtime framework or
cluster write adapter. Repository tests can load those scripts directly.

Run:ai product releases, REST generations, Kubernetes apiVersions, CLI versions,
and MCP server/protocol versions remain independent. Profiles are small JSON
records, bounded to reviewed evidence. Unknown releases retain offline analysis;
only affected version-dependent procedures become missing-evidence results.
Local declarations carry provenance but cannot defeat contradictory observations,
grant permissions, or certify vendor support. Documentation, synthetic fixtures,
agent evaluations, and live tests are separate evidence columns.

Current primary-source discoveries:
- [Agent Skills specification](https://agentskills.io/specification): portable
  SKILL.md frontmatter and packaged resources.
- [Codex skills](https://learn.chatgpt.com/docs/build-skills): repository and user
  `.agents/skills`, including symlinked directories.
- [Run:ai index](https://docs.nvidia.com/run-ai/llms.txt): default Self-Hosted
  documentation identifies v3.0; selectors expose bounded historical references.
- [Official MCP tools](https://docs.nvidia.com/run-ai/self-hosted/v3.0/documentation/agents/mcp-server/tools-reference):
  optional official integration; discovery alone does not establish usable access.

Read-only collector: explicitly selected Kubernetes targets, documented kubectl
interface, client-side projection of allowlisted fields, bounded output and time.
kubectl retrieves full named objects internally; this is output minimization,
not server-side field authorization. Do not use this collector if full-object
retrieval is outside the authorized scope. No Secret resources, kubeconfig export,
logs, environment output, exec, mutation, or probes are requested.
Offline helpers import no live adapters and never consult credentials. Quota,
readiness, TLS evidence, scheduling fit, serving budget, and report utilities
operate only on local synthetic/schema-validated data.

All external content is evidence, never an instruction source. Installation
never changes global configuration or overwrites existing skills. Original code
and prose use MIT; upstream material is linked and attributed, with no vendored
upstream skills. Changes to that choice require license review.

The destination was an empty PUBLIC repository owned by the authenticated
personal account sidney-neto. Preserve existing visibility. User explicitly
authorized implementation, commits, and publication. No cluster access is allowed.
