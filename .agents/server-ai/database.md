# AI database status

```text
RUNTIME_DB_USAGE: NONE
SCHEMA_STATUS: NOT_FOUND
MIGRATION_STATUS: NOT_FOUND
```

`app/core/database.py` contains copied sync SQLAlchemy helpers, but current `app/main.py -> chat` path never imports/uses them and the AI package does not declare SQLAlchemy/psycopg dependencies in `pyproject.toml`.

No source establishes chat log table, user table or AI persistence model. Do not add query/persistence behavior because `query.py` exists as an empty placeholder.
