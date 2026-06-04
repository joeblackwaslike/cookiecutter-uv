# {{cookiecutter.project_name}}

{{cookiecutter.project_description}}

## Stack

- **Language:** Python (uv for dependency management)
- **Style:** async-first, Pydantic v2 for models, type-annotated throughout

## Commands

```sh
uv run pytest          # run tests
uv run ruff check .    # lint
uv run ruff format .   # format
uv run mypy .          # type check
```

## Conventions

- Tests live in `tests/`, mirroring `src/` structure
- Use `uv add` to add dependencies, never edit `pyproject.toml` by hand for deps
- Prefer `pathlib.Path` over `os.path`
- Async by default; only use sync where the library forces it

## Agent Instruction Files

This project uses `CLAUDE.md` as the single source of truth for both Claude Code and Codex:

- **Claude Code** reads this file natively.
- **Codex CLI** reads it via `project_doc_fallback_filenames = ["CLAUDE.md"]` in `~/.codex/config.toml` (no AGENTS.md needed).
- Do **not** use `@filename` import syntax in AGENTS.md — it is Claude Code-only and does nothing in Codex.
