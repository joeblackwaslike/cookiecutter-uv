# spinup-py

[![Build status](https://img.shields.io/github/actions/workflow/status/joeblackwaslike/spinup-py/main.yml?branch=main)](https://github.com/joeblackwaslike/spinup-py/actions/workflows/main.yml?query=branch%3Amain)
[![Supported Python versions](https://img.shields.io/badge/python-3.10_%7C_3.11_%7C_3.12_%7C_3.13-blue?labelColor=grey&color=blue)](https://github.com/joeblackwaslike/spinup-py/blob/main/pyproject.toml)
[![Docs](https://img.shields.io/badge/docs-gh--pages-blue)](https://joeblackwaslike.github.io/spinup-py/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Discord](https://img.shields.io/discord/1486035859747897414?logo=discord&label=Discord&color=5865F2)](https://discord.gg/Fjc9zYHZyV)

Agentic Python scaffolding — spin up production-ready projects pre-wired for AI-assisted development. Ships a Claude Code plugin with slash commands, deterministic linters and type-checkers tuned for agentic workflows, and everything you need for testing, CI/CD, and deployment. Supports the following features:

- [uv](https://docs.astral.sh/uv/) for dependency management
- Supports [src layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/)
- CI/CD with [GitHub Actions](https://github.com/features/actions)
- Pre-commit hooks with [pre-commit](https://pre-commit.com/)
- Code quality with [ruff](https://github.com/charliermarsh/ruff), [mypy](https://mypy.readthedocs.io/en/stable/), [wemake-python-styleguide](https://wemake-python-styleguide.readthedocs.io/en/latest/pages/usage/setup.html), [deptry](https://github.com/joeblackwaslike/deptry/) and [prettier](https://prettier.io/)
- Publishing to [PyPI](https://pypi.org) by creating a new release on GitHub
- Testing and coverage with [pytest](https://docs.pytest.org/en/7.1.x/) and [codecov](https://about.codecov.io/)
- Documentation with [Docusaurus](https://docusaurus.io/)
- Compatibility testing for multiple versions of Python with [tox-uv](https://github.com/tox-dev/tox-uv)
- Containerization with [Docker](https://www.docker.com/)
- Development environment with [VSCode devcontainers](https://code.visualstudio.com/docs/devcontainers/containers)

---

<p align="center">
  <a href="https://joeblackwaslike.github.io/spinup-py/">Documentation</a> - <a href="https://github.com/joeblackwaslike/spinup-py-example">Example</a>
</p>

---

## Quickstart

[![Discord](https://img.shields.io/discord/1486035859747897414?logo=discord&label=Discord&color=5865F2)](https://discord.com/channels/1486035859747897414/1509515362012626944) [![Join Discord](https://img.shields.io/badge/Discord-Join%20Server-5865F2?logo=discord&logoColor=white)](https://discord.gg/Fjc9zYHZyV)

Navigate to the directory where you want your new project and run:

```shell
uvx spinup-py my-project
```

Or install globally first:

```shell
uv tool install spinup-py
spinup-py my-project
```

Follow the guided prompts to configure your project. Once complete, a new directory `my-project/` will be created with everything set up.

To retrofit an existing project with the latest tooling:

```shell
spinup-py --update /path/to/existing-project
```

> `spinup-py` is the Python sibling of [`spinup-ts`](https://www.npmjs.com/package/spinup-ts), the equivalent TypeScript project scaffolder.

### Install from source

For local or development use (e.g. running it as a Claude Code plugin), install the checkout directly with an editable install:

```shell
uv tool install --editable .
```

## Usage

```shell
# Scaffold a new project (bare form — positional name)
spinup-py my-project

# Same thing via the explicit subcommand
spinup-py new my-project

# Retrofit an existing project with the current tooling
spinup-py update /path/to/existing-project

# Or via the root flag (equivalent to `update`)
spinup-py --update /path/to/existing-project

# Print the installed version
spinup-py --version
```

### Flags

| Flag / command             | Description                                                                  |
| -------------------------- | ---------------------------------------------------------------------------- |
| `spinup-py <name>`         | Scaffold a new project with the given name (runs the guided prompts).        |
| `spinup-py new [<name>]`   | Explicit subcommand for scaffolding a new project.                           |
| `spinup-py update [<dir>]` | Retrofit an existing project at `<dir>` (defaults to the current directory). |
| `--update`, `-u <dir>`     | Root-level equivalent of `update` — retrofit an existing project at `<dir>`. |
| `--non-interactive`, `-y`  | Scaffold with sensible defaults and no prompts.                              |
| `--version`, `-v`          | Print the installed version and exit.                                        |

### Offline / custom template

By default the published CLI fetches its project template from GitHub (`gh:joeblackwaslike/spinup-py`). To use a local or custom template instead — handy when working offline or from a fork — set the `SPINUP_PY_TEMPLATE` environment variable to any Cookiecutter reference (a local path, a different GitHub repo, etc.):

```shell
SPINUP_PY_TEMPLATE=/path/to/template spinup-py my-project
```

## Acknowledgements & Lineage

- This project is partially based on [Florian Maas's](https://github.com/fpgmaas) great
  [cookiecutter-uv](https://github.com/fpgmaas/cookiecutter-uv)
  repository. Many additional improvements have been added from all the projects I've worked on over the last 12 years or so.
- Florian also credits [Audrey Feldroy's](https://github.com/audreyfeldroy) great [cookiecutter-pypackage](https://github.com/audreyfeldroy/cookiecutter-pypackage) repository.

## Feedback and contributing

My mission with this is to build the best project starter for python projects that has everything you can want, the ability to customize and/or opt out of most everything, and save you the most time!

I am only one person with very specific preferences. If you have any feedback you can email me at `me@joeblack.nyc`. If you find any bugs, mistakes, missed opportunities, or would like to contribute new functionality in any way, I would love to hear about it in an issue, feel free to email me the issue to get my attention.

This project is under continuous iterative improvements as I find bugs, and better and more effective ways to do things. But I can only do so much on my own, so please open an issue if you want to help/contribute and we can iterate and discuss how we can make this happen. If you find an outright bug or mistake, just open a PR and describe all the details there.
