---
title: Constitution
---

# Constitution

The non-negotiable architectural principles for {{cookiecutter.project_name}}.

## Core Principles

1. **Type-safe** — every public API is fully annotated; mypy strict mode with no `Any`
2. **Minimal dependencies** — replace or remove if your project has zero deps
3. **Immutability** — replace with your principle
4. **Replace with your principle** — describe it

## Constraints

- Python `>= {{cookiecutter.python_version}}` — minimum runtime requirement
- `src` layout — all library code lives under `src/{{cookiecutter.project_slug}}/`
- Add other constraints relevant to your project

## What This Is Not

Describe what {{cookiecutter.project_name}} explicitly does NOT do. Scope boundaries matter.
