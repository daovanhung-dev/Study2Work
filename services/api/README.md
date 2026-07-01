# Study2Work API

Canonical Study-scope backend foundation for Study2Work.

## Stack

- Python 3.12+
- FastAPI + Pydantic v2
- SQLAlchemy 2.0 async + Alembic
- PostgreSQL
- Redis
- Celery
- uv, Ruff, mypy, pytest

## Commands

```powershell
uv sync
uv run uvicorn app.main:app --reload
uv run ruff check .
uv run ruff format --check .
uv run mypy app
uv run pytest
```

From the repository root, the development runtime can also be started with:

```powershell
docker compose up --build
```

## Public Foundation Endpoint

- `GET /api/v1/health`

Business APIs are intentionally not implemented until each API has an approved API DD.
