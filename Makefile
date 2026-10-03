.PHONY: setup lint test vectors bench audit ci

setup:
	cd python && python -m pip install --upgrade pip && python -m pip install -e ".[dev]"

lint:
	python spec/generate_vectors.py --check
	cd java && mvn -B -q -DskipTests compile
	cd python && python -m ruff check . ../spec && python -m ruff format --check . ../spec
	cd js && npm run -s lint

# Shared vectors plus 500 random oracle comparisons per algorithm, in every language.
test:
	cd java && mvn -B -q verify
	cd python && python -m pytest -q
	cd js && npm test

# Regenerate spec/vectors/*.json from the brute-force oracles.
vectors:
	python spec/generate_vectors.py

bench:
	@echo "M2: growth-rate harness with log-log fitting lands with the correctness write-ups"

# Known vulnerabilities in the installed Python dependencies.
audit:
	cd python && python -m pip_audit --skip-editable --cache-dir ../.tmp/pip-audit

ci: setup lint test
