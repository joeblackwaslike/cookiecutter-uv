# spinup-py: Rename + CI/CD & PyPI Publishing — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebrand `create-py-project` → `spinup-py` (package, CLI, import, repo, local path) and add a CI smoke test + release-please → PyPI Trusted Publishing pipeline.

**Architecture:** Phased: (0) mechanical rename, (1) defaults-only `--non-interactive` CLI mode, (2) `build-and-smoke` CI job exercising the built wheel, (3) release-please + OIDC publish in one workflow (publish & docs-deploy gated on `release_created` to dodge the GITHUB_TOKEN no-trigger gotcha), (4) README/docs, (5) human-only manual setup. Branch: `feat/spinup-py-rename-cicd`.

**Tech Stack:** Python 3.10–3.13, uv, Typer, cookiecutter, pydantic v2, pytest, GitHub Actions, `googleapis/release-please-action`, `pypa/gh-action-pypi-publish`.

Spec: `docs/superpowers/specs/2026-06-08-spinup-py-rename-and-cicd-design.md`

---

## File Structure

- `src/create_py_project/` → `src/spinup_py/` (all modules; one responsibility each, unchanged).
- `pyproject.toml` — package name, console script, URLs.
- `src/spinup_py/cli.py` — Typer app: add `--non-interactive`.
- `src/spinup_py/prompts.py` — add `build_default_config()` (pure, non-interactive config).
- `src/spinup_py/scaffold.py` — thread `non_interactive` to skip the push prompt.
- `tests/` — update imports; add non-interactive tests.
- `.github/workflows/main.yml` — add `build-and-smoke` job.
- `.github/workflows/release-please.yml` (new), `release-please-config.json` (new), `.release-please-manifest.json` (new).
- `.github/workflows/on-release-main.yml` — retire the `release:` trigger.
- `README.md`, `mkdocs.yml`, `hooks/scripts/install-cli.sh`, `.serena/project.yml` — name references.

---

## Task 1: Rename import package `create_py_project` → `spinup_py`

**Files:**
- Move: `src/create_py_project/` → `src/spinup_py/`
- Modify: every `from create_py_project`/`import create_py_project` in `src/` and `tests/`

- [ ] **Step 1: Move the package directory (preserve history)**

```bash
git mv src/create_py_project src/spinup_py
```

- [ ] **Step 2: Rewrite all internal imports**

```bash
grep -rl "create_py_project" src tests | while read -r f; do
  sed -i '' 's/create_py_project/spinup_py/g' "$f"
done
# sanity: no references remain in code
grep -rn "create_py_project" src tests || echo "clean"
```

- [ ] **Step 3: Run the suite to confirm the rename is consistent**

Run: `PYTHONPATH="$PWD" .venv/bin/python -m pytest -q`
Expected: PASS (same count as before, currently 47). If imports were missed, failures name the file — fix and re-run.

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "refactor: rename import package create_py_project -> spinup_py"
```

---

## Task 2: Rename the distribution + CLI to `spinup-py` in `pyproject.toml` and `cli.py`

**Files:**
- Modify: `pyproject.toml` (`[project].name`, `[project.scripts]`, `[project.urls]`)
- Modify: `src/spinup_py/cli.py` (Typer `name`, `pkg_version`)

- [ ] **Step 1: Update `pyproject.toml`**

Set:
```toml
[project]
name = "spinup-py"
# ...
[project.scripts]
spinup-py = "spinup_py.cli:app"

