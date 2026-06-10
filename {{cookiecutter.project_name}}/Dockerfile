# Install uv
FROM python:{{cookiecutter.python_version}}-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Change the working directory to the `app` directory
WORKDIR /app

# Copy the lockfile and `pyproject.toml` into the image
COPY uv.lock /app/uv.lock
COPY pyproject.toml /app/pyproject.toml

# Install dependencies
RUN uv sync --frozen --no-install-project

# Copy the project into the image (see .dockerignore for excluded paths)
COPY . /app

# Sync the project
RUN uv sync --frozen

# Run as a non-root user instead of root
RUN useradd --create-home --uid 1000 appuser && chown -R appuser /app
USER appuser

CMD [ "python", "src/{{cookiecutter.project_slug}}/foo.py"]
