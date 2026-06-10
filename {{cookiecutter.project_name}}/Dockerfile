# Install uv
FROM python:{{cookiecutter.python_version}}-slim
COPY --from=ghcr.io/astral-sh/uv:0.11.19 /uv /bin/uv

# Create a non-root user and give it ownership of /app up front, so we never need
# a costly recursive chown of the populated virtualenv in a later layer.
RUN useradd --create-home --uid 1000 appuser
WORKDIR /app
RUN chown appuser:appuser /app
USER appuser

# Copy the lockfile and `pyproject.toml` into the image
COPY --chown=appuser:appuser uv.lock pyproject.toml /app/

# Install dependencies
RUN uv sync --frozen --no-install-project

# Copy the project into the image
# (.dockerignore restricts the build context sent to the Docker daemon)
COPY --chown=appuser:appuser . /app

# Sync the project
RUN uv sync --frozen

# Use `uv run` so the uv-managed virtualenv (not the base image's system Python) is used
CMD [ "uv", "run", "python", "src/{{cookiecutter.project_slug}}/foo.py"]
