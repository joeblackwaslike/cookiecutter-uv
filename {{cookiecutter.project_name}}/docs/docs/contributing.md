---
title: Contributing
---

# Contributing

Thank you for your interest in contributing to {{cookiecutter.project_name}}!

## Development Setup

```bash
git clone https://github.com/{{cookiecutter.github_handle}}/{{cookiecutter.project_name}}.git
cd {{cookiecutter.project_name}}
uv sync
uv run pre-commit install
```

## Running Tests

```bash
uv run pytest              # run tests
uv run pytest --cov        # run with coverage
```

## Code Quality

```bash
just check                 # lint + typecheck + deptry
uv run ruff check .        # lint only
uv run mypy                # typecheck only
```

## Submitting a Pull Request

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Make your changes and add tests
4. Ensure all checks pass: `just check && just test`
5. Commit using [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat: add new feature`
   - `fix: correct a bug`
   - `docs: update documentation`
6. Open a pull request

## Release Process

Releases are automated via [release-please](https://github.com/googleapis/release-please).
Merging a release PR automatically publishes to PyPI and deploys the docs.
