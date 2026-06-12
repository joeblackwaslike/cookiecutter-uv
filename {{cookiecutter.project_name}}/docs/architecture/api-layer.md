---
title: API Layer
---

# API Layer

## Overview

Describe the API layer of {{cookiecutter.project_name}} — how it exposes functionality to consumers.

## Public API Surface

Everything exported from `src/{{cookiecutter.project_slug}}/__init__.py` is part of the public API and subject to semver.

```python
# Example: primary exports
from {{cookiecutter.project_slug}}.core import your_main_export
from {{cookiecutter.project_slug}}.types import Config, Result
```

## API Design Principles

- **Minimal surface** — only expose what consumers need; keep internals private
- **Type-safe** — every parameter and return type is fully annotated; no `Any`
- **Stable** — breaking changes require a major version bump

## Request / Response Flow

Describe how a call flows from consumer → public API → internal implementation → return value.

```
Consumer → your_main_export(input)
         → validate(input)
         → process(validated)
         → Result
```

## Error Handling

Describe how errors surface to callers (raised exceptions, returned error objects, Result types, etc.).

## Versioning

Describe your semver strategy and how you signal deprecations before breaking changes.
