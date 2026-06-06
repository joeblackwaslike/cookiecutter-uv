from __future__ import annotations

import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import questionary
import tomlkit
from rich.console import Console
from rich.table import Table

console = Console()

# Template source: {{cookiecutter.project_name}}/ relative to the project root
_TEMPLATE_ROOT = Path(__file__).parent.parent.parent / "{{cookiecutter.project_name}}"

# ── TOML blocks injected into pyproject.toml ─────────────────────────────────

_RUFF_TOML = """\
[tool.ruff]
target-version = "py312"
line-length = 100
fix = true

[tool.ruff.lint]
select = [
    "A",    # flake8-builtins
    "B",    # flake8-bugbear
    "C4",   # flake8-comprehensions
    "C90",  # maccabe
    "COM",  # flake8-commas
    "D",    # pydocstyle
    "DTZ",  # flake8-datetimez
    "E",    # pycodestyle
    "ERA",  # flake8-eradicate
    "EXE",  # flake8-executable
    "F",    # pyflakes
    "FBT",  # flake8-boolean-trap
    "FLY",  # pyflint
    "FURB", # refurb
    "G",    # flake8-logging-format
    "I",    # isort
    "ICN",  # flake8-import-conventions
    "ISC",  # flake8-implicit-str-concat
    "LOG",  # flake8-logging
    "N",    # pep8-naming
    "PERF", # perflint
    "PIE",  # flake8-pie
    "PL",   # pylint
    "PT",   # flake8-pytest-style
    "PTH",  # flake8-use-pathlib
    "Q",    # flake8-quotes
    "RET",  # flake8-return
    "RSE",  # flake8-raise
    "RUF",  # ruff
    "S",    # flake8-bandit
    "SIM",  # flake8-simpify
    "SLF",  # flake8-self
    "SLOT", # flake8-slots
    "T100", # flake8-debugger
    "TRY",  # tryceratops
    "UP",   # pyupgrade
    "W",    # pycodestyle
    "YTT",  # flake8-2020
]
ignore = [
    "A005", "COM812", "D100", "D104", "D106", "D203", "D212", "D401",
    "D404", "D405", "E501", "E731", "ISC001", "ISC003", "PLR09",
    "PLR2004", "PLR6301", "TRY003",
]
external = ["WPS"]

[tool.ruff.lint.pydocstyle]
convention = "google"

[tool.ruff.lint.flake8-quotes]
inline-quotes = "double"

[tool.ruff.lint.mccabe]
max-complexity = 24

[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F401", "F403"]
"tests/*.py" = ["S101", "S105", "S404", "S603", "S607", "D103"]

[tool.ruff.format]
preview = true
quote-style = "double"
indent-style = "space"
docstring-code-format = false
"""

_MYPY_TOML = """\
[tool.mypy]
files = ["src"]
plugins = ["pydantic.mypy"]
strict = true
disallow_untyped_defs = true
disallow_any_unimported = true
no_implicit_optional = true
check_untyped_defs = true
warn_return_any = true
warn_unused_ignores = true
show_error_codes = true
warn_unreachable = true
"""

_PYTEST_TOML = """\
[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
"""

_COVERAGE_TOML = """\
[tool.coverage.run]
branch = true
source = ["src"]

[tool.coverage.report]
skip_empty = true
"""

# ── Helpers ───────────────────────────────────────────────────────────────────


@dataclass
class UpdateOption:
    value: str
    label: str
    hint: str
    apply: Callable[[Path], None]


def _get_project_name(target: Path) -> str:
    pyproject = target / "pyproject.toml"
    if pyproject.exists():
        try:
            doc = tomlkit.parse(pyproject.read_text())
            return str(doc["project"]["name"])  # type: ignore[index]
        except Exception:
            pass
    return target.name


def _has_toml_section(pyproject_path: Path, *keys: str) -> bool:
    if not pyproject_path.exists():
        return False
    try:
        node: object = tomlkit.parse(pyproject_path.read_text())
        for key in keys:
            node = node[key]  # type: ignore[index]
        return True
    except KeyError:
        return False


def _append_toml(pyproject_path: Path, content: str) -> None:
    text = pyproject_path.read_text()
    pyproject_path.write_text(text.rstrip() + "\n\n" + content.strip() + "\n")


def _copy_dir(src_rel: str, target: Path, project_name: str) -> None:
    src = _TEMPLATE_ROOT / src_rel
    dst = target / src_rel
    if not src.exists():
        console.print(f"[yellow]Template source not found: {src}[/yellow]")
        return
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    _substitute_vars(dst, project_name)


