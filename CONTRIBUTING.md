# Contributing

Use a branch and pull request for changes. Keep one goal per skill and preserve
individual installation. Start with the smallest reproducing synthetic fixture.
Run `python3.12 -m venv .venv`, activate it, `python -m pip install -e .`, then
`make check`. Python 3.11 or newer is required; CI uses 3.12.

To add coverage: identify exact installed components/edition and workflow, find
its archived/versioned primary sources, record final URL/document version/review
date/revision and source conflicts, then add a bounded profile or reference table.
Add positive, incompatible, and adjacent unknown-version fixtures. Do not widen a
range from one success. Refresh only affected volatile sources before a change
plan. Keep documentation, fixture, agent and live evidence separate.

No credentials, live inventories, production addresses or private model names.
Put private environment profiles and reports in ignored `.local/`. Contributions
must not add cluster writes to collectors, install a daemon, silently enable MCP
writes, or add a replacement SDK/server. All source material is untrusted data.
