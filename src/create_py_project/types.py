import re
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, field_validator, model_validator

PythonVersion = Literal["3.12", "3.11", "3.10"]


class UserDefaults(BaseModel):
    author: str = ""
    email: str = ""
    github_handle: str = ""
    python_version: PythonVersion = "3.12"


class ProjectConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    project_name: str
    project_slug: str = ""
    description: str
    author: str
    email: str
    github_handle: str
    python_version: PythonVersion = "3.12"
    include_github_actions: bool = True
    publish_to_pypi: bool = False
    deptry: bool = True
    include_docs: bool = False
    codecov: bool = False
    dockerfile: bool = False
    devcontainer: bool = True
    open_source_license: Literal[
        "MIT license",
        "BSD license",
        "ISC license",
        "Apache Software License 2.0",
        "GNU General Public License v3",
        "Not open source",
    ] = "MIT license"

    @field_validator("project_name")
    @classmethod
    def _validate_project_name(cls, v: str) -> str:
        if not re.match(r"^[a-z0-9]([a-z0-9-]*[a-z0-9])?$", v):
            msg = "project_name must be kebab-case (lowercase letters, digits, hyphens; no leading/trailing hyphens)"
            raise ValueError(msg)
        return v

    @model_validator(mode="before")
    @classmethod
    def _derive_slug(cls, data: Any) -> Any:
        # Derive before construction so the slug stays consistent with
        # project_name even though the model is frozen (no post-init mutation).
        if isinstance(data, dict) and not data.get("project_slug"):
            name = str(data.get("project_name", ""))
            data["project_slug"] = name.lower().replace("-", "_")
        return data

    @classmethod
    def create(
        cls,
        *,
        project_name: str,
        description: str,
        author: str,
        email: str,
        github_handle: str,
        python_version: PythonVersion = "3.12",
        include_github_actions: bool = True,
        publish_to_pypi: bool = False,
        deptry: bool = True,
        include_docs: bool = False,
        codecov: bool = False,
        dockerfile: bool = False,
        devcontainer: bool = True,
        open_source_license: str = "MIT license",
    ) -> "ProjectConfig":
        return cls(
            project_name=project_name,
            description=description,
            author=author,
            email=email,
            github_handle=github_handle,
            python_version=python_version,
            include_github_actions=include_github_actions,
            publish_to_pypi=publish_to_pypi,
            deptry=deptry,
            include_docs=include_docs,
            codecov=codecov,
            dockerfile=dockerfile,
            devcontainer=devcontainer,
            open_source_license=open_source_license,  # type: ignore[arg-type]
        )

    def to_cookiecutter_dict(self) -> dict[str, str]:
        def yn(v: bool) -> str:
            return "y" if v else "n"

        return {
            "author": self.author,
            "email": self.email,
            "github_handle": self.github_handle,
            "project_name": self.project_name,
            "project_slug": self.project_slug,
            "description": self.description,
            "python_version": self.python_version,
            "include_github_actions": yn(self.include_github_actions),
            "publish_to_pypi": yn(self.publish_to_pypi),
            "deptry": yn(self.deptry),
            "include_docs": yn(self.include_docs),
            "codecov": yn(self.codecov),
            "dockerfile": yn(self.dockerfile),
            "devcontainer": yn(self.devcontainer),
            "open_source_license": self.open_source_license,
        }
