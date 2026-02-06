.PHONY: dev test test-e2e build lint clean install

# Development
dev:
	uvicorn api.app:app --reload --port 8080

# Install dependencies
install:
	pip install -e ".[dev]"
	cd frontend && npm install

# Testing
test:
	pytest api/tests/ -v

test-e2e:
	cd e2e && npx playwright test

# Build frontend and copy to static
build:
	cd frontend && npm run build && cp -r dist ../static

# Linting
lint:
	ruff check api/
	cd frontend && npm run lint

# Type checking
typecheck:
	mypy api/
	cd frontend && npx tsc --noEmit

# Clean build artifacts
clean:
	rm -rf __pycache__ .pytest_cache .mypy_cache .ruff_cache
	rm -rf api/__pycache__ api/**/__pycache__
	rm -rf frontend/dist static
	rm -rf .coverage htmlcov coverage.xml

# Full check before commit
check: lint typecheck test
	@echo "All checks passed!"
