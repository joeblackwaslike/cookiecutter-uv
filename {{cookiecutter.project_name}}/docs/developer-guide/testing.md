---
title: Testing
---

# Testing

## Test Structure

```
tests/
├── conftest.py        # shared fixtures
├── test_core.py       # unit tests
└── test_integration/  # integration tests
```

## Running Tests

```bash
uv run pytest                  # all tests
uv run pytest --cov            # with coverage report
uv run pytest -x --watch       # stop on first failure + watch mode
```

## Writing Tests

```python
import pytest
from {{cookiecutter.project_slug}} import your_function


class TestYourFunction:
    def test_should_do_x_when_given_y(self):
        result = your_function(input_value)
        assert result == expected

    def test_raises_on_invalid_input(self):
        with pytest.raises(ValueError):
            your_function(bad_input)
```

## Testing Philosophy

Replace with your project's specific testing approach and conventions.
