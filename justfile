# List available recipes
default:
    @just --list

# bake without inputs and overwrite if exists.
bake:
    @uv run cookiecutter --no-input . --overwrite-if-exists

# bake with inputs and overwrite if exists.
bake-with-inputs:
    @uv run cookiecutter . --overwrite-if-exists

# For quick publishing to cookiecutter-uv-example to test GH Actions
bake-and-test-deploy:
    @rm -rf cookiecutter-uv-example || true
    @uv run cookiecutter --no-input . --overwrite-if-exists \
        author="Joe Black" \
        email="me@joeblack.nyc" \
        github_author_handle=joeblackwaslike \
        project_name=cookiecutter-uv-example \
        project_slug=cookiecutter_uv_example
    @cd cookiecutter-uv-example; uv sync && \
        git init -b main && \
        git add . && \
        uv run pre-commit install && \
        uv run pre-commit run -a || true && \
        git add . && \
        uv run pre-commit run -a || true && \
        git add . && \
        git commit -m "init commit" && \
        git remote add origin git@github.com:joeblackwaslike/cookiecutter-uv-example.git && \
        git push -f origin main

# Install the virtual environment
install:
    @echo "🚀 Creating virtual environment"
    @uv sync

# Run code quality tools.
check:
    @echo "🚀 Checking lock file consistency with 'pyproject.toml'"
    @uv lock --locked
    @echo "🚀 Linting code: Running pre-commit"
    @uv run pre-commit run -a
    @echo "🚀 Static type checking: Running mypy"
    @uv run mypy
    @echo "🚀 Checking for obsolete dependencies: Running deptry"
    @uv run deptry "src"

# Test the code with pytest.
test:
    @echo "🚀 Testing code: Running pytest"
    @uv run python -m pytest --cov --cov-config=pyproject.toml --cov-report=xml tests

# Build wheel file
build: clean-build
    @echo "🚀 Creating wheel file"
    @uvx --from build pyproject-build --installer uv

# Clean build artifacts
clean-build:
    @echo "🚀 Removing build artifacts"
    @uv run python -c "import shutil; import os; shutil.rmtree('dist') if os.path.exists('dist') else None"

# Publish a release to PyPI.
publish:
    @echo "🚀 Publishing: Dry run."
    @uvx --from build pyproject-build --installer uv
    @echo "🚀 Publishing."
    @uvx twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

# Build and publish.
build-and-publish: build publish

# Test if documentation can be built without warnings or errors
docs-test:
    @uv run mkdocs build -s

# Build and serve the documentation
docs:
    @uv run mkdocs serve
