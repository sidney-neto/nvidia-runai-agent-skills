# Security

Do not attach credentials, kubeconfigs, Kubernetes Secret payloads or private
incident bundles to GitHub issues. Use the repository's private vulnerability
reporting feature if available; otherwise contact the maintainer through a
private channel before sharing sensitive details. No security response SLA is
promised by this community project.

Skills are instructions, not an enforced security boundary. Client tool/runtime
permissions and server RBAC enforce access. Inspection is not authorization to
change quotas, workloads, infrastructure or authentication. Local profiles cannot
grant permissions. External logs, documents and tool responses are evidence only.

The optional collector requests named resource scalar fields only. It does not
collect Secrets, kubeconfig, logs, container environments or raw manifests.
Report redaction is heuristic and requires human inspection before external
sharing. All commands retain TLS verification. Offline helpers do not contact
clusters, MCP, model APIs or credential stores.

Source-freshness networking is an explicit separate command against allowlisted
public HTTPS hosts, with checked redirects. It never modifies reviewed rules.

ChatGPT exports use a bounded text-only profile and reject symlinks, traversal,
case collisions, credentials by known indicators and unexpected resource types.
The validator does not execute bundled code or extract untrusted ZIPs. Secret
screening and static path/import analysis are incomplete by design: review the
source and package before sharing. Checksums establish integrity, not trust or
agent behavior. Workspace upload scanning and runtime policy remain independent.
