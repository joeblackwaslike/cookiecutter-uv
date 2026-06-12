---
title: Hooks & Plugins Reference
---

# Hooks & Plugins Reference

Remove this page if {{cookiecutter.project_name}} does not have a hooks/plugin system.

## Available Hooks

| Hook | When it fires | Signature |
| ---- | ------------- | --------- |
| `on_init` | Replace with real hook | `(config: Config) -> None` |

## Example

```python
from {{cookiecutter.project_slug}} import create_instance


def my_init_hook(config):
    print(f"Initialized: {config}")


instance = create_instance(
    hooks={
        "on_init": my_init_hook,
    },
)
```
