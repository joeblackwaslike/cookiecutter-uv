---
title: Quality Checks
---

# Quality Checks

## On Every Commit (pre-commit hook)

- Ruff format + lint
- Prettier for markdown, JSON, YAML

## On Every Push / PR (CI)

- `uv lock --locked` — lock file consistency with pyproject.toml
- `uv run ruff check .` — linting with zero warnings
- `uv run ruff format --check .` — formatting check
- `uv run mypy` — strict type checking, zero errors allowed
- `uv run deptry src` — no unused or missing dependencies
- `uv run pytest --cov` — test suite with coverage
- `uv run mkdocs build -s` — docs build (if applicable)

## Gates

| Gate | Threshold |
|------|-----------|
| Test coverage | Replace with your target (e.g., 80%) |
| mypy errors | 0 |
| Ruff warnings | 0 |
| Dependency issues | 0 |
