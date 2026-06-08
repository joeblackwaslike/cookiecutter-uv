#!/usr/bin/env python
import os
import re
import shutil

import tomlkit

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)
PYPROJECT = os.path.join(PROJECT_DIRECTORY, "pyproject.toml")


def remove_file(filepath: str) -> None:
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


def remove_dir(filepath: str) -> None:
    shutil.rmtree(os.path.join(PROJECT_DIRECTORY, filepath))


def move_file(filepath: str, target: str) -> None:
    os.rename(os.path.join(PROJECT_DIRECTORY, filepath), os.path.join(PROJECT_DIRECTORY, target))


def _dep_name(spec: str) -> str:
    """Extract the lowercased package name from a PEP 508 dependency string."""
    return re.split(r"[<>=~!\[ ;]", spec.strip(), maxsplit=1)[0].lower()


def remove_dependencies(path: str, names: list[str]) -> None:
    """Remove dependencies (matched by package name) from dependency-groups.dev.

    Matching is by package name only, so it is robust to version-pin changes
    (e.g. ``deptry~=0.23.1`` -> ``deptry~=0.24.0``) and to extras such as
    ``coverage[toml]``.
    """
    with open(path) as f:
        doc = tomlkit.parse(f.read())
    try:
        dev_deps = doc["dependency-groups"]["dev"]
    except KeyError:
        return
    targets = {name.lower() for name in names}
    for dep in list(dev_deps):
        if _dep_name(str(dep)) in targets:
            dev_deps.remove(dep)
    with open(path, "w") as f:
        f.write(tomlkit.dumps(doc))


def remove_toml_section(path: str, section: str) -> None:
    """Remove a TOML section by key path (e.g. 'tool.coverage.run')."""
    with open(path) as f:
        doc = tomlkit.parse(f.read())
    keys = section.split(".")
    node = doc
    for key in keys[:-1]:
        if key not in node:
            return
        node = node[key]
    if keys[-1] in node:
        del node[keys[-1]]
    with open(path, "w") as f:
        f.write(tomlkit.dumps(doc))


if __name__ == "__main__":
    if "{{cookiecutter.deptry}}" != "y":
        remove_dependencies(PYPROJECT, ["deptry", "ipython"])

    if "{{cookiecutter.codecov}}" != "y":
        remove_dependencies(PYPROJECT, ["coverage", "pytest-cov"])
        remove_toml_section(PYPROJECT, "tool.coverage.run")
        remove_toml_section(PYPROJECT, "tool.coverage.report")

    if "{{cookiecutter.include_github_actions}}" != "y":
        remove_dir(".github")
    else:
        if "{{cookiecutter.include_docs}}" != "y" and "{{cookiecutter.publish_to_pypi}}" == "n":
            remove_file(".github/workflows/on-release-main.yml")

    if "{{cookiecutter.include_docs}}" != "y":
        remove_dir("docs")

    if "{{cookiecutter.dockerfile}}" != "y":
        remove_file("Dockerfile")
        remove_file("docker-compose.yaml")
    if "{{cookiecutter.codecov}}" != "y":
        remove_file("codecov.yaml")
        if "{{cookiecutter.include_github_actions}}" == "y":
            remove_file(".github/workflows/validate-codecov-config.yml")

    if "{{cookiecutter.devcontainer}}" != "y":
        remove_dir(".devcontainer")

    if "{{cookiecutter.open_source_license}}" == "MIT license":
        move_file("LICENSE_MIT", "LICENSE")
        remove_file("LICENSE_BSD")
        remove_file("LICENSE_ISC")
        remove_file("LICENSE_APACHE")
        remove_file("LICENSE_GPL")

    if "{{cookiecutter.open_source_license}}" == "BSD license":
        move_file("LICENSE_BSD", "LICENSE")
        remove_file("LICENSE_MIT")
        remove_file("LICENSE_ISC")
        remove_file("LICENSE_APACHE")
        remove_file("LICENSE_GPL")

    if "{{cookiecutter.open_source_license}}" == "ISC license":
        move_file("LICENSE_ISC", "LICENSE")
        remove_file("LICENSE_MIT")
        remove_file("LICENSE_BSD")
        remove_file("LICENSE_APACHE")
        remove_file("LICENSE_GPL")

    if "{{cookiecutter.open_source_license}}" == "Apache Software License 2.0":
        move_file("LICENSE_APACHE", "LICENSE")
        remove_file("LICENSE_MIT")
        remove_file("LICENSE_BSD")
        remove_file("LICENSE_ISC")
        remove_file("LICENSE_GPL")

    if "{{cookiecutter.open_source_license}}" == "GNU General Public License v3":
        move_file("LICENSE_GPL", "LICENSE")
        remove_file("LICENSE_MIT")
        remove_file("LICENSE_BSD")
        remove_file("LICENSE_ISC")
        remove_file("LICENSE_APACHE")

    if "{{cookiecutter.open_source_license}}" == "Not open source":
        remove_file("LICENSE_GPL")
        remove_file("LICENSE_MIT")
        remove_file("LICENSE_BSD")
        remove_file("LICENSE_ISC")
        remove_file("LICENSE_APACHE")
