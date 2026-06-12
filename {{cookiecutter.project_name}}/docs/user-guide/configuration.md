---
title: Configuration
---

# Configuration

## Configuration Object

```python
from {{cookiecutter.project_slug}} import Config

config = Config(
    # Replace with your actual configuration options
    option1="default-value",
    option2=True,
)
```

## Options Reference

| Option | Type | Default | Description |
| ------ | ---- | ------- | ----------- |
| `option1` | `str` | `"default"` | Replace with real option description |
| `option2` | `bool` | `True` | Replace with real option description |

## Environment Variables

| Variable | Description |
| -------- | ----------- |
| `{{cookiecutter.project_slug | upper}}_OPTION` | Replace with real env var if applicable |

Replace or remove this section if your library doesn't use environment variables.
