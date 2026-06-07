import re
from typing import Literal

from pydantic import BaseModel, field_validator, model_validator


class UserDefaults(BaseModel):
    author: str = ""
    email: str = ""
    github_handle: str = ""
    python_version: str = "3.12"


class ProjectConfig(BaseModel):
    project_name: str
    project_slug: str = ""
    description: str
    author: str
    email: str
    github_handle: str
    python_version: Literal["3.12", "3.11", "3.10"] = "3.12"
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

    @model_validator(mode="after")
    def _derive_slug(self) -> "ProjectConfig":
        if not self.project_slug:
            self.project_slug = self.project_name.lower().replace("-", "_")
        return self

    @classmethod
    def create(cls, *, project_name: str, **kwargs: object) -> "ProjectConfig":
        return cls(project_name=project_name, **kwargs)  # type: ignore[arg-type]

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
