# Operational model

1. Resolve the named cluster/context/project/workload; ambiguous identity blocks
   only the affected operation. Never switch global kubectl context.
2. Collect only relevant component versions and their origins. Separate control
   plane, cluster services, scheduler, CLI and MCP; nodes can differ. Preserve
   REST generation, Kubernetes apiVersion and MCP protocol as independent fields.
3. Match a bounded profile, then verify settings, workload/submission path,
   interface schema, permissions and source agreement. Tool advertisement is not
   evidence of usable semantics or entitlement.
4. Prefer the compatible official MCP server. If absent, use an independently
   verified CLI/API/Kubernetes path within the same read/write scope, or analyze
   supplied evidence offline. Do not guess flags or automatically request admin.
5. Report target, timestamps, evidence, findings, uncertainty and next action.
   Inspection never authorizes mutation. Reuse existing exact-scope authorization;
   present proposed diff, impact, prerequisites, verification and recovery limits
   before execution. Use native dry-run only where documented for that interface.

MCP is optional. Current documented local/remote transports and authentication
are reviewed in the MCP skill; the repository does not deploy a server, edit
client configuration, enable writes or provide credentials. Client policies and
server RBAC are the security boundary, not skill text or risk labels.

Collect the minimum allowlisted fields. Logs require explicit target/time/size
bounds and redaction before artifacts are written. The shipped collector avoids
logs entirely. Container access, probes, inference calls and benchmarks consume
resources or extend scope; do not treat them as ordinary offline inspection.
Keep TLS verification enabled and distinguish administrator-host trust from
application-container trust. Keep private snapshots under `.local/`.
