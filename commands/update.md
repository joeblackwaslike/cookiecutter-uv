# /update

**Description:** Retrofit an existing Python project with create-py-project tooling and best practices.

**Argument hint:** `[project-path]`

**Allowed tools:** Bash, Read, Write, Skill

---

## Instructions

You are helping the user apply missing Python project patterns to an existing codebase using `create-py-project update`.

### Step 1 — Resolve target directory

If an argument was provided, use it. Otherwise ask:

> Which project directory should I update? (default: current directory)

Resolve to an absolute path:

```bash
TARGET_DIR="$(cd "GIVEN_PATH" && pwd)"
echo "Target: $TARGET_DIR"
```

### Step 2 — Run the update command

```bash
create-py-project update "$TARGET_DIR"
```

This will:
1. Detect which patterns are missing from the target project
2. Present a multi-select checkbox list
3. Apply the selected updates
4. Print a summary

If `create-py-project` is not on PATH, fall back to:

```bash
python3 -c "
import sys
# find plugin src
import subprocess, pathlib
plugin_root = pathlib.Path('$CLAUDE_PLUGIN_ROOT')
sys.path.insert(0, str(plugin_root / 'src'))
from create_py_project.update import update_project
update_project('$TARGET_DIR')
"
```

### Step 3 — Report results

After the command completes, summarize:
- Which updates were applied
- Any updates that failed and why
- Suggested next steps (e.g., `uv sync`, `uv run pre-commit install`, `git add -A && git commit`)

### Available update options

| Option | What it adds |
|--------|-------------|
| devcontainer | `.devcontainer/` with Claude Code dev environment |
| AGENTS.md | Agent instruction file (Codex, Gemini, Cursor, Copilot) |
| CLAUDE.md | `@AGENTS.md` import for Claude Code |
| GitHub Actions CI | `.github/` directory — lint, test, build workflows |
| PyPI publish workflow | `.github/workflows/on-release-main.yml` |
| ruff config | `[tool.ruff]` block in `pyproject.toml` |
| mypy config | `[tool.mypy]` block in `pyproject.toml` |
| pytest config | `[tool.pytest.ini_options]` in `pyproject.toml` |
| coverage config | `[tool.coverage.*]` in `pyproject.toml` |
| pre-commit + WPS | `.pre-commit-config.yaml` with ruff + WPS + prettier |
| deptry | `deptry` added to dev deps |
| Docusaurus docs | `docs/` Docusaurus site scaffold |
| Dockerfile | Multi-stage Python Docker build |
| Init Beads | `.beads/` via `bd init --skip-agents` |
| Init Serena | `.serena/project.yml` |
