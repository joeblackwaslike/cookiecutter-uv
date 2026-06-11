---
title: Testing
---

# Testing

## Test Structure

```
tests/
├── __init__.py
├── test_core.py
└── conftest.py
```

## Running Tests

```bash
just test                          # all tests
uv run pytest --cov                # with coverage report
uv run pytest -k "test_specific"   # single test
uv run pytest --watch              # watch mode (requires pytest-watch)
```

## Writing Tests

```python
import pytest
from {{cookiecutter.project_slug}} import your_function


def test_should_do_x_when_given_y():
    result = your_function(input_value)
    assert result == expected


@pytest.fixture
def sample_data():
    return {"key": "value"}
```

## Testing Philosophy

Replace with your project's specific testing approach and conventions.
