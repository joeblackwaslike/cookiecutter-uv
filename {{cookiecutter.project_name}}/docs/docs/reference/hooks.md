---
title: Hooks Reference
---

# Hooks Reference

Remove this page if {{cookiecutter.project_name}} does not have a hooks/plugin system.

## Available Hooks

| Hook | When it fires | Signature |
|------|--------------|-----------|
| `on_init` | Replace with real hook | `(config: Config) -> None` |

## Example

```python
from {{cookiecutter.project_slug}} import create_instance

instance = create_instance(
    hooks={
        "on_init": lambda config: print(f"Initialized: {config}"),
    },
)
```
