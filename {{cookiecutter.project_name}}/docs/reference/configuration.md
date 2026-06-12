---
title: Configuration Reference
---

# Configuration Reference

## Full Config Schema

```python
from pydantic import BaseModel


class Config(BaseModel):
    # Replace with your actual Config model
    required: str
    optional: bool = False
```

## Options

### `required`

**Type:** `str` · **Required:** yes

Description of this option.

### `optional`

**Type:** `bool` · **Default:** `False`

Description of this option.

## Configuration Sources

List where configuration can come from (constructor args, env vars, config file, etc.).

## Environment Variables

| Variable | Description |
| -------- | ----------- |
| `{{cookiecutter.project_slug | upper}}_OPTION` | Replace with real env var if applicable |

Replace or remove this section if your library doesn't use environment variables.
