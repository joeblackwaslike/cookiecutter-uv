---
sidebar_position: 2
---

# Installation

## Requirements

- Python {{cookiecutter.python_version}}+
- [uv](https://docs.astral.sh/uv/) (recommended)

## Install

```bash
uv add {{cookiecutter.project_name}}
```

Or with pip:

```bash
pip install {{cookiecutter.project_name}}
```

## Verify

```python
import {{cookiecutter.project_slug}}
print({{cookiecutter.project_slug}}.__version__)
```
