# spinup-py: rename + CI/CD & PyPI publishing — design

**Date:** 2026-06-08
**Repo:** `joeblackwaslike/create-py-project` → renaming to `spinup-py`
**Status:** approved design, pending spec review → implementation plan

## Context

The CLI in this repo (currently `create-py-project`) is a working, installable Typer
app, but it is not published to PyPI and the README's `uvx create-py-project` /
`uv tool install create-py-project` commands therefore fail. Publishing surfaced a
naming blocker: PyPI rejects `create-py-project` via its name-similarity guard
(collision with the existing `create-py-project-by-bhimrazy`).

The tool also has a TypeScript sibling, `create-ts-project` (npm). We want a
**matched, memorable pair** that is free on both registries and clears the PyPI guard.
`create-ts` (npm) and `scaffold-ts` (npm) are taken, and `scaffold-py`/`create-py-project`
are guard-blocked on PyPI. The chosen pair is **`spinup-py`** (PyPI, this repo) /
**`spinup-ts`** (npm, the sibling repo, renamed separately). Both verified free on PyPI
and npm with no separator-collapsed neighbor that would trip the guard.

The intended outcome: rebrand this tool to `spinup-py`, give it real CI gates + a
smoke test of the _published artifact_, and a release-please → Trusted Publishing
pipeline so a merged release PR ships to PyPI.

## Goals

- Rebrand the package, CLI command, and import package to `spinup-py` / `spinup_py`.
- Rename the GitHub repo to `spinup-py`.
- Add a CLI `--non-interactive` mode (defaults-only) so the tool can scaffold without prompts.
- Add a CI smoke test that builds the wheel, installs it clean, and exercises the real binary.
- Automate version bump + CHANGELOG via release-please; publish to PyPI via Trusted Publishing (OIDC) on release-PR merge.
- Make the README install/usage instructions truthful post-publish.

## Non-goals

- Renaming the cookiecutter template tree (`{{cookiecutter.project_name}}/`) — unaffected.
- Override flags for `--non-interactive` (`--python`, `--author`, feature toggles) — future extension (YAGNI).
- Changing the template's own (generated-project) release tooling.
- Renaming/repointing the TS sibling — tracked separately on its repo.

## Locked decisions

| Decision            | Choice                                                                               |
| ------------------- | ------------------------------------------------------------------------------------ |
| PyPI/npm name pair  | `spinup-py` / `spinup-ts`                                                            |
| PyPI auth           | **Trusted Publishing (OIDC)** — no stored token                                      |
| Smoke test          | Build wheel → install clean → run binary **+ non-interactive scaffold**, assert tree |
| Promotion gate      | **Merge the release-please PR ⇒ publish** (CI green required to merge)               |
| Import package      | Rename `create_py_project` → `spinup_py`                                             |
| GitHub repo         | Rename `create-py-project` → `spinup-py`                                             |
| `--non-interactive` | Defaults-only                                                                        |
| Docs deploy         | Folded into the release-please workflow (see gotcha)                                 |

## Phase 0 — Rename to spinup-py

- `src/create_py_project/` → `src/spinup_py/`; update every `from create_py_project...` / `import create_py_project` (cli.py, scaffold.py, update.py, prompts.py, types.py, tests).
- `pyproject.toml`: `[project].name = "spinup-py"`; `[project.scripts]` → `spinup-py = "spinup_py.cli:app"`; `[tool.setuptools.packages.find] where = ["src"]` already generic; update URLs to `…/spinup-py`.
- `cli.py`: `typer.Typer(name="spinup-py", …)`, `pkg_version("spinup-py")`, fallback string.
- `.serena/project.yml`, `hooks/scripts/install-cli.sh` (editable install + status text), `tests/` imports.
- Repo rename (GitHub UI, user action): update `origin` remote, README badges, `mkdocs.yml` site refs, links.
- Re-point SonarCloud project key to `spinup-py` (user action; see manual setup).
- **Rename everything**, in this order: import package → PyPI/CLI name → GitHub repo → **local clone directory** (`~/github/joeblackwaslike/create-py-project` → `…/spinup-py`). The local-path move is **done last** (it changes the working directory, so it must follow all in-repo edits, commit, push, and the GitHub rename).

## Phase 1 — CLI `--non-interactive` (defaults-only)

- Add `--non-interactive` / `--yes` to the `main` callback and `new` subcommand.
- Thread `non_interactive: bool` through `run_new(project_name, non_interactive)` → `scaffold(..., non_interactive)`.
- When set: build `ProjectConfig` from `load_user_defaults()` + built-in defaults + positional name, **without** any `questionary` prompt; skip the confirm; in `scaffold()`, skip the "Push to GitHub?" prompt (default = no push) and the `_copy_dir` replace prompt path is not reached for new scaffolds.
- Files: `cli.py`, `prompts.py` (new non-interactive config builder), `scaffold.py` (guard the push prompt).