[project.urls]
Repository = "https://github.com/joeblackwaslike/spinup-py"
Documentation = "https://joeblackwaslike.github.io/spinup-py/"
Homepage = "https://joeblackwaslike.github.io/spinup-py/"
```
Remove the old `create-py-project = ...` script line.

- [ ] **Step 2: Update `cli.py` identifiers**

In `src/spinup_py/cli.py`: `app = typer.Typer(name="spinup-py", ...)` and `typer.echo(pkg_version("spinup-py"))` (keep the `PackageNotFoundError` fallback).

- [ ] **Step 3: Re-sync so the new entry point installs**

Run: `uv sync` then `uv run spinup-py --version`
Expected: prints `0.1.0` (and the old `create-py-project` command is gone).

- [ ] **Step 4: Run tests + mypy**

Run: `PYTHONPATH="$PWD" .venv/bin/python -m pytest -q && .venv/bin/mypy src`
Expected: PASS / `Success: no issues found`.

- [ ] **Step 5: Commit**

```bash
git add pyproject.toml src/spinup_py/cli.py uv.lock
git commit -m "refactor: rename distribution + CLI to spinup-py"
```

---

## Task 3: Update remaining name references (hooks, serena, mkdocs)

**Files:**
- Modify: `hooks/scripts/install-cli.sh`, `.serena/project.yml`, `mkdocs.yml`

- [ ] **Step 1: Replace command/name references**

```bash
grep -rln "create-py-project\|create_py_project" hooks .serena mkdocs.yml 2>/dev/null
sed -i '' 's/create-py-project/spinup-py/g' hooks/scripts/install-cli.sh .serena/project.yml mkdocs.yml
```
Verify the `install-cli.sh` guard line still references `$CLAUDE_PLUGIN_ROOT` correctly and the install command is `uv tool install --editable .` (unchanged) with status text now saying `spinup-py`.

- [ ] **Step 2: Verify the hook script is still valid**

Run: `shellcheck hooks/scripts/install-cli.sh`
Expected: no output (clean).

- [ ] **Step 3: Commit**

```bash
git add hooks/scripts/install-cli.sh .serena/project.yml mkdocs.yml
git commit -m "refactor: update name references to spinup-py (hooks/serena/mkdocs)"
```

---

## Task 4: Add defaults-only `--non-interactive` — `build_default_config`

**Files:**
- Modify: `src/spinup_py/prompts.py` (add `build_default_config`)
- Test: `tests/test_units.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_units.py
from spinup_py.prompts import build_default_config

def test_build_default_config_uses_defaults():
    cfg = build_default_config("my-proj")
    assert cfg.project_name == "my-proj"
    assert cfg.project_slug == "my_proj"
    assert cfg.open_source_license == "MIT license"
    assert cfg.deptry is True
    assert cfg.include_github_actions is True
    assert cfg.devcontainer is True
    assert cfg.include_docs is False
    assert cfg.codecov is False
    assert cfg.publish_to_pypi is False
```

- [ ] **Step 2: Run it to verify it fails**

Run: `PYTHONPATH="$PWD" .venv/bin/python -m pytest tests/test_units.py::test_build_default_config_uses_defaults -q`
Expected: FAIL (`ImportError: cannot import name 'build_default_config'`).

- [ ] **Step 3: Implement `build_default_config`**

```python
# src/spinup_py/prompts.py  (add near run_prompts)
def build_default_config(project_name: str) -> ProjectConfig:
    """Build a ProjectConfig from saved/built-in defaults with no prompts."""
    defaults = load_user_defaults()
    return ProjectConfig.create(
        project_name=project_name,
        description="",
        author=defaults.author,
        email=defaults.email,
        github_handle=defaults.github_handle,
        python_version=defaults.python_version,
        include_github_actions=True,
        devcontainer=True,
        include_docs=False,
        codecov=False,
        dockerfile=False,
        deptry=True,
        publish_to_pypi=False,
        open_source_license="MIT license",
    )
```

- [ ] **Step 4: Run it to verify it passes**

Run: `PYTHONPATH="$PWD" .venv/bin/python -m pytest tests/test_units.py::test_build_default_config_uses_defaults -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/spinup_py/prompts.py tests/test_units.py
git commit -m "feat: add build_default_config for non-interactive scaffolding"
```

---

## Task 5: Thread `non_interactive` through `run_new` and `scaffold`

**Files:**
- Modify: `src/spinup_py/scaffold.py` (`run_new`, `scaffold`)
- Test: `tests/test_units.py`

- [ ] **Step 1: Write the failing test (push prompt is skipped when non-interactive)**

```python
# tests/test_units.py
from pathlib import Path
import pytest
from spinup_py import scaffold as scaffold_mod

