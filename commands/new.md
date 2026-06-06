# /new

**Description:** Scaffold a new Python project through guided conversation.

**Argument hint:** `[project-name]`

**Allowed tools:** Bash, Read, Write

---

## Instructions

You are helping the user scaffold a new production-ready Python project using `create-py-project`.

### Step 1 — Load user defaults

Check if `~/.create-py-projectrc.toml` exists and read it:

```bash
cat ~/.create-py-projectrc.toml 2>/dev/null || echo "(no RC file yet)"
```

Use any stored `author`, `email`, `github_handle`, `python_version` as defaults for the prompts below.

### Step 2 — Collect configuration

Ask the user for each of the following. If a default is available from the RC file, show it and ask them to confirm or change. Gather all values before proceeding (batch the non-obvious ones).

| Field                    | Type                                                                                                                       | Default               |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------- | --------------------- |
| `project_name`           | string (kebab-case)                                                                                                        | from argument, or ask |
| `description`            | string                                                                                                                     | —                     |
| `author`                 | string                                                                                                                     | RC default            |
| `email`                  | email                                                                                                                      | RC default            |
| `github_handle`          | string                                                                                                                     | RC default            |
| `python_version`         | one of: 3.12, 3.11, 3.10, 3.9                                                                                              | 3.12                  |
| `include_github_actions` | bool                                                                                                                       | true                  |
| `devcontainer`           | bool                                                                                                                       | true                  |
| `include_docs`           | bool (Docusaurus)                                                                                                          | false                 |
| `codecov`                | bool                                                                                                                       | false                 |
| `dockerfile`             | bool                                                                                                                       | false                 |
| `deptry`                 | bool                                                                                                                       | true                  |
| `publish_to_pypi`        | bool                                                                                                                       | false                 |
| `open_source_license`    | one of: MIT license, BSD license, ISC license, Apache Software License 2.0, GNU General Public License v3, Not open source | MIT license           |

Show a summary table of the collected config and confirm with the user before proceeding.

### Step 3 — Scaffold the project

Find the plugin root and determine the destination directory. Then write and run a temp scaffold script:

```bash
# Find where create-py-project is installed
PLUGIN_ROOT="$(python3 -c "import create_py_project, pathlib; print(pathlib.Path(create_py_project.__file__).parent.parent.parent)")"

# Write temp script
cat > /tmp/cpp-scaffold.py << 'PYEOF'
import sys
sys.path.insert(0, "PLUGIN_SRC_PATH")
from create_py_project.scaffold import scaffold
from create_py_project.types import ProjectConfig

config = ProjectConfig.create(
    project_name="PROJECT_NAME",
    description="DESCRIPTION",
    author="AUTHOR",
    email="EMAIL",
    github_handle="GITHUB_HANDLE",
    python_version="PYTHON_VERSION",
    include_github_actions=INCLUDE_GITHUB_ACTIONS,
    devcontainer=DEVCONTAINER,
    include_docs=INCLUDE_DOCS,
    codecov=CODECOV,
    dockerfile=DOCKERFILE,
    deptry=DEPTRY,
    publish_to_pypi=PUBLISH_TO_PYPI,
    open_source_license="OPEN_SOURCE_LICENSE",
)
import os, pathlib
dest = pathlib.Path(os.getcwd()) / config.project_name
# Skip interactive git push prompt — handled separately below
scaffold.__module__  # ensure import works

from cookiecutter.main import cookiecutter
cookiecutter(
    str(pathlib.Path(sys.path[0]).parent),
    no_input=True,
    extra_context=config.to_cookiecutter_dict(),
    output_dir=str(pathlib.Path(os.getcwd())),
)
print(f"Scaffolded: {dest}")
PYEOF

python3 /tmp/cpp-scaffold.py
```

Replace each `PLACEHOLDER` with the collected values before running. Use `True`/`False` for boolean fields.

### Step 4 — Post-scaffold setup

After scaffolding, run from the newly created project directory:

```bash
cd PROJECT_NAME
git init && git add -A && git commit -m "chore: initial scaffold from create-py-project"
```

Ask the user: "Push to GitHub? (public / private / skip)"

If public or private:

```bash
gh repo create GITHUB_HANDLE/PROJECT_NAME --VISIBILITY --source=. --remote=origin --push
```

Run Beads and Serena init (errors are non-fatal):

```bash
bd init --skip-agents --non-interactive 2>/dev/null || true
mkdir -p .serena && echo "project_name: PROJECT_NAME\nlanguage: python" > .serena/project.yml
```

### Step 5 — Summary

Report:

- Full path to the created project
- GitHub URL (if pushed)
- Next steps: `cd PROJECT_NAME && uv sync && uv run pre-commit install`
