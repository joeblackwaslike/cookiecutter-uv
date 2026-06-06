from __future__ import annotations

import sys
from pathlib import Path

import questionary
import tomlkit
from rich.console import Console
from rich.table import Table

from create_py_project.types import ProjectConfig, UserDefaults

RC_PATH = Path.home() / ".create-py-projectrc.toml"
console = Console()


def load_user_defaults() -> UserDefaults:
    if RC_PATH.exists():
        try:
            data = tomlkit.parse(RC_PATH.read_text()).get("defaults", {})
            return UserDefaults(**data)
        except (OSError, tomlkit.exceptions.TOMLKitError, ValueError):
            console.print(f"[yellow]Warning: could not parse {RC_PATH}, using defaults[/yellow]")
    return UserDefaults()


def save_user_defaults(d: UserDefaults) -> None:
    if RC_PATH.exists():
        try:
            doc = tomlkit.parse(RC_PATH.read_text())
        except Exception:
            doc = tomlkit.document()
    else:
        doc = tomlkit.document()
    tbl = tomlkit.table()
    tbl["author"] = d.author
    tbl["email"] = d.email
    tbl["github_handle"] = d.github_handle
    tbl["python_version"] = d.python_version
    doc["defaults"] = tbl
    try:
        RC_PATH.write_text(tomlkit.dumps(doc))
    except OSError:
        console.print(f"[yellow]Warning: could not save defaults to {RC_PATH}[/yellow]")


def run_prompts(project_name_arg: str | None = None) -> ProjectConfig:
    console.rule("[bold blue]create-py-project[/bold blue]")
    defaults = load_user_defaults()

    if project_name_arg:
        project_name = project_name_arg
    else:
        project_name = questionary.text(
            "Project name (kebab-case):",
            validate=lambda v: bool(v) and all(c.islower() or c.isdigit() or c == "-" for c in v)
            or "Use lowercase letters, digits, and hyphens only",
        ).ask()
        if project_name is None:
            console.print("[yellow]Aborted.[/yellow]")
            sys.exit(0)

    description = questionary.text("Short description:").ask()
    if description is None:
        console.print("[yellow]Aborted.[/yellow]")
        sys.exit(0)

    author = questionary.text("Author name:", default=defaults.author).ask()
    if author is None:
        console.print("[yellow]Aborted.[/yellow]")
        sys.exit(0)
    author = author or defaults.author
    email = questionary.text("Email:", default=defaults.email).ask()
    if email is None:
        console.print("[yellow]Aborted.[/yellow]")
        sys.exit(0)
    email = email or defaults.email
    github_handle = questionary.text("GitHub handle:", default=defaults.github_handle).ask()
    if github_handle is None:
        console.print("[yellow]Aborted.[/yellow]")
        sys.exit(0)
    github_handle = github_handle or defaults.github_handle
    python_version = questionary.select(
        "Python version:",
        choices=["3.12", "3.11", "3.10", "3.9"],
        default=defaults.python_version if defaults.python_version in ["3.12", "3.11", "3.10", "3.9"] else "3.12",
    ).ask()
    if python_version is None:
        console.print("[yellow]Aborted.[/yellow]")
        sys.exit(0)

    features: list[str] | None = questionary.checkbox(
        "Features to include:",
        choices=[
            questionary.Choice("GitHub Actions CI", value="github_actions", checked=True),
            questionary.Choice("Devcontainer", value="devcontainer", checked=True),
            questionary.Choice("Docusaurus docs site", value="include_docs"),
            questionary.Choice("Codecov coverage", value="codecov"),
            questionary.Choice("Dockerfile", value="dockerfile"),
            questionary.Choice("deptry (dependency audit)", value="deptry", checked=True),
            questionary.Choice("Publish to PyPI", value="publish_to_pypi"),
        ],
    ).ask()
    if features is None:
        console.print("[yellow]Aborted.[/yellow]")
        sys.exit(0)

    license_choice = questionary.select(
        "License:",
        choices=[
            "MIT license",
            "BSD license",
            "ISC license",
            "Apache Software License 2.0",
            "GNU General Public License v3",
            "Not open source",
        ],
        default="MIT license",
    ).ask()
    if license_choice is None:
        console.print("[yellow]Aborted.[/yellow]")
        sys.exit(0)

    config = ProjectConfig.create(
        project_name=project_name,
        description=description,
        author=author,
        email=email,
        github_handle=github_handle,
        python_version=python_version,
        include_github_actions="github_actions" in features,
        devcontainer="devcontainer" in features,
        include_docs="include_docs" in features,
        codecov="codecov" in features,
        dockerfile="dockerfile" in features,
        deptry="deptry" in features,
        publish_to_pypi="publish_to_pypi" in features,
        open_source_license=license_choice,
    )

    table = Table(title="Project Configuration", show_header=False, box=None, padding=(0, 2))
    table.add_column("Key", style="cyan")
    table.add_column("Value", style="white")
    for k, v in config.to_cookiecutter_dict().items():
        table.add_row(k, str(v))
    console.print()
    console.print(table)
    console.print()

    confirm = questionary.confirm("Create project?", default=True).ask()
    if confirm is None or not confirm:
        console.print("[yellow]Aborted.[/yellow]")
        sys.exit(0)

    save_user_defaults(
        UserDefaults(
            author=author,
            email=email,
            github_handle=github_handle,
            python_version=python_version,
        )
    )
    return config
