---
title: Installation
---

# Installation

## Requirements

- Python `>= {{cookiecutter.python_version}}`
- A package manager: uv (recommended), pip, or poetry

## Install

**uv (recommended)**

```bash
uv add {{cookiecutter.project_name}}
```

**pip**

```bash
pip install {{cookiecutter.project_name}}
```

**poetry**

```bash
poetry add {{cookiecutter.project_name}}
```

## Verify

```python
import {{cookiecutter.project_slug}}
print({{cookiecutter.project_slug}}.__version__)
```

## Optional Dependencies

List any optional dependency groups here. If none, remove this section.

```bash
pip install "{{cookiecutter.project_name}}[dev]"
```

## Next Steps

→ [Getting Started](./getting-started)
