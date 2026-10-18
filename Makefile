PYTHON ?= python3
.PHONY: check freshness
check:
	$(PYTHON) -m unittest discover -s tests -v
freshness:
	$(PYTHON) scripts/check_sources.py docs/sources.json
