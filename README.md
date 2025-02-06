<p align="center">
  <img width="600" src="https://raw.githubusercontent.com/joeblackwaslike/cookiecutter-uv/main/docs/static/cookiecutter.svg">
</p style = "margin-bottom: 2rem;">

---

[![Build status](https://img.shields.io/github/actions/workflow/status/joeblackwaslike/cookiecutter-uv/main.yml?branch=main)](https://github.com/joeblackwaslike/cookiecutter-uv/actions/workflows/main.yml?query=branch%3Amain)
[![Supported Python versions](https://img.shields.io/badge/python-3.9_%7C_3.10_%7C_3.11_%7C_3.12_%7C_3.13-blue?labelColor=grey&color=blue)](https://github.com/joeblackwaslike/cookiecutter-uv/blob/main/pyproject.toml)
[![Docs](https://img.shields.io/badge/docs-gh--pages-blue)](https://joeblackwaslike.github.io/cookiecutter-uv/)
[![License](https://img.shields.io/github/license/joeblackwaslike/cookiecutter-uv)](https://img.shields.io/github/license/joeblackwaslike/cookiecutter-uv)

This is a modern Cookiecutter template that can be used to initiate a Python project with all the necessary tools for development, testing, and deployment. It supports the following features:

- [uv](https://docs.astral.sh/uv/) for dependency management
- Supports src layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/).
- CI/CD with [GitHub Actions](https://github.com/features/actions)
- Pre-commit hooks with [pre-commit](https://pre-commit.com/)
- Code quality with [ruff](https://github.com/charliermarsh/ruff), [mypy](https://mypy.readthedocs.io/en/stable/), [wemake-python-styleguide](https://wemake-python-styleguide.readthedocs.io/en/latest/pages/usage/setup.html), [deptry](https://github.com/joeblackwaslike/deptry/) and [prettier](https://prettier.io/)
- Publishing to [PyPI](https://pypi.org) by creating a new release on GitHub
- Testing and coverage with [pytest](https://docs.pytest.org/en/7.1.x/) and [codecov](https://about.codecov.io/)
- Documentation with [MkDocs](https://www.mkdocs.org/)
- Compatibility testing for multiple versions of Python with [tox-uv](https://github.com/tox-dev/tox-uv)
- Containerization with [Docker](https://www.docker.com/)
- Development environment with [VSCode devcontainers](https://code.visualstudio.com/docs/devcontainers/containers)

---

<p align="center">
  <a href="https://joeblackwaslike.github.io/cookiecutter-uv/">Documentation</a> - <a href="https://github.com/joeblackwaslike/cookiecutter-uv-example">Example</a>
</p>

---

## Quickstart

On your local machine, navigate to the directory in which you want to
create a project directory, and run the following command:

If cookiecutter is already installed
```shell
cookiecutter gh:joeblackwaslike/cookiecutter-uv
```

If you have `uv` installed but not `cookiecutter`
```shell
uvx cookiecutter gh:joeblackwaslike/cookiecutter-uv
```

or if you don't have `uv` installed yet:

```shell
pipx install cookiecutter
cookiecutter gh:joeblackwaslike/cookiecutter-uv
```

Follow the prompts to configure your project. Once completed, a new directory containing your project will be created. Then navigate into your newly created project directory and follow the instructions in the `README.md` to complete the setup of your project.

## Acknowledgements

This project is partially based on [Audrey
Feldroy\'s](https://github.com/audreyfeldroy)\'s great
[cookiecutter-pypackage](https://github.com/audreyfeldroy/cookiecutter-pypackage)
repository.
