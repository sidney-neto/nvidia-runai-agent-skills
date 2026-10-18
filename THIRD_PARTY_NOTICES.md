# Attribution and licensing

Independent community project; not endorsed by NVIDIA. NVIDIA, Run:ai, NIM and
other product names belong to their respective owners.

Original repository code and documentation are MIT licensed. No upstream source
files or full documentation pages are vendored. Operational guidance is written
for this repository; links and short identifiers identify the relevant interfaces.

The upstream NVIDIA/Run:ai skills at
[revision 8190247dc97cd67538e8d4ab383d13b22da5037b](https://github.com/dsx-ai-factory/run-ai/tree/8190247dc97cd67538e8d4ab383d13b22da5037b/skills)
informed the workload diagnostic ordering and quota audit approach. Their
[skills/LICENSE](https://github.com/dsx-ai-factory/run-ai/blob/8190247dc97cd67538e8d4ab383d13b22da5037b/skills/LICENSE)
distinguishes executable code (Apache-2.0) from prose (CC-BY-4.0). Credit: NVIDIA
and Run:ai contributors. Local changes include version and capability gates,
offline fallbacks, hierarchy-safe arithmetic, source-conflict handling and distinct
skill names. This attribution also covers that conceptual adaptation; no upstream
license is replaced by this repository's license.

If contributors copy or adapt upstream expression or executable files, preserve
the applicable license and attribution in the installed skill itself, identify
modifications, and record provenance. Do not assume the repository root license
applies to every upstream subtree. Dependency licenses remain their owners'.

Additional conceptual review of quota, failure, health and utilization workflows
used [revision 70997dcca3b4486878778cef71b50830e708b31a](https://github.com/dsx-ai-factory/run-ai/tree/70997dcca3b4486878778cef71b50830e708b31a/skills).
Credit remains NVIDIA and Run:ai contributors; the code/prose license distinction
is unchanged. The affected installed skills include their own NOTICE.md.
