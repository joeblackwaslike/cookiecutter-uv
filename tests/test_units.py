"""Unit tests for the CLI's pure logic (validation, slug, deps, templating)."""

import subprocess
from pathlib import Path

import pytest
from pydantic import ValidationError

from spinup_py import prompts as prompts_mod
from spinup_py import scaffold as scaffold_mod
from spinup_py.prompts import build_default_config, load_user_defaults, save_user_defaults
from spinup_py.scaffold import _CommandError, scaffold
from spinup_py.types import ProjectConfig, UserDefaults
from spinup_py.update import _has_dev_dependency, _render_template


def _config(**overrides: object) -> ProjectConfig:
    base: dict[str, object] = {
        "project_name": "my-project",
        "description": "d",
        "author": "a",
        "email": "e@example.com",
        "github_handle": "gh",
    }
    base.update(overrides)
    return ProjectConfig.create(**base)  # type: ignore[arg-type]


# ── ProjectConfig validation / slug / immutability ──────────────────────────


@pytest.mark.parametrize("name", ["my-project", "a", "a1", "my-proj-2", "abc123"])
def test_project_name_valid(name: str) -> None:
    assert _config(project_name=name).project_name == name


@pytest.mark.parametrize("name", ["My-Project", "my_project", "-leading", "trailing-", "", "has space", "../escape"])
def test_project_name_invalid(name: str) -> None:
    with pytest.raises(ValidationError):
        _config(project_name=name)


def test_slug_derived_from_name() -> None:
    assert _config(project_name="my-cool-project").project_slug == "my_cool_project"


def test_slug_explicit_preserved() -> None:
    # Constructed directly (create() derives the slug); the before-validator must
    # leave a caller-supplied slug untouched.
    cfg = ProjectConfig(
        project_name="my-project",
        project_slug="custom_slug",
        description="d",
        author="a",
        email="e@example.com",
        github_handle="gh",
    )
    assert cfg.project_slug == "custom_slug"


def test_build_default_config_uses_defaults() -> None:
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


def test_config_is_frozen() -> None:
    cfg = _config()
    with pytest.raises(ValidationError):
        cfg.project_slug = "mutated"  # type: ignore[misc]


def test_user_defaults_rejects_unknown_python_version() -> None:
    with pytest.raises(ValidationError):
        UserDefaults(python_version="3.8")  # type: ignore[arg-type]


# ── _has_dev_dependency ─────────────────────────────────────────────────────


def _write(tmp_path: Path, body: str) -> Path:
    p = tmp_path / "pyproject.toml"
    p.write_text(body)
    return p


def test_has_dev_dependency_present(tmp_path: Path) -> None:
    p = _write(tmp_path, '[dependency-groups]\ndev = ["deptry~=0.23.1", "ruff"]\n')
    assert _has_dev_dependency(p, "deptry") is True
    assert _has_dev_dependency(p, "ruff") is True


def test_has_dev_dependency_absent(tmp_path: Path) -> None:
    p = _write(tmp_path, '[dependency-groups]\ndev = ["ruff"]\n')
    assert _has_dev_dependency(p, "deptry") is False


def test_has_dev_dependency_ignores_comment(tmp_path: Path) -> None:
    p = _write(tmp_path, '[dependency-groups]\ndev = ["ruff"]  # deptry not needed\n')
    assert _has_dev_dependency(p, "deptry") is False


def test_has_dev_dependency_no_group(tmp_path: Path) -> None:
    p = _write(tmp_path, '[project]\nname = "x"\n')
    assert _has_dev_dependency(p, "deptry") is False


# ── _render_template ────────────────────────────────────────────────────────


def test_render_substitutes_name_and_slug() -> None:
    out = _render_template("{{cookiecutter.project_name}}/{{cookiecutter.project_slug}}", "my-proj")
    assert out == "my-proj/my_proj"


def test_render_strips_unresolved_tokens() -> None:
    out = _render_template("name={{cookiecutter.project_name}} extra={{cookiecutter.author}}", "p")
    assert out == "name=p extra="


# ── RC file load/save with legacy back-compat ───────────────────────────────


