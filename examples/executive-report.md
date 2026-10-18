# Synthetic capacity review

Scope: synthetic-lab / pool-a / synthetic-80GiB. Evidence timestamp:
2026-10-18T12:00:00Z. Source: eight-gpu.snapshot.json, complete synthetic page set.
No live discovery, model requests or changes were performed.

| Measure | Observed value |
|---|---:|
| Physical GPU devices | 8 |
| Allocatable GPU-equivalents | 8 |
| Finite project quotas | 12 |
| Department quota, reported separately | 8 |
| Project allocations | 7 |
| Per-device free GPU-equivalents | 0.125 on each of 8 devices |
| GPU compute activity / measured memory usage | Unknown / unknown |

Configured project entitlement exceeds allocatable capacity by 4 equivalents.
Research is allocated 7 against quota 6; this can represent permitted borrowing,
not necessarily a policy violation. Parent quota is not added to child demand.

The pending one-device request cannot fit any reported device despite an aggregate
free equivalent. Other placement, permission and topology constraints remain
unverified. Proposed action: review borrowing policy and owner-approved capacity
or placement options. No quota cut, preemption or termination is authorized.

Run:ai control-plane 3.0 and cluster 2.26 are independent synthetic observations;
CLI/MCP versions are unknown. The single virtual control plane cannot be treated
as highly available. Serving latency and volume were not supplied. The evidence
supports arithmetic and triage only, not vendor compatibility or performance.
