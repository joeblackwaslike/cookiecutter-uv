---
title: Contributing (Dev)
---

# Contributing — Developer Notes

This covers technical details for contributors. See the [user-facing contributing guide](../contributing) for the PR workflow.

## Project Setup

```bash
git clone https://github.com/{{cookiecutter.github_handle}}/{{cookiecutter.project_name}}.git
cd {{cookiecutter.project_name}}
make install
uv run pytest
```

## Code Conventions

- mypy strict mode — no `Any`, no `# type: ignore` without comment
- Ruff for formatting — `uv run ruff format .` before committing
- Conventional commits — required for release-please automation

## Release Process

Releases are fully automated:

1. Commit with conventional commit messages
2. release-please opens a versioned PR automatically
3. Merge the PR → release created → PyPI published → docs deployed
