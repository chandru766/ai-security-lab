# Testing

## Implemented Tests
The project utilizes `pytest` for backend testing.

- **`test_api.py`**: Integration tests for general API endpoints, auth, and dashboard metrics.
- **`test_learning.py`**: Tests the quiz generation, completion, and scoring logic.

## How to Run Tests
```bash
# Activate virtual environment
.env\Scriptsctivate

# Run tests
pytest -q tests/test_learning.py tests/test_api.py
```\n