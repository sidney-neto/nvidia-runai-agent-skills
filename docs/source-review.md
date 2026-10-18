# Source review notes

All requested discovery entry points were inspected on 2026-10-18; the complete
requested/resolved URL inventory is in sources.json. Run:ai llms.txt and Markdown
representations were used after initial HTML inspection. vLLM llms.txt was not
available; versioned official HTML was used. Codex legacy URLs redirect to
ChatGPT Learn; direct Python fetches failed on the old aliases, while browser
retrieval resolved them and the final Markdown pages were fetched successfully.
KAI-Scheduler redirects from NVIDIA to kai-scheduler; it remains a development
reference unless tied to an installed version. NVIDIA's live skill catalog was
listed for discovery; no additional plugin/skill was installed into the project.

The ledger distinguishes entry-point inspection from procedural evidence. Source
URLs under latest/main are never alone evidence of an installed release. The
per-skill tables specify document versions, review dates and content hashes.
Hashes report byte-level changes, not semantic or compatibility validation.

Conflicts identified during review: upstream pending node-pool filter advice,
legacy swap guidance versus v3.0 removal, GPU Operator fraction minimum versus
support-matrix upper bound, and differing v3.0 compute-sharing annotation names.
Only the affected procedure is blocked pending resolution; see the relevant skill
references and upstream-provenance.md. No new support claim is generated from
successful source retrieval or synthetic helper tests.
