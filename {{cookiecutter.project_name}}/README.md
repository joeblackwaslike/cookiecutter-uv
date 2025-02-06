# {{cookiecutter.project_name}}

[![Release](https://img.shields.io/github/v/release/{{cookiecutter.github_handle}}/{{cookiecutter.project_name}})](https://img.shields.io/github/v/release/{{cookiecutter.github_handle}}/{{cookiecutter.project_name}})
[![Build status](https://img.shields.io/github/actions/workflow/status/{{cookiecutter.github_handle}}/{{cookiecutter.project_name}}/main.yml?branch=main)](https://github.com/{{cookiecutter.github_handle}}/{{cookiecutter.project_name}}/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/{{cookiecutter.github_handle}}/{{cookiecutter.project_name}}/branch/main/graph/badge.svg)](https://codecov.io/gh/{{cookiecutter.github_handle}}/{{cookiecutter.project_name}})
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)
[![Commit activity](https://img.shields.io/github/commit-activity/m/{{cookiecutter.github_handle}}/{{cookiecutter.project_name}})](https://img.shields.io/github/commit-activity/m/{{cookiecutter.github_handle}}/{{cookiecutter.project_name}})
[![License](https://img.shields.io/github/license/{{cookiecutter.github_handle}}/{{cookiecutter.project_name}})](https://img.shields.io/github/license/{{cookiecutter.github_handle}}/{{cookiecutter.project_name}})

{{cookiecutter.description}}

- **Github repository**: <https://github.com/{{cookiecutter.github_handle}}/{{cookiecutter.project_name}}/>
- **Documentation** <https://{{cookiecutter.github_handle}}.github.io/{{cookiecutter.project_name}}/>

## Getting started with your project

### 1. Create a New Repository

First, create a repository on GitHub with the same name as this project, and then run the following commands:

```shell
git init -b main
git add .
git commit -m "init commit"
git remote add origin git@github.com:{{cookiecutter.github_handle}}/{{cookiecutter.project_name}}.git
git push -u origin main
```

Or you can use the `gh` CLI to create the remote repository from the current directory:

```shell
git init -b main
git add .
git commit -m "init commit"
gh repo create {{cookiecutter.project_name}} --description "{{cookiecutter.description}}" --public --source=. --remote=origin --push
```

### 2. Set Up Your Development Environment

Then, install the environment and the pre-commit hooks with

```shell
make install
```

This will also generate your `uv.lock` file

### 3. Run the pre-commit hooks

Initially, the CI/CD pipeline might be failing due to formatting issues. To resolve those run:

```shell
uv run pre-commit run -a
```

### 4. Commit the changes

Lastly, commit the changes made by the two steps above to your repository.

```shell
git add .
git commit -m 'Fix formatting issues'
git push origin main
```

You are now ready to start development on your project!
The CI/CD pipeline will be triggered when you open a pull request, merge to main, or when you create a new release.

To finalize the set-up for publishing to PyPI, see [here](https://joeblackwaslike.github.io/cookiecutter-uv/features/publishing/#set-up-for-pypi).
For activating the automatic documentation with MkDocs, see [here](https://joeblackwaslike.github.io/cookiecutter-uv/features/mkdocs/#enabling-the-documentation-on-github).
To enable the code coverage reports, see [here](https://joeblackwaslike.github.io/cookiecutter-uv/features/codecov/).

## Releasing a new version

{% if cookiecutter.publish_to_pypi == "y" -%}

- Create an API Token on [PyPI](https://pypi.org/).
- Add the API Token to your projects secrets with the name `PYPI_TOKEN` by visiting [this page](https://github.com/{{cookiecutter.github_handle}}/{{cookiecutter.project_name}}/settings/secrets/actions/new).
- Create a [new release](https://github.com/{{cookiecutter.github_handle}}/{{cookiecutter.project_name}}/releases/new) on Github.
- Create a new tag in the form `*.*.*`.

For more details, see [here](https://joeblackwaslike.github.io/cookiecutter-uv/features/cicd/#how-to-trigger-a-release).
{%- endif %}

---

Repository initiated with [joeblackwaslike/cookiecutter-uv](https://github.com/joeblackwaslike/cookiecutter-uv).