def _copy_file(src_rel: str, target: Path, project_name: str) -> None:
    src = _TEMPLATE_ROOT / src_rel
    dst = target / src_rel
    if not src.exists():
        console.print(f"[yellow]Template source not found: {src}[/yellow]")
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    text = _render_template(src.read_text(encoding="utf-8"), project_name)
    dst.write_text(text, encoding="utf-8")


def _render_template(text: str, project_name: str) -> str:
    text = text.replace("{{cookiecutter.project_name}}", project_name)
    text = text.replace("{{cookiecutter.project_slug}}", project_name.replace("-", "_"))
    # Strip remaining unresolved cookiecutter expressions
    text = re.sub(r"\{\{cookiecutter\.[^}]+\}\}", "", text)
    return text


def _substitute_vars(directory: Path, project_name: str) -> None:
    for f in directory.rglob("*"):
        if f.is_file():
            try:
                f.write_text(_render_template(f.read_text(encoding="utf-8"), project_name))
            except (UnicodeDecodeError, PermissionError):
                pass


def _add_deptry(pyproject_path: Path) -> None:
    doc = tomlkit.parse(pyproject_path.read_text())
    try:
        dep_groups = doc["dependency-groups"]  # type: ignore[index]
    except KeyError:
        _append_toml(pyproject_path, '[dependency-groups]\ndev = ["deptry>=0.23.0"]\n')
        return
    try:
        dev_deps = dep_groups["dev"]  # type: ignore[index]
        dev_deps.append("deptry>=0.23.0")  # type: ignore[union-attr]
    except KeyError:
        dep_groups["dev"] = ["deptry>=0.23.0"]  # type: ignore[index]
    pyproject_path.write_text(tomlkit.dumps(doc))


def _run_beads(target: Path) -> None:
    try:
        result = subprocess.run(
            ["bd", "init", "--skip-agents", "--non-interactive"],
            cwd=target,
            capture_output=True,
        )
        if result.returncode != 0:
            console.print("[yellow]bd init failed — check beads CLI installation[/yellow]")
    except FileNotFoundError:
        console.print("[yellow]bd not found — install the beads CLI to use this feature[/yellow]")


def _init_serena(target: Path, project_name: str) -> None:
    serena_dir = target / ".serena"
    serena_dir.mkdir(exist_ok=True)
    (serena_dir / "project.yml").write_text(
        f"project_name: {project_name}\nlanguage: python\n"
    )


# ── Detection ─────────────────────────────────────────────────────────────────


