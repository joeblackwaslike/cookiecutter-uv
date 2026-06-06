from __future__ import annotations

import typer

app = typer.Typer(
    name="create-py-project",
    help="Scaffold and maintain production-ready Python projects.",
    no_args_is_help=False,
    add_completion=False,
)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    project_name: str | None = typer.Argument(None, help="Name of the new project"),
    update: str | None = typer.Option(
        None,
        "--update",
        "-u",
        metavar="DIR",
        help="Retrofit an existing project at DIR (default: current directory)",
    ),
    version: bool = typer.Option(False, "--version", "-v", help="Show version and exit"),
) -> None:
    if ctx.invoked_subcommand is not None:
        return

    if version:
        try:
            from importlib.metadata import PackageNotFoundError
            from importlib.metadata import version as pkg_version

            typer.echo(pkg_version("create-py-project"))
        except PackageNotFoundError:
            typer.echo("0.1.0")
        raise typer.Exit()

    if update is not None:
        from create_py_project.update import update_project

        update_project(update or ".")
    elif project_name is not None:
        from create_py_project.scaffold import run_new

        run_new(project_name)
    else:
        typer.echo(ctx.get_help())


@app.command("new")
def new_cmd(
    project_name: str | None = typer.Argument(None, help="Project name (kebab-case)"),
) -> None:
    """Scaffold a new Python project through guided prompts."""
    from create_py_project.scaffold import run_new

    run_new(project_name)


@app.command("update")
def update_cmd(
    target_dir: str = typer.Argument(".", help="Path to the project to retrofit"),
) -> None:
    """Retrofit an existing Python project with create-py-project tooling."""
    from create_py_project.update import update_project

    update_project(target_dir)
