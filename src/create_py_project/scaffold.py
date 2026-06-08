import shutil
import subprocess
import sys
from pathlib import Path

import questionary
from cookiecutter.main import cookiecutter  # type: ignore[import-untyped]
from rich.console import Console

from create_py_project.types import ProjectConfig

console = Console()


def _template_dir() -> str:
    root = Path(__file__).parent.parent.parent
    if not (root / "cookiecutter.json").exists():
        console.print(
            "[red]Template not found. This CLI must be installed in editable mode "
            "(uv tool install --editable .) from the repository root.[/red]"
        )
        raise SystemExit(1)
    return str(root)


def scaffold(dest_dir: str, config: ProjectConfig) -> None:
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
    template_dir = _template_dir()

    console.print(f"\n[bold]Scaffolding [cyan]{config.project_name}[/cyan]...[/bold]")

    cookiecutter(
        template_dir,
        no_input=True,
        extra_context=config.to_cookiecutter_dict(),
        output_dir=str(dest.parent),
    )

    project_dir = dest.parent / config.project_name

    # Git
    console.print("[dim]Initializing git...[/dim]")
    try:
        _run(["git", "init"], cwd=project_dir)
        _run(["git", "add", "-A"], cwd=project_dir)
        _run(
            ["git", "commit", "-m", "chore: initial scaffold from create-py-project"],
            cwd=project_dir,
        )
    except _CommandError as exc:
        console.print(f"[red]{exc}[/red]")
        console.print(f"[yellow]Cleaning up {project_dir}[/yellow]")
        shutil.rmtree(project_dir, ignore_errors=True)
        sys.exit(1)

    # GitHub
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


def run_new(project_name: str | None) -> None:
    from create_py_project.prompts import run_prompts

    config = run_prompts(project_name)
    dest_dir = str(Path.cwd() / config.project_name)
    scaffold(dest_dir, config)


class _CommandError(Exception):
    pass


def _run(cmd: list[str], cwd: Path) -> None:
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        raise _CommandError(f"Command failed: {' '.join(cmd)}\n{result.stderr}")
