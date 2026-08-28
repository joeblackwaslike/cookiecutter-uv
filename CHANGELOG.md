# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.1](https://github.com/joeblackwaslike/spinup-py/compare/v0.3.0...v0.3.1) (2026-08-28)


### Bug Fixes

* post-gen hook initializes beads with --shared-server and export.auto=true ([99e914b](https://github.com/joeblackwaslike/spinup-py/commit/99e914b1e940bb188282d418b97444c48f587db4))
* **template:** point generated README links at spinup-py ([bc8cffc](https://github.com/joeblackwaslike/spinup-py/commit/bc8cffc7618a9c319391d82a0db7a2da3da41bca))


### Documentation

* rebrand from Cookiecutter UV to agentic Python scaffolding ([17f23e4](https://github.com/joeblackwaslike/spinup-py/commit/17f23e4096a53fff2113ab86146b9aa6a82e66f5))
* standardize README badges, install, and license ([3abd436](https://github.com/joeblackwaslike/spinup-py/commit/3abd4368eecc18a54e614a35ec31e2d49f20c973))

## [0.3.0](https://github.com/joeblackwaslike/spinup-py/compare/v0.2.0...v0.3.0) (2026-06-12)


### Features

* **template:** add .tool-versions with dynamic python version ([646106d](https://github.com/joeblackwaslike/spinup-py/commit/646106d3915af1c1d014bd5399ceb015bb806b41))
* **template:** restructure docs to match spinup-ts layout ([047fd7f](https://github.com/joeblackwaslike/spinup-py/commit/047fd7f7c4cb5c1bcf9b24d97df662e955b1d824))
* use serena CLI for project init and add --shared-server to beads ([37197ac](https://github.com/joeblackwaslike/spinup-py/commit/37197ac278af2f7b9316d8af0cfe2ab480098bcc))


### Bug Fixes

* **ci:** docs-deploy deps + release-please/prettier hygiene ([#5](https://github.com/joeblackwaslike/spinup-py/issues/5)) ([4fcd905](https://github.com/joeblackwaslike/spinup-py/commit/4fcd90527182664ff594e23174a8af34e1428db9))
* **ci:** exclude release-please-owned files from prettier ([72134db](https://github.com/joeblackwaslike/spinup-py/commit/72134db26ed75e8f81a4a82384af05bb6bb76d23))
* **ci:** install mkdocs deps for docs deploy ([e8b66ba](https://github.com/joeblackwaslike/spinup-py/commit/e8b66babd0778de7e6d9333dcaf51f9c3694bef9))
* **ci:** use docs group in the manual on-release-main docs deploy too ([32d3ed6](https://github.com/joeblackwaslike/spinup-py/commit/32d3ed62442f6ca68385cd340fe26fb6fa024930))


### Documentation

* **template:** add setup step to AGENTS.md ([e052441](https://github.com/joeblackwaslike/spinup-py/commit/e0524413b7e735c5fa0f8e410aed07d429bb56a7))

## [0.2.0](https://github.com/joeblackwaslike/spinup-py/compare/v0.1.0...v0.2.0) (2026-06-10)


### Features

* add --non-interactive flag to the CLI ([5529e8b](https://github.com/joeblackwaslike/spinup-py/commit/5529e8b86f88900ba39b71fb689cff89e29ba9d1))
* add build_default_config for non-interactive scaffolding ([17aac2e](https://github.com/joeblackwaslike/spinup-py/commit/17aac2e825bf1e43a535c9e19231170ae57d3c3d))
* add CLAUDE.md template to generated projects ([3da575c](https://github.com/joeblackwaslike/spinup-py/commit/3da575c051e618a0faa238dddd9425138d209495))
* fetch cookiecutter template from GitHub when not installed from source ([9b9ba73](https://github.com/joeblackwaslike/spinup-py/commit/9b9ba7363c58d850ff9e68ae617ffdba53e11a8a))
* thread non_interactive through run_new/scaffold (skip push prompt) ([2b63682](https://github.com/joeblackwaslike/spinup-py/commit/2b63682870c01ad377dcc52aea4bfc03d615ef74))


### Bug Fixes

* repoint tool configs to spinup_py import path ([497cfa2](https://github.com/joeblackwaslike/spinup-py/commit/497cfa2ad077b925877ad3aedaa3bc6a1efd361a))
* **review:** handle pydantic ValidationError and missing-git OSError ([c4b4fa0](https://github.com/joeblackwaslike/spinup-py/commit/c4b4fa0fcaff2035553999dc41932aa126a8efda))
* **review:** pin uv base image to 0.11.19 in template Dockerfile ([ba11d72](https://github.com/joeblackwaslike/spinup-py/commit/ba11d729d9dabe86e070ca5d8f561aacdd13eb9e))
* **review:** restructure template Dockerfile and wire .dockerignore ([b851389](https://github.com/joeblackwaslike/spinup-py/commit/b851389d6abb01cfd78380844abd2e14d7e15492))
* **security:** pin third-party actions to SHAs and harden template Dockerfile ([3ff2fe0](https://github.com/joeblackwaslike/spinup-py/commit/3ff2fe0ac0c98140c18f7c1ebdfabc0139992eae))
* **security:** resolve SonarCloud hotspots + harden template Dockerfile ([#4](https://github.com/joeblackwaslike/spinup-py/issues/4)) ([c3355d8](https://github.com/joeblackwaslike/spinup-py/commit/c3355d8962d6b995d03702d434aafaad9a9f5ff9))


### Documentation

* add Discord channel and invite badges ([93900a0](https://github.com/joeblackwaslike/spinup-py/commit/93900a06b59146574beadbdb36476739093ccf85))
* design spec for spinup-py rename + CI/CD & PyPI publishing ([aca6805](https://github.com/joeblackwaslike/spinup-py/commit/aca6805c439d1e9e7971e1784934e71985c6dc6b))
* flip template — AGENTS.md source of truth, CLAUDE.md = @AGENTS.md ([642110e](https://github.com/joeblackwaslike/spinup-py/commit/642110eb28759dd89905c0d930bf4869b7520d13))
* implementation plan for spinup-py rename + CI/CD ([f3d5481](https://github.com/joeblackwaslike/spinup-py/commit/f3d5481b65cad2756e3725e6119efeb09474eb82))
* include local-path rename (last) in spinup-py spec ([81b4b31](https://github.com/joeblackwaslike/spinup-py/commit/81b4b310e87ea8595320173bae517aeb2a7c368d))
* rebrand README/docs to spinup-py + document --non-interactive and SPINUP_PY_TEMPLATE ([b816878](https://github.com/joeblackwaslike/spinup-py/commit/b8168788bdd92c6e16fda786be5a08e14cb28990))

## [Unreleased]

### Added

### Changed

### Removed

## [1.1.0] - 2025-01-18

### Added

- Added support for src layout
- Added docker-compose.yaml file

### Changed

- Updated the default ruff version to 0.9.2
- Updated the default deptry version to 0.22.0

## [1.0.1] - 2025-01-09

### Added

- Added default settings to devcontainer
- Added github issue and pull request templates
- Added `wemake-python-styleguide` checks to the linter checks and pre-commit, pyproject.toml updated to ensure alignment with ruff, setup.cfg added to deal with flake8 checks.
- Added .python-version file for pyenv/uv
- Added AUTHORS.md and CHANGELOG.md files
- Added a few stub files to tests folder
- Added an inner and outer vscode workspace files
- Added a py.typed to inner package to allow for type checking.

### Changed

- Changed the default Python version to 3.11.
- Made full use of .editorconfig template
- Added alternative bootstrap commands to the create a new repo section.
- Made pyproject.toml the source of truth for version and stubbed **version** in the **init**.py file to reflect this.