def test_scaffold_non_interactive_skips_push_prompt(tmp_path, monkeypatch):
    cfg = _config(project_name="ni-proj")  # _config helper already in this file
    project_dir = tmp_path / "ni-proj"

    def fake_cookiecutter(*a, **k):
        project_dir.mkdir(parents=True)
        return str(project_dir)
    monkeypatch.setattr(scaffold_mod, "cookiecutter", fake_cookiecutter)
    monkeypatch.setattr(scaffold_mod, "_template_dir", lambda: str(tmp_path))
    monkeypatch.setattr(scaffold_mod, "_run", lambda cmd, cwd: None)  # git no-ops

    # If a questionary prompt is reached, fail loudly:
    def boom(*a, **k):
        raise AssertionError("prompt should not be called in non-interactive mode")
    monkeypatch.setattr(scaffold_mod.questionary, "select", boom)

    scaffold_mod.scaffold(str(project_dir), cfg, non_interactive=True)
    assert (project_dir / ".serena" / "project.yml").exists()
```

- [ ] **Step 2: Run it to verify it fails**

Run: `PYTHONPATH="$PWD" .venv/bin/python -m pytest tests/test_units.py::test_scaffold_non_interactive_skips_push_prompt -q`
Expected: FAIL (`scaffold() got an unexpected keyword argument 'non_interactive'`).

- [ ] **Step 3: Add the `non_interactive` parameter**

In `src/spinup_py/scaffold.py`, change `def scaffold(dest_dir: str, config: ProjectConfig) -> None:` to `def scaffold(dest_dir: str, config: ProjectConfig, non_interactive: bool = False) -> None:` and guard the GitHub block:

```python
    # GitHub
    if not non_interactive:
        push_choice = questionary.select("Push to GitHub?", choices=["public", "private", "skip"], default="skip").ask()
        if push_choice in ("public", "private"):
            console.print("[dim]Creating GitHub repo...[/dim]")
            try:
                subprocess.run(
                    ["gh", "repo", "create", f"{config.github_handle}/{config.project_name}",
                     f"--{push_choice}", "--source=.", "--remote=origin", "--push"],
                    cwd=project_dir, check=True,
                )
            except (subprocess.CalledProcessError, FileNotFoundError) as exc:
                console.print(f"[yellow]GitHub repo creation failed: {exc}[/yellow]")
                console.print("[dim]You can push manually later with: gh repo create[/dim]")
```

Update `run_new`:

```python
def run_new(project_name: str | None, non_interactive: bool = False) -> None:
    if non_interactive:
        if not project_name:
            console.print("[red]--non-interactive requires a project name[/red]")
            raise SystemExit(2)
        from spinup_py.prompts import build_default_config
        config = build_default_config(project_name)
    else:
        from spinup_py.prompts import run_prompts
        config = run_prompts(project_name)
    dest_dir = str(Path.cwd() / config.project_name)
    scaffold(dest_dir, config, non_interactive=non_interactive)
```

- [ ] **Step 4: Run it to verify it passes**

Run: `PYTHONPATH="$PWD" .venv/bin/python -m pytest tests/test_units.py -q && .venv/bin/mypy src`
Expected: PASS / `Success`.

- [ ] **Step 5: Commit**

```bash
git add src/spinup_py/scaffold.py tests/test_units.py
git commit -m "feat: thread non_interactive through run_new/scaffold (skip push prompt)"
```

---

## Task 6: Wire `--non-interactive` into the CLI

**Files:**
- Modify: `src/spinup_py/cli.py`
- Test: `tests/test_units.py`

- [ ] **Step 1: Write the failing test (flag routes to non-interactive)**

```python
# tests/test_units.py
from typer.testing import CliRunner
from spinup_py.cli import app

