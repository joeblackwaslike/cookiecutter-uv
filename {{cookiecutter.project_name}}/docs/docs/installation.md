---
title: Installation
---

# Installation

## Requirements

- Python `>= {{cookiecutter.python_version}}`
- A package manager: [uv](https://docs.astral.sh/uv/) (recommended) or pip

## Install

**uv (recommended)**

```bash
uv add {{cookiecutter.project_name}}
```

**pip**

```bash
pip install {{cookiecutter.project_name}}
```

## Verify

```python
import {{cookiecutter.project_slug}}

print({{cookiecutter.project_slug}}.__version__)
```

## Next Steps

→ [Getting Started](./getting-started)
