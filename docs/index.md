<style>
  .md-typeset h1,
  .md-content__button {
    display: none;
  }
</style>

---

Agentic Python scaffolding — spin up production-ready projects pre-wired for AI-assisted development. Ships a Claude Code plugin with slash commands, deterministic linters and type-checkers tuned for agentic workflows, and everything you need for testing, CI/CD, and deployment. Supports the following features:

- [uv](https://docs.astral.sh/uv/) for dependency management
- Supports src layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/).
- CI/CD with [GitHub Actions](https://github.com/features/actions)
- Pre-commit hooks with [pre-commit](https://pre-commit.com/)
- Code quality with [ruff](https://github.com/charliermarsh/ruff), [mypy](https://mypy.readthedocs.io/en/stable/), [wemake-python-styleguide](https://wemake-python-styleguide.readthedocs.io/en/latest/pages/usage/setup.html), [deptry](https://github.com/joeblackwaslike/deptry/) and [prettier](https://prettier.io/)
- Publishing to [PyPI](https://pypi.org) by creating a new release on GitHub
- Testing and coverage with [pytest](https://docs.pytest.org/en/7.1.x/) and [codecov](https://about.codecov.io/)
- Documentation with [Docusaurus](https://docusaurus.io/)
- Compatibility testing for multiple versions of Python with [tox-uv](https://github.com/tox-dev/tox-uv)
- Containerization with [Docker](https://www.docker.com/)
- Development environment with [VSCode devcontainers](https://code.visualstudio.com/docs/devcontainers/containers)

## Quickstart

Navigate to the directory where you want your new project and run:

```bash
uvx spinup-py my-project
```

Or install globally first:

```bash
uv tool install spinup-py
spinup-py my-project
```

Follow the guided prompts to configure your project. Once complete, a new directory `my-project/` will be created with everything set up.

### Acknowledgements

This project is partially based on [Audrey
Feldroy's](https://github.com/audreyfeldroy) great
[cookiecutter-pypackage](https://github.com/audreyfeldroy/cookiecutter-pypackage).
