.PHONY: install lint format fix type test coverage ci clean help

# Default target
help:
	@echo "Available targets:"
	@echo "  make install   - Install package in editable mode with dev dependencies"
	@echo "  make lint      - Run ruff check on dicominfo/"
	@echo "  make format    - Run ruff format --check (fails if format differs)"
	@echo "  make fix       - Apply ruff fixes and formatting"
	@echo "  make type      - Run mypy on dicominfo/"
	@echo "  make test      - Run pytest in verbose mode"
	@echo "  make coverage  - Run pytest with coverage (80% threshold)"
	@echo "  make ci        - Run all checks (format, lint, type, coverage)"
	@echo "  make clean     - Remove build artifacts and cache files"

# Install package with dev dependencies
install:
	pip install -e .[dev]

# Run ruff linting
lint:
	ruff check dicominfo/

# Check code formatting
format:
	ruff format --check dicominfo/

# Apply fixes and formatting
fix:
	ruff check --fix dicominfo/
	ruff format dicominfo/

# Run mypy type checking
type:
	mypy dicominfo/

# Run tests
test:
	pytest

# Run tests with coverage
coverage:
	pytest --cov=dicominfo --cov-report=term --cov-report=xml --cov-fail-under=80

# Run all CI checks
ci: format lint type coverage

# Clean build artifacts
clean:
	rm -rf build dist *.egg-info
	rm -rf .pytest_cache .mypy_cache .ruff_cache
	rm -rf htmlcov coverage.xml .coverage
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