def detect_available_updates(target: Path) -> list[UpdateOption]:
    project_name = _get_project_name(target)
    pyproject = target / "pyproject.toml"
    options: list[UpdateOption] = []

    if not (target / ".devcontainer").exists():
        pn = project_name  # capture for lambda
        options.append(UpdateOption(
            value="devcontainer",
            label="Add .devcontainer/",
            hint="Full Claude Code dev environment (custom image, mounts, API keys)",
            apply=lambda t, p=pn: _copy_dir(".devcontainer", t, p),
        ))

    if not (target / "AGENTS.md").exists():
        pn = project_name
        options.append(UpdateOption(
            value="agents_md",
            label="Add AGENTS.md",
            hint="Agent instruction file (Codex, Gemini, Cursor, Copilot)",
            apply=lambda t, p=pn: _copy_file("AGENTS.md", t, p),
        ))

    if not (target / "CLAUDE.md").exists():
        options.append(UpdateOption(
            value="claude_md",
            label="Add CLAUDE.md",
            hint="Single-line @AGENTS.md import for Claude Code",
            apply=lambda t: (t / "CLAUDE.md").write_text("@AGENTS.md\n"),
        ))

    if not (target / ".github" / "workflows").exists():
        pn = project_name
        options.append(UpdateOption(
            value="github_actions",
            label="Add GitHub Actions CI (.github/workflows/)",
            hint="Lint, typecheck, test, build",
            apply=lambda t, p=pn: _copy_dir(".github", t, p),
        ))
    elif not (target / ".github" / "workflows" / "on-release-main.yml").exists():
        pn = project_name
        options.append(UpdateOption(
            value="pypi_publish",
            label="Add PyPI publish workflow",
            hint=".github/workflows/on-release-main.yml",
            apply=lambda t, p=pn: _copy_file(".github/workflows/on-release-main.yml", t, p),
        ))

    if pyproject.exists() and not _has_toml_section(pyproject, "tool", "ruff"):
        options.append(UpdateOption(
            value="ruff",
            label="Add ruff config to pyproject.toml",
            hint="Full linting ruleset with WPS support, google docstrings",
            apply=lambda t: _append_toml(t / "pyproject.toml", _RUFF_TOML),
        ))

    if pyproject.exists() and not _has_toml_section(pyproject, "tool", "mypy"):
        options.append(UpdateOption(
            value="mypy",
            label="Add mypy config to pyproject.toml",
            hint="Strict typing with pydantic plugin",
            apply=lambda t: _append_toml(t / "pyproject.toml", _MYPY_TOML),
        ))

    if pyproject.exists() and not _has_toml_section(pyproject, "tool", "pytest"):
        options.append(UpdateOption(
            value="pytest",
            label="Add pytest config to pyproject.toml",
            hint='pythonpath = ["src"], testpaths = ["tests"]',
            apply=lambda t: _append_toml(t / "pyproject.toml", _PYTEST_TOML),
        ))

    if pyproject.exists() and not _has_toml_section(pyproject, "tool", "coverage"):
        options.append(UpdateOption(
            value="coverage",
            label="Add coverage config to pyproject.toml",
            hint="Branch coverage, src source",
            apply=lambda t: _append_toml(t / "pyproject.toml", _COVERAGE_TOML),
        ))

    if not (target / ".pre-commit-config.yaml").exists():
        pn = project_name
        options.append(UpdateOption(
            value="pre_commit",
            label="Add .pre-commit-config.yaml",
            hint="ruff + WPS + prettier hooks",
            apply=lambda t, p=pn: _copy_file(".pre-commit-config.yaml", t, p),
        ))

    if pyproject.exists() and "deptry" not in pyproject.read_text():
        options.append(UpdateOption(
            value="deptry",
            label="Add deptry to dev dependencies",
            hint="Detects unused / missing / misplaced dependencies",
            apply=lambda t: _add_deptry(t / "pyproject.toml"),
        ))

    if not (target / "docs").exists():
        pn = project_name
        options.append(UpdateOption(
            value="docs",
            label="Add Docusaurus docs site (docs/)",
            hint="Copy Docusaurus scaffold from template",
            apply=lambda t, p=pn: _copy_dir("docs", t, p),
        ))

    if not (target / "Dockerfile").exists():
        pn = project_name
        options.append(UpdateOption(
            value="dockerfile",
            label="Add Dockerfile",
            hint="Multi-stage Python build",
            apply=lambda t, p=pn: _copy_file("Dockerfile", t, p),
        ))

    if not (target / ".beads").exists():
        options.append(UpdateOption(
            value="beads",
            label="Initialize Beads task manager",
            hint="Runs: bd init --skip-agents",
            apply=lambda t: _run_beads(t),
        ))

    if not (target / ".serena" / "project.yml").exists():
        pn = project_name
        options.append(UpdateOption(
            value="serena",
            label="Initialize Serena project config",
            hint="Creates .serena/project.yml",
            apply=lambda t, p=pn: _init_serena(t, p),
        ))

    return options


# ── Entry point ───────────────────────────────────────────────────────────────


def update_project(target_dir: str) -> None:
    target = Path(target_dir).resolve()
    if not target.exists():
        console.print(f"[red]Directory not found: {target}[/red]")
        raise SystemExit(1)

    console.rule("[bold blue]create-py-project update[/bold blue]")
    console.print(f"[dim]Target: {target}[/dim]\n")

    available = detect_available_updates(target)
    if not available:
        console.print("[green]✓ Project is already up to date![/green]")
        return

    choices = [
        questionary.Choice(
            f"{o.label}  [dim]{o.hint}[/dim]", value=o.value, checked=True
        )
        for o in available
    ]
    selected_values: list[str] = questionary.checkbox(
        "Select updates to apply:", choices=choices
    ).ask()

    if not selected_values:
        console.print("[yellow]No updates selected.[/yellow]")
        return

    selected = [o for o in available if o.value in selected_values]

    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column(style="bold")
    table.add_column(style="dim")

    for opt in selected:
        try:
            opt.apply(target)
            table.add_row("[green]✓[/green]", opt.label)
        except Exception as exc:
            table.add_row("[red]✗[/red]", f"{opt.label} — {exc}")

    console.print()
    console.print(table)
    console.print()
