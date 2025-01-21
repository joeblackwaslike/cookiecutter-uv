# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
- Made pyproject.toml the source of truth for version and stubbed __version__ in the __init__.py file to reflect this.