---
title: Testing Plan
---

# Testing Plan

## Test Strategy

Replace with your project's testing strategy. For a library:

- **Unit tests** — every exported function, edge cases, error paths
- **Integration tests** — key workflows end-to-end
- No mocking of internal implementation details

## Coverage Goals

| Metric | Target |
| ------ | ------ |
| Line coverage | > 80% (replace with your target) |
| Branch coverage | > 75% |
| Function coverage | > 90% |

## Test File Conventions

```
tests/
├── conftest.py           # shared fixtures
├── test_core.py          # mirrors src/{{cookiecutter.project_slug}}/core.py
└── test_models.py        # mirrors src/{{cookiecutter.project_slug}}/models.py
```

## What We Do Not Test

- Third-party library internals
- Build tooling (ruff, mypy)
- Generated files
