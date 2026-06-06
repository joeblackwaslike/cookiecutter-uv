---
sidebar_position: 6
---

# Contributing

See [CONTRIBUTING.md](https://github.com/{{cookiecutter.github_handle}}/{{cookiecutter.project_name}}/blob/main/CONTRIBUTING.md) for the full contribution guide.

## Development setup

```bash
git clone https://github.com/{{cookiecutter.github_handle}}/{{cookiecutter.project_name}}
cd {{cookiecutter.project_name}}
uv sync
uv run pre-commit install
```

## Running docs locally

```bash
make docs
```
