import typer

app = typer.Typer(
    name="spinup-py",
    help="Scaffold and maintain production-ready Python projects.",
    no_args_is_help=False,
    add_completion=False,
)


@app.callback(
    invoke_without_command=True,
    # Allow options after the positional, e.g. `spinup-py my-proj --non-interactive`.
    context_settings={"allow_interspersed_args": True},
)
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
    non_interactive: bool = typer.Option(
        False, "--non-interactive", "-y", help="Scaffold with defaults, no prompts"
    ),
) -> None:
    if ctx.invoked_subcommand is not None:
        return

    if version:
        try:
            from importlib.metadata import PackageNotFoundError
            from importlib.metadata import version as pkg_version

            typer.echo(pkg_version("spinup-py"))
        except PackageNotFoundError:
            typer.echo("0.1.0")
        raise typer.Exit()

    if update is not None:
        from spinup_py.update import update_project

        update_project(update or ".")
    elif project_name is not None:
        from spinup_py.scaffold import run_new

        run_new(project_name, non_interactive=non_interactive)
    else:
        typer.echo(ctx.get_help())


@app.command("new")
def new_cmd(
    project_name: str | None = typer.Argument(None, help="Project name (kebab-case)"),
    non_interactive: bool = typer.Option(
        False, "--non-interactive", "-y", help="Scaffold with defaults, no prompts"
    ),
) -> None:
    """Scaffold a new Python project through guided prompts."""
    from spinup_py.scaffold import run_new

    run_new(project_name, non_interactive=non_interactive)


@app.command("update")
def update_cmd(
    target_dir: str = typer.Argument(".", help="Path to the project to retrofit"),
) -> None:
    """Retrofit an existing Python project with spinup-py tooling."""
    from spinup_py.update import update_project

    update_project(target_dir)
