---
title: Quality Checks
---

# Quality Checks

## On Every Commit (pre-commit hook)

- Ruff format + lint
- Trailing whitespace / end-of-file fixes

## On Every Push / PR (CI)

- `uv run mypy .` — strict mode, zero errors allowed
- `uv run ruff check .` — lint with zero warnings
- `uv run ruff format --check .` — formatting enforcement
- `uv run pytest --cov` — pytest with coverage
- Dependency Review — blocks PRs with known-vulnerable dependencies

## Gates

| Gate | Threshold |
| ---- | --------- |
| Test coverage | Replace with your target (e.g., 80%) |
| mypy errors | 0 |
| Ruff warnings | 0 |
| Dependency vulnerabilities | 0 moderate+ |
