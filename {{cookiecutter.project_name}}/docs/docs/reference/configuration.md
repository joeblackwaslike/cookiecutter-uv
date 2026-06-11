---
title: Configuration Reference
---

# Configuration Reference

## Full Config Schema

```python
from dataclasses import dataclass

@dataclass
class Config:
    """Replace with your actual Config class."""
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
