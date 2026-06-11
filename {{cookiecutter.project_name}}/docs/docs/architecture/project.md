---
title: Project Structure
---

# Project Structure

```
{{cookiecutter.project_name}}/
├── src/
│   └── {{cookiecutter.project_slug}}/
│       ├── __init__.py       # public API exports
│       └── ...               # replace with your structure
├── tests/                    # test suite
├── docs/                     # documentation source (Docusaurus)
├── pyproject.toml            # project metadata and dependencies
└── justfile                  # development task runner
```

## Module Boundaries

Describe the internal module structure and how modules relate.

## Public API

Everything exported from `src/{{cookiecutter.project_slug}}/__init__.py` is part of the public API and subject to semver.
Everything else is internal and may change without notice.