## Phase 2 — `build-and-smoke` CI job (in `main.yml`)

- Runs on PR + push to main alongside `quality` and `tests-and-type-check`.
- Steps: `uv build` → create clean venv (`uv venv` / system venv, _not_ `uv run`) → `pip install dist/*.whl` → assert `spinup-py --version` (matches `pyproject` version), `--help`, `new --help`, `update --help` exit 0 → in a temp dir run `spinup-py smoketest-proj --non-interactive` → assert expected tree (`pyproject.toml`, `src/smoketest_proj/`, `tests/`, etc.).
- Purpose: catch broken entry points, missing runtime deps, and packaged-scaffold regressions that `uv run`-based tests miss.

## Phase 3 — release-please + Trusted Publishing (`release-please.yml`)

Single workflow on `push: main`:

- **Job `release-please`**: `googleapis/release-please-action`, manifest mode
  (`release-please-config.json` with `"release-type": "python"`,
  `.release-please-manifest.json` bootstrapped to `0.1.0`). Maintains
  `[project].version` in `pyproject.toml` + `CHANGELOG.md`, opens/updates the
  release PR; on merge it tags + creates the GitHub Release. Outputs `release_created`, `tag_name`.
- **Job `publish`** (`needs: release-please`, `if: needs.release-please.outputs.release_created == 'true'`):
  checkout the tag → `uv build` → `pypa/gh-action-pypi-publish` with
  `permissions: { id-token: write }`, `environment: pypi`. No token.
- **Job `deploy-docs`** (`if: release_created`): `uv run mkdocs gh-deploy --force`.

### ⚠️ Gotcha (drives the single-workflow shape)

Releases created by the default `GITHUB_TOKEN` **do not trigger** other workflows.
A separate `on: release: published` workflow (the current `on-release-main.yml`)
would therefore **silently stop firing** once releases come from release-please.
So publish _and_ docs-deploy are jobs **inside** the release-please workflow,
gated on `release_created`, instead of separate `on: release` workflows — no PAT needed.
Retire the `release:` trigger of `on-release-main.yml` (or keep it for manual-release fallback only).

Conventional commits drive the bump (repo already follows this).

## Phase 4 — README & docs

- Install: `uvx spinup-py my-project` / `uv tool install spinup-py` (work post-publish) + a short "install from source" note.
- Usage: document `new` / `update` subcommands, `--update`, `--version`, and `--non-interactive`.
- Note `spinup-py` is the Python sibling of `spinup-ts`.

## One-time manual setup (user — cannot be automated here)

1. **PyPI pending publisher** (PyPI → account → Publishing): project `spinup-py`, owner `joeblackwaslike`, repo `spinup-py` (post-rename), workflow `release-please.yml`, environment `pypi`.
2. **GitHub Environment** `pypi` (no required reviewers — merge is the gate).
3. **Rename GitHub repo** `create-py-project` → `spinup-py`.
4. **SonarCloud**: update project key / binding to `spinup-py` (optional, cosmetic).
5. (Optional) reserve `spinup-py` on PyPI before first publish to avoid sniping.

## File change summary

- **Rename/move:** `src/create_py_project/` → `src/spinup_py/` (+ all imports & tests).
- **Modify:** `pyproject.toml`, `cli.py`, `prompts.py`, `scaffold.py`, `.serena/project.yml`, `hooks/scripts/install-cli.sh`, `README.md`, `mkdocs.yml`, `.github/workflows/main.yml`, `.github/workflows/on-release-main.yml` (retire release trigger).
- **New:** `.github/workflows/release-please.yml`, `release-please-config.json`, `.release-please-manifest.json`, `tests/test_cli_smoke.py` (or smoke as a CI step).

## Testing / verification

- Local: full `pytest` (incl. renamed imports + new non-interactive scaffold test) green; `mypy`, `deptry`, pre-commit green.
- Manual: `uv build` then install the wheel in a throwaway venv and run `spinup-py smoketest --non-interactive`.
- CI: open a throwaway PR → `build-and-smoke` green.
- Release dry-run: optionally publish `0.1.0` to **TestPyPI** first (separate pending publisher) to validate the OIDC flow before the real PyPI release.
- First real release: merge the release-please PR → confirm GitHub Release, PyPI `spinup-py 0.1.0`, and docs deploy.

## Risks / open items

- PyPI guard could still reject `spinup-py` at first upload (low risk — distinct, no collapsed-neighbor). Mitigation: reserve early / TestPyPI dry-run.
- Repo rename touches the Claude plugin / marketplace entry if one references `create-py-project` — verify during implementation.
- Import-package rename is broad mechanical churn — covered by the existing test suite + smoke test.
