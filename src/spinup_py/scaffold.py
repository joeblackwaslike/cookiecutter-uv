import os
import shutil
import subprocess
import sys
from pathlib import Path

import questionary
from cookiecutter.exceptions import (  # type: ignore[import-untyped]
    RepositoryCloneFailed,
    RepositoryNotFound,
)
from cookiecutter.main import cookiecutter  # type: ignore[import-untyped]
from rich.console import Console

from spinup_py.types import ProjectConfig

console = Console()

REMOTE_TEMPLATE = "gh:joeblackwaslike/spinup-py"


def _template_ref() -> str:
    """Resolve the cookiecutter template reference.

    1. An explicit override via the SPINUP_PY_TEMPLATE env var (used by CI smoke
       tests and power users) — a local path or any cookiecutter-accepted ref.
    2. The local repository root when running from a source checkout / editable
       install (cookiecutter.json present next to the installed package).
    3. Otherwise the published template on GitHub, which cookiecutter clones.
    """
    override = os.environ.get("SPINUP_PY_TEMPLATE")
    if override:
        return override
    root = Path(__file__).parent.parent.parent
    if (root / "cookiecutter.json").exists():
        return str(root)
    return REMOTE_TEMPLATE


def scaffold(dest_dir: str, config: ProjectConfig, non_interactive: bool = False) -> None:
    """Scaffold a new project from the template.

    The project is always created at ``<parent of dest_dir>/<config.project_name>``:
    only the *parent* of ``dest_dir`` is used as cookiecutter's output directory,
    and the final directory name comes from ``config.project_name``. Callers must
    therefore pass a ``dest_dir`` whose basename equals ``config.project_name``
    (``run_new`` does this); otherwise the basename would be silently ignored.
    """
    dest = Path(dest_dir).resolve()
    if dest.name != config.project_name:
        console.print(
            f"[red]dest_dir basename ({dest.name!r}) must match " f"project_name ({config.project_name!r}).[/red]"
        )
        raise SystemExit(1)
    template_ref = _template_ref()

    console.print(f"\n[bold]Scaffolding [cyan]{config.project_name}[/cyan]...[/bold]")

    try:
        cookiecutter(
            template_ref,
            no_input=True,
            extra_context=config.to_cookiecutter_dict(),
            output_dir=str(dest.parent),
        )
    except (RepositoryNotFound, RepositoryCloneFailed) as exc:
        console.print(f"[red]Could not fetch the project template ({template_ref}): {exc}[/red]")
        console.print(
            "[dim]If you are offline or the template repo is unavailable, point "
            "SPINUP_PY_TEMPLATE at a local cookiecutter template directory.[/dim]"
        )
        raise SystemExit(1) from exc

    project_dir = dest.parent / config.project_name

    # Git
    console.print("[dim]Initializing git...[/dim]")
    try:
        _run(["git", "init"], cwd=project_dir)
        _run(["git", "add", "-A"], cwd=project_dir)
        _run(
            ["git", "commit", "-m", "chore: initial scaffold from spinup-py"],
            cwd=project_dir,
        )
    except _CommandError as exc:
        console.print(f"[red]{exc}[/red]")
        console.print(f"[yellow]Cleaning up {project_dir}[/yellow]")
        shutil.rmtree(project_dir, ignore_errors=True)
        sys.exit(1)

    # GitHub
    if not non_interactive:
        push_choice = questionary.select("Push to GitHub?", choices=["public", "private", "skip"], default="skip").ask()
        if push_choice in ("public", "private"):
            console.print("[dim]Creating GitHub repo...[/dim]")
            try:
                subprocess.run(
                    [
                        "gh",
                        "repo",
                        "create",
                        f"{config.github_handle}/{config.project_name}",
                        f"--{push_choice}",
                        "--source=.",
                        "--remote=origin",
                        "--push",
                    ],
                    cwd=project_dir,
                    check=True,
                )
            except (subprocess.CalledProcessError, FileNotFoundError) as exc:
                console.print(f"[yellow]GitHub repo creation failed: {exc}[/yellow]")
                console.print("[dim]You can push manually later with: gh repo create[/dim]")

    # Beads
    try:
        result = subprocess.run(
            ["bd", "init", "--skip-agents", "--non-interactive"],
            cwd=project_dir,
            capture_output=True,
        )
        if result.returncode != 0:
            console.print("[dim yellow]bd init failed — skipping Beads init[/dim yellow]")
    except OSError:
        console.print("[dim yellow]bd not found or not executable — skipping Beads init[/dim yellow]")

    # Serena
    serena_dir = project_dir / ".serena"
    serena_dir.mkdir(exist_ok=True)
    (serena_dir / "project.yml").write_text(f"project_name: {config.project_name}\nlanguage: python\n")

    console.print(f"\n[bold green]✓ Project created at {project_dir}[/bold green]")
    console.print(f"[dim]Next: cd {config.project_name} && uv sync && uv run pre-commit install[/dim]")


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


class _CommandError(Exception):
    pass


def _run(cmd: list[str], cwd: Path) -> None:
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        raise _CommandError(f"Command failed: {' '.join(cmd)}\n{result.stderr}")