def test_load_user_defaults_reads_legacy_when_new_absent(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    new_rc = tmp_path / ".spinup-pyrc.toml"
    legacy_rc = tmp_path / ".create-py-projectrc.toml"
    legacy_rc.write_text(
        '[defaults]\nauthor = "Legacy Author"\nemail = "legacy@example.com"\n'
        'github_handle = "legacygh"\npython_version = "3.11"\n'
    )
    monkeypatch.setattr(prompts_mod, "RC_PATH", new_rc)
    monkeypatch.setattr(prompts_mod, "LEGACY_RC_PATH", legacy_rc)

    defaults = load_user_defaults()
    assert defaults.author == "Legacy Author"
    assert defaults.email == "legacy@example.com"
    assert defaults.github_handle == "legacygh"
    assert defaults.python_version == "3.11"


def test_load_user_defaults_prefers_new_over_legacy(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    new_rc = tmp_path / ".spinup-pyrc.toml"
    legacy_rc = tmp_path / ".create-py-projectrc.toml"
    new_rc.write_text('[defaults]\nauthor = "New Author"\n')
    legacy_rc.write_text('[defaults]\nauthor = "Legacy Author"\n')
    monkeypatch.setattr(prompts_mod, "RC_PATH", new_rc)
    monkeypatch.setattr(prompts_mod, "LEGACY_RC_PATH", legacy_rc)

    assert load_user_defaults().author == "New Author"


def test_save_user_defaults_writes_new_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    new_rc = tmp_path / ".spinup-pyrc.toml"
    legacy_rc = tmp_path / ".create-py-projectrc.toml"
    # Legacy file has both a defaults table and an unrelated section to preserve.
    legacy_rc.write_text('[defaults]\nauthor = "Legacy Author"\n\n[other]\nkeep = "me"\n')
    monkeypatch.setattr(prompts_mod, "RC_PATH", new_rc)
    monkeypatch.setattr(prompts_mod, "LEGACY_RC_PATH", legacy_rc)

    save_user_defaults(
        UserDefaults(
            author="Saved Author",
            email="saved@example.com",
            github_handle="savedgh",
            python_version="3.12",
        )
    )

    assert new_rc.exists()
    content = new_rc.read_text()
    assert "Saved Author" in content
    # Non-defaults content from the legacy file is migrated/preserved.
    assert "keep" in content


def test_load_user_defaults_invalid_data_falls_back(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    # Valid TOML but invalid values raise pydantic ValidationError (which is NOT a
    # ValueError); load_user_defaults must catch it and fall back to defaults.
    new_rc = tmp_path / ".spinup-pyrc.toml"
    new_rc.write_text('[defaults]\npython_version = "2.7"\n')
    monkeypatch.setattr(prompts_mod, "RC_PATH", new_rc)
    monkeypatch.setattr(prompts_mod, "LEGACY_RC_PATH", tmp_path / "absent.toml")

    assert load_user_defaults() == UserDefaults()


# ── _template_ref() resolution ──────────────────────────────────────────────


def test_template_ref_uses_env_override(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SPINUP_PY_TEMPLATE", "gh:foo/bar")
    assert scaffold_mod._template_ref() == "gh:foo/bar"


def test_template_ref_uses_local_when_present(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("SPINUP_PY_TEMPLATE", raising=False)
    # Point root (Path(__file__).parent.parent.parent) at tmp_path containing cookiecutter.json.
    (tmp_path / "cookiecutter.json").write_text("{}")
    monkeypatch.setattr(scaffold_mod, "__file__", str(tmp_path / "src" / "spinup_py" / "scaffold.py"))
    assert scaffold_mod._template_ref() == str(tmp_path)


def test_template_ref_falls_back_to_remote(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("SPINUP_PY_TEMPLATE", raising=False)
    # Point root at tmp_path with NO cookiecutter.json.
    monkeypatch.setattr(scaffold_mod, "__file__", str(tmp_path / "src" / "spinup_py" / "scaffold.py"))
    assert scaffold_mod._template_ref() == scaffold_mod.REMOTE_TEMPLATE
    assert scaffold_mod.REMOTE_TEMPLATE == "gh:joeblackwaslike/spinup-py"


def test_scaffold_remote_fetch_failure_is_friendly(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    from cookiecutter.exceptions import RepositoryNotFound

    cfg = _config(project_name="x")

    def boom(*_a: object, **_k: object) -> object:
        raise RepositoryNotFound("gh:foo/bar could not be found")

    monkeypatch.setattr(scaffold_mod, "cookiecutter", boom)
    monkeypatch.setattr(scaffold_mod, "_template_ref", lambda: "gh:foo/bar")
    with pytest.raises(SystemExit) as exc:
        scaffold_mod.scaffold(str(tmp_path / "x"), cfg, non_interactive=True)
    assert exc.value.code == 1
    captured = capsys.readouterr()
    assert "SPINUP_PY_TEMPLATE" in (captured.out + captured.err)


# ── scaffold() git-failure cleanup ──────────────────────────────────────────


def test_scaffold_cleans_up_on_git_failure(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    cfg = _config(project_name="my-project")
    project_dir = tmp_path / "my-project"

    # Stub cookiecutter so it just creates the project directory (no real render).
    def fake_cookiecutter(*_args: object, **_kwargs: object) -> str:
        project_dir.mkdir(parents=True)
        (project_dir / "marker.txt").write_text("x")
        return str(project_dir)

    monkeypatch.setattr(scaffold_mod, "cookiecutter", fake_cookiecutter)
    monkeypatch.setattr(scaffold_mod, "_template_ref", lambda: str(tmp_path))

    # Make the first git command fail.
    def fake_run(cmd: list[str], cwd: Path) -> None:
        raise _CommandError("boom")

    monkeypatch.setattr(scaffold_mod, "_run", fake_run)

    with pytest.raises(SystemExit) as exc:
        scaffold(str(project_dir), cfg)
    assert exc.value.code == 1
    assert not project_dir.exists()  # partial project was cleaned up


def test_scaffold_cleans_up_when_git_missing(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    # git not installed -> subprocess raises FileNotFoundError (an OSError); scaffold
    # must still clean up the partial project and exit cleanly rather than crash.
    cfg = _config(project_name="my-project")
    project_dir = tmp_path / "my-project"

    def fake_cookiecutter(*_args: object, **_kwargs: object) -> str:
        project_dir.mkdir(parents=True)
        return str(project_dir)

    monkeypatch.setattr(scaffold_mod, "cookiecutter", fake_cookiecutter)
    monkeypatch.setattr(scaffold_mod, "_template_ref", lambda: str(tmp_path))

    def fake_run(cmd: list[str], cwd: Path) -> None:
        raise FileNotFoundError("git not found")

    monkeypatch.setattr(scaffold_mod, "_run", fake_run)

    with pytest.raises(SystemExit) as exc:
        scaffold(str(project_dir), cfg)
    assert exc.value.code == 1
    assert not project_dir.exists()  # cleaned up despite git being absent


def test_scaffold_rejects_mismatched_dest_basename(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    cfg = _config(project_name="my-project")
    monkeypatch.setattr(scaffold_mod, "_template_ref", lambda: str(tmp_path))
    with pytest.raises(SystemExit) as exc:
        scaffold(str(tmp_path / "different-name"), cfg)
    assert exc.value.code == 1


def test_scaffold_non_interactive_skips_push_prompt(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    cfg = _config(project_name="ni-proj")
    project_dir = tmp_path / "ni-proj"

    def fake_cookiecutter(*_args: object, **_kwargs: object) -> str:
        project_dir.mkdir(parents=True)
        return str(project_dir)

    monkeypatch.setattr(scaffold_mod, "cookiecutter", fake_cookiecutter)
    monkeypatch.setattr(scaffold_mod, "_template_ref", lambda: str(tmp_path))
    monkeypatch.setattr(scaffold_mod, "_run", lambda cmd, cwd: None)  # git no-ops

    # Stub out subprocess (gh/bd) so non-interactive scaffold stays hermetic.
    def fake_subprocess_run(*_args: object, **_kwargs: object) -> subprocess.CompletedProcess[str]:
        cmd = _args[0] if _args else _kwargs.get("args", [])
        if isinstance(cmd, list) and cmd and cmd[0] == "serena":
            return subprocess.CompletedProcess(args=cmd, returncode=1, stdout="", stderr="")
        return subprocess.CompletedProcess(args=["x"], returncode=0, stdout="", stderr="")

    monkeypatch.setattr(scaffold_mod.subprocess, "run", fake_subprocess_run)

    # If a questionary prompt is reached, fail loudly:
    def boom(*_args: object, **_kwargs: object) -> object:
        raise AssertionError("prompt should not be called in non-interactive mode")

    monkeypatch.setattr(scaffold_mod.questionary, "select", boom)

    scaffold(str(project_dir), cfg, non_interactive=True)
    assert (project_dir / ".serena" / "project.yml").exists()


def test_cli_non_interactive_flag_routes(monkeypatch: pytest.MonkeyPatch) -> None:
    from typer.testing import CliRunner

    from spinup_py.cli import app

    called: dict[str, object] = {}
    monkeypatch.setattr(
        scaffold_mod,
        "run_new",
        lambda name, non_interactive=False: called.update(name=name, ni=non_interactive),
    )
    result = CliRunner().invoke(app, ["my-proj", "--non-interactive"])
    assert result.exit_code == 0
    assert called == {"name": "my-proj", "ni": True}


def test_scaffold_run_raises_on_nonzero(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    # _run should raise _CommandError when the subprocess exits non-zero.
    def fake_subprocess_run(*_args: object, **_kwargs: object) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(args=["x"], returncode=1, stdout="", stderr="nope")

    monkeypatch.setattr(scaffold_mod.subprocess, "run", fake_subprocess_run)
    with pytest.raises(_CommandError):
        scaffold_mod._run(["git", "status"], cwd=tmp_path)
