---
title: Constitution
---

# Constitution

The non-negotiable architectural principles for {{cookiecutter.project_name}}.

## Core Principles

1. **Type-annotated** — every public API is fully typed; strict mypy compliance
2. **Async-first** — async by default; only use sync where the library forces it
3. **Minimal dependencies** — replace or remove if your project has deps
4. **Replace with your principle** — describe it

## Constraints

- Python `>= {{cookiecutter.python_version}}` — minimum runtime requirement
- Pydantic v2 for data validation where applicable
- Add other constraints relevant to your project

## What This Is Not

Describe what {{cookiecutter.project_name}} explicitly does NOT do. Scope boundaries matter.