def test_cli_non_interactive_flag_routes(monkeypatch):
    called = {}
    import spinup_py.scaffold as scaffold_mod
    monkeypatch.setattr(scaffold_mod, "run_new", lambda name, non_interactive=False: called.update(name=name, ni=non_interactive))
    # also patch the symbol imported lazily inside cli.main
    result = CliRunner().invoke(app, ["my-proj", "--non-interactive"])
    assert result.exit_code == 0
    assert called == {"name": "my-proj", "ni": True}
```

- [ ] **Step 2: Run it to verify it fails**

Run: `PYTHONPATH="$PWD" .venv/bin/python -m pytest tests/test_units.py::test_cli_non_interactive_flag_routes -q`
Expected: FAIL (no such option `--non-interactive`).

- [ ] **Step 3: Add the option to the callback and `new` subcommand**

In `src/spinup_py/cli.py`, add to `main(...)` params:
```python
    non_interactive: bool = typer.Option(False, "--non-interactive", "-y", help="Scaffold with defaults, no prompts"),
```
and in the `elif project_name is not None:` branch:
```python
        from spinup_py.scaffold import run_new
        run_new(project_name, non_interactive=non_interactive)
```
Add the same option to `new_cmd` and pass it through to `run_new`.

> Note: the test patches `spinup_py.scaffold.run_new`; ensure `cli.py` calls `run_new` via `from spinup_py.scaffold import run_new` inside the function (lazy import) so the monkeypatch on the module attribute is observed. If patching the module attribute is unreliable, the test may instead assert on `result.stdout`/a created dir — keep the assertion on the routing call.

- [ ] **Step 4: Run it to verify it passes**

Run: `PYTHONPATH="$PWD" .venv/bin/python -m pytest tests/test_units.py -q`
Expected: PASS.

- [ ] **Step 5: Manual end-to-end check**

Run: `cd "$(mktemp -d)" && uv run --project /Users/joe/github/joeblackwaslike/create-py-project spinup-py demo-proj --non-interactive && ls demo-proj`
Expected: `demo-proj/` created with `pyproject.toml`, `src/demo_proj/`, `tests/`; no prompts appeared.

- [ ] **Step 6: Commit**

```bash
git add src/spinup_py/cli.py tests/test_units.py
git commit -m "feat: add --non-interactive flag to the CLI"
```

---

## Task 7: Add the `build-and-smoke` CI job

**Files:**
- Modify: `.github/workflows/main.yml`

- [ ] **Step 1: Append the job** (after `tests-and-type-check`)

```yaml
  build-and-smoke:
    runs-on: ubuntu-latest
    steps:
      - name: Check out
        uses: actions/checkout@v4

      - name: Set up the environment
        uses: ./.github/actions/setup-python-env

      - name: Build distributions
        run: uv build

      - name: Smoke-test the built wheel in a clean venv
        run: |
          set -euo pipefail
          python -m venv /tmp/smoke
          /tmp/smoke/bin/pip install --quiet dist/*.whl
          /tmp/smoke/bin/spinup-py --version
          /tmp/smoke/bin/spinup-py --help
          /tmp/smoke/bin/spinup-py new --help
          /tmp/smoke/bin/spinup-py update --help
          workdir="$(mktemp -d)"
          ( cd "$workdir" && /tmp/smoke/bin/spinup-py smoketest-proj --non-interactive )
          test -f "$workdir/smoketest-proj/pyproject.toml"
          test -d "$workdir/smoketest-proj/src/smoketest_proj"
          test -d "$workdir/smoketest-proj/tests"
          echo "smoke OK"

      - name: Upload distributions
        uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/
```

- [ ] **Step 2: Lint the workflow**

Run: `actionlint .github/workflows/main.yml` (or `uvx actionlint`); if unavailable, validate YAML: `python -c "import yaml,sys; yaml.safe_load(open('.github/workflows/main.yml'))"`
Expected: no errors.

- [ ] **Step 3: Reproduce the smoke steps locally**

Run the body of the smoke step manually from the repo root (build, venv, install wheel, run `spinup-py ... --non-interactive`, assert tree).
Expected: `smoke OK`. (`spinup-py smoketest-proj --non-interactive` must not prompt and must not attempt a git push.)

- [ ] **Step 4: Commit**

```bash
git add .github/workflows/main.yml
git commit -m "ci: add build-and-smoke job exercising the built wheel"
```

---

## Task 8: release-please config + workflow with Trusted Publishing

**Files:**
- Create: `release-please-config.json`, `.release-please-manifest.json`, `.github/workflows/release-please.yml`
- Modify: `.github/workflows/on-release-main.yml` (retire `release:` trigger)

- [ ] **Step 1: Create `release-please-config.json`**

```json
{
  "$schema": "https://raw.githubusercontent.com/googleapis/release-please/main/schemas/config.json",
  "packages": {
    ".": {
      "release-type": "python",
      "package-name": "spinup-py",
      "changelog-path": "CHANGELOG.md",
      "include-component-in-tag": false
    }
  }
}
```

- [ ] **Step 2: Create `.release-please-manifest.json`**

```json
{ ".": "0.1.0" }
```

- [ ] **Step 3: Create `.github/workflows/release-please.yml`**

```yaml
name: release-please

on:
  push:
    branches: [main]

permissions:
  contents: write
  pull-requests: write

jobs:
  release-please:
    runs-on: ubuntu-latest
    outputs:
      release_created: ${{ steps.rp.outputs.release_created }}
      tag_name: ${{ steps.rp.outputs.tag_name }}
    steps:
      - uses: googleapis/release-please-action@v4
        id: rp
        with:
          config-file: release-please-config.json
          manifest-file: .release-please-manifest.json

  publish:
    needs: release-please
    if: ${{ needs.release-please.outputs.release_created == 'true' }}
    runs-on: ubuntu-latest
    environment: pypi
    permissions:
      id-token: write
      contents: read
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ needs.release-please.outputs.tag_name }}
      - name: Set up the environment
        uses: ./.github/actions/setup-python-env
      - name: Build
        run: uv build
      - name: Publish to PyPI (Trusted Publishing)
        uses: pypa/gh-action-pypi-publish@release/v1

  deploy-docs:
    needs: release-please
    if: ${{ needs.release-please.outputs.release_created == 'true' }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ needs.release-please.outputs.tag_name }}
      - name: Set up the environment
        uses: ./.github/actions/setup-python-env
      - name: Deploy documentation
        run: uv run mkdocs gh-deploy --force
```

- [ ] **Step 4: Retire the `release:` trigger in `on-release-main.yml`**

Replace its `on:` block so it no longer fires on release (docs deploy now lives in `release-please.yml`). Either delete the file, or convert it to manual-only:
```yaml
name: release-main (manual fallback)
on:
  workflow_dispatch:
```
(keep the existing `deploy-docs` job body). Document in the file header that automatic docs deploy is handled by `release-please.yml`.

- [ ] **Step 5: Validate the workflows**

Run: `for f in .github/workflows/release-please.yml .github/workflows/on-release-main.yml; do python -c "import yaml; yaml.safe_load(open('$f'))"; done` (and `actionlint` if available).
Expected: no errors. Confirm `.release-please-manifest.json` version matches `pyproject.toml` (`0.1.0`).

- [ ] **Step 6: Commit**

```bash
git add release-please-config.json .release-please-manifest.json .github/workflows/release-please.yml .github/workflows/on-release-main.yml
git commit -m "ci: add release-please + PyPI Trusted Publishing; retire release-triggered docs"
```

---

## Task 9: README & docs

**Files:**
- Modify: `README.md` (+ docs pages referencing the old name)

- [ ] **Step 1: Update install/usage + name references**

```bash
grep -rln "create-py-project\|create_py_project" README.md docs 2>/dev/null
sed -i '' 's/create-py-project/spinup-py/g; s/create_py_project/spinup_py/g' README.md
```
Then by hand: ensure Quickstart shows `uvx spinup-py my-project` and `uv tool install spinup-py`; add an "Install from source" note (`uv tool install --editable .`); document the `new`/`update` subcommands, `--update`, `--version`, and `--non-interactive`; add a one-line note that `spinup-py` is the Python sibling of `spinup-ts`.

- [ ] **Step 2: Verify no stale references remain**

Run: `grep -rn "create-py-project\|create_py_project" README.md docs src tests pyproject.toml | grep -v "{{cookiecutter" || echo "clean"`
Expected: `clean` (the cookiecutter template tree is intentionally untouched).

- [ ] **Step 3: Commit**

```bash
git add README.md docs
git commit -m "docs: rebrand README/docs to spinup-py + document --non-interactive"
```

---

## Task 10: Full local gate + push + open PR

**Files:** none (verification)

- [ ] **Step 1: Run the full local gate**

Run:
```bash
PYTHONPATH="$PWD" .venv/bin/python -m pytest -q
.venv/bin/mypy src
.venv/bin/deptry .
.venv/bin/pre-commit run -a
```
Expected: all green.

- [ ] **Step 2: Push and open the PR**

```bash
git push -u origin feat/spinup-py-rename-cicd
gh pr create --repo joeblackwaslike/create-py-project --fill --title "Rename to spinup-py + CI/CD & PyPI publishing"
```
Expected: PR created; `quality`, `tests-and-type-check (3.10–3.13)`, and the new `build-and-smoke` job run and pass.

- [ ] **Step 3: Merge once green** (the maintainer merges; do not self-merge unless instructed).

---

## Task 11: Manual setup checklist (human-only — cannot be automated)

These are **operator actions**; an agent cannot perform them. Surface this checklist to the user.

- [ ] PyPI **pending publisher** (PyPI → account → Publishing): project `spinup-py`, owner `joeblackwaslike`, repo `spinup-py`, workflow `release-please.yml`, environment `pypi`.
- [ ] Create GitHub **Environment** `pypi` (no required reviewers).
- [ ] (Optional) TestPyPI dry-run: add a second pending publisher on test.pypi.org and a one-off `repository-url: https://test.pypi.org/legacy/` publish to validate OIDC before the first real release.
- [ ] **Rename the GitHub repo** `create-py-project` → `spinup-py`, then `git remote set-url origin git@github.com:joeblackwaslike/spinup-py.git`.
- [ ] **SonarCloud**: update project key/binding to `spinup-py` (cosmetic).
- [ ] **Local path LAST** (after everything above is committed, pushed, and the repo is renamed):
  ```bash
  cd ~ && mv ~/github/joeblackwaslike/create-py-project ~/github/joeblackwaslike/spinup-py
  ```
- [ ] First release: merge the release-please PR → confirm GitHub Release, PyPI `spinup-py 0.1.0`, and docs deploy.

---

## Self-Review

- **Spec coverage:** Phase 0 → Tasks 1–3 + 9 + 11 (repo/local path). Phase 1 → Tasks 4–6. Phase 2 → Task 7. Phase 3 → Task 8. Phase 4 → Task 9. Manual setup → Task 11. ✓ All spec sections mapped.
- **Placeholder scan:** No TBD/“add error handling”/empty-test placeholders; every code step has concrete content. ✓
- **Type/name consistency:** import package `spinup_py`, dist/command `spinup-py`, `build_default_config(project_name)`, `run_new(project_name, non_interactive=False)`, `scaffold(dest_dir, config, non_interactive=False)`, manifest version `0.1.0` == `pyproject` — consistent across tasks. ✓
- **Note:** the `_config(...)` helper referenced in Tasks 5 already exists in `tests/test_units.py` (from the prior round). If executing tasks out of order, confirm it's present.
