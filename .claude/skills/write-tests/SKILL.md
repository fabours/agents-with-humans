---
name: write-tests
description: Writes pytest tests for FastAPI routes. Use this after implementing any backend route.
---

# Skill: write-tests

Use this skill after implementing any FastAPI route to write tests before opening a PR.

## Setup Check

Verify `pytest` and `httpx` are in `requirements.txt`. If not, add them.

```
pytest>=8.0
httpx>=0.27
```

## File Location

Tests live in `backend/tests/`. One test file per router:
```
backend/
└── tests/
    ├── __init__.py
    ├── conftest.py        ← shared fixtures
    └── test_weather.py    ← one file per router
```

## Conftest Pattern

If `conftest.py` doesn't exist, create it:

```python
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as c:
        yield c
```

## Test Pattern

For each route, write at minimum:
1. **Happy path** — valid input, expected response shape
2. **Error case** — upstream failure or invalid input

```python
import pytest

@pytest.mark.asyncio
async def test_get_current_weather_success(client):
    response = await client.get("/api/weather/current?city=Montreal")
    assert response.status_code == 200
    data = response.json()
    assert "temperature" in data
    assert "windspeed" in data

@pytest.mark.asyncio
async def test_get_current_weather_invalid_city(client):
    response = await client.get("/api/weather/current?city=")
    assert response.status_code == 422  # or 400 depending on validation
```

## Run Tests Locally Before Committing

```bash
cd backend
pytest tests/ -v
```

All tests must pass before using the `open-pr` skill.
