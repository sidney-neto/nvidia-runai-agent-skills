# Operational skill catalog

This independent library provides 22 portable operational skills. Install a single canonical directory under `skills/`; its `SKILL.md` and packaged references work without repository imports. `.agents/skills` contains discovery links only. Each skill starts with a bounded read-only or offline assessment and prepares a concrete change review when requested.

| Skill | Outcome |
| --- | --- |
| [runai-context-discovery](../skills/runai-context-discovery/SKILL.md) | Produce a small, evidence-backed context for a selected environment. |
| [runai-cluster-health](../skills/runai-cluster-health/SKILL.md) | Locate the failing layer across control-plane synchronization, Kubernetes nodes, GPU capacity and workload admission. |
| [runai-mcp-integration](../skills/runai-mcp-integration/SKILL.md) | Assess an optional MCP connection and produce a scoped configuration proposal. |
| [runai-quota-capacity-planning](../skills/runai-quota-capacity-planning/SKILL.md) | Build a per-pool capacity and demand ledger, then propose an auditable quota change. |
| [runai-projects-departments](../skills/runai-projects-departments/SKILL.md) | Produce a scoped organizational mapping and a change proposal with workload impact. |
| [runai-rbac-access](../skills/runai-rbac-access/SKILL.md) | Identify the authorization plane, principal, action and scope responsible for a denial. |
| [runai-workload-policies](../skills/runai-workload-policies/SKILL.md) | Explain the effective policy and produce a targeted policy/spec diff. |
| [runai-scheduling-diagnostics](../skills/runai-scheduling-diagnostics/SKILL.md) | Find the first evidenced placement constraint and distinguish it from startup failure. |
| [runai-workload-lifecycle](../skills/runai-workload-lifecycle/SKILL.md) | Build the correct lifecycle diagnosis and a concrete change proposal for one workload. |
| [runai-tls-oidc](../skills/runai-tls-oidc/SKILL.md) | Locate the trust or identity mismatch using sanitized evidence and propose a precise correction. |
| [runai-gpu-sharing](../skills/runai-gpu-sharing/SKILL.md) | Separate memory allocation, compute behavior and device accounting, then assess the exact supported sharing path. |
| [runai-upgrade-readiness](../skills/runai-upgrade-readiness/SKILL.md) | Produce a go/no-go evidence checklist for one explicit transition. |
| [kubernetes-gpu-operations](../skills/kubernetes-gpu-operations/SKILL.md) | Create a node-specific maintenance decision with workload and control-plane impact. |
| [nvidia-gpu-operator](../skills/nvidia-gpu-operator/SKILL.md) | Locate the failing GPU enablement component and propose a version-matched correction. |
| [runai-storage](../skills/runai-storage/SKILL.md) | Trace storage from Run:ai datasource selection to Kubernetes PVC/PV/CSI and application access. |
| [runai-networking](../skills/runai-networking/SKILL.md) | Map one failing connection and locate the routing, policy or TLS layer. |
| [runai-observability](../skills/runai-observability/SKILL.md) | Validate telemetry meaning and freshness before drawing an operational conclusion. |
| [runai-vllm-serving](../skills/runai-vllm-serving/SKILL.md) | Create a memory and placement budget plus a small serving-config proposal. |
| [runai-nim-serving](../skills/runai-nim-serving/SKILL.md) | Validate a pinned NIM image/profile and the Run:ai deployment path, then prepare a bounded serving proposal. |
| [runai-distributed-workloads](../skills/runai-distributed-workloads/SKILL.md) | Separate group placement from process rendezvous and collective communication. |
| [runai-backup-recovery](../skills/runai-backup-recovery/SKILL.md) | Build a recovery inventory and evidence-based restore plan. |
| [runai-support-report](../skills/runai-support-report/SKILL.md) | Create a shareable incident report with controlled evidence scope. |

Each canonical directory also exports as an individual [ChatGPT Workspace Agents package](chatgpt-workspace-agents.md), with generated OpenAI UI metadata and preserved resources. The exporter discovers skills dynamically; this catalog does not act as its allowlist.

## Selection and boundaries

Start with context discovery when target/version evidence is incomplete. Use cluster health for system impact, scheduling diagnostics for placement, and workload lifecycle for a particular attempt. Quota planning analyzes commitments and eligible demand; observability evaluates measured usage. Organization, RBAC and policy reviews are separate because namespace presence, API permission and admission enforcement are different claims.

Serving skills separate vLLM memory budgeting from NIM profile compatibility. Distributed workloads adds whole-group placement and rendezvous analysis. Infrastructure skills distinguish nodes, GPU enablement, durable storage, networking and verifier-specific TLS/OIDC trust. Upgrade readiness requires explicit source-to-target evidence; recovery and support reporting each have independent data scopes.

Every skill includes English and pt-BR invocation examples, input requirements, version selection, a numbered decision workflow, bounded read examples, error/partial-result handling, evidence output and change/recovery limits. Primary instructions stay in `SKILL.md`; detailed interpretation and source/version profiles are packaged in `references/runbook.md`.

## Evidence and optional upstream reuse

The [source ledger](sources.json) records resolved URLs, documentation versions, review dates and hashes. Run:ai domain procedures here were reviewed against explicit v3.0 pages. GPU Operator 25.3.4, NIM LLM 1.10.0 and vLLM 0.10.2 references have independent scopes and are not an asserted compatible stack. Unknown releases keep useful offline analysis; concrete procedures wait for matching evidence. Structural, deterministic, agent-behavior and live tests must be reported separately.

The upstream [failed-workload skill](https://github.com/dsx-ai-factory/run-ai/blob/8190247dc97cd67538e8d4ab383d13b22da5037b/skills/runai-diagnose-failed-workload/SKILL.md) and [quota-audit skill](https://github.com/dsx-ai-factory/run-ai/blob/8190247dc97cd67538e8d4ab383d13b22da5037b/skills/runai-audit-assigned-quota/SKILL.md) were inspected at revision `8190247dc97cd67538e8d4ab383d13b22da5037b`. They are optional compatible specialists, not required dependencies. Their code/prose licenses are Apache-2.0/CC-BY-4.0; this library links and attributes them without copying their implementation or shadowing their skill names. Local workflows retain explicit namespace resolution, offline paths and careful handling of the upstream quota reference's conflicting pending-node-pool guidance.

MCP is optional. Prefer a verified official Run:ai server when its runtime schemas, permissions and exact targets match the task. A listed tool is not proof of usable access, permission or vendor support. Kubernetes reads and sanitized local snapshots remain available fallbacks. No skill contacts a cluster or credential store for repository validation.
