---
title: Contributing (Dev)
---

# Contributing — Developer Notes

This covers technical details for contributors. See the [user-facing contributing guide](../contributing) for the PR workflow.

## Project Setup

```bash
git clone https://github.com/{{cookiecutter.github_handle}}/{{cookiecutter.project_name}}.git
cd {{cookiecutter.project_name}}
uv sync
uv run pre-commit install
just check
just test
```

## Code Conventions

- Type annotations on all public APIs — mypy strict mode, no `Any`
- Ruff for linting and formatting — `uv run ruff check . && uv run ruff format .`
- Conventional commits — required for release-please automation

## Release Process

Releases are fully automated:
1. Commit with conventional commit messages
2. release-please opens a versioned PR automatically
3. Merge the PR → release created → published to PyPI → docs deployed
