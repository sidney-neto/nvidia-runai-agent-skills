PYTHON ?= python3
CHATGPT_OUTPUT ?= dist/chatgpt
.PHONY: check freshness check-chatgpt package-chatgpt validate-chatgpt
check:
	$(PYTHON) -m unittest discover -s tests -v
freshness:
	$(PYTHON) scripts/check_sources.py docs/sources.json
check-chatgpt:
	$(PYTHON) -m unittest discover -s tests -p test_chatgpt_packaging.py -v
	$(PYTHON) scripts/package_chatgpt_skills.py --all --validate-only
package-chatgpt:
	$(PYTHON) scripts/package_chatgpt_skills.py --all --output "$(CHATGPT_OUTPUT)"
validate-chatgpt:
	$(PYTHON) scripts/validate_chatgpt_skill.py --release "$(CHATGPT_OUTPUT)/release" --json
