# Study database status

```text
SCHEMA_STATUS: NOT_FOUND
MIGRATION_DIRECTORY_STATUS: NOT_FOUND
RUNTIME_DB_HELPER: VERIFIED
```

Current evidence establishes PostgreSQL configuration and sync SQLAlchemy helpers only. It does **not** establish any business table.

Known discrepancy:
- runtime core uses `postgresql+psycopg` and configurable `search_path`;
- `alembic.ini` references migration setup/directory that is absent and is not sufficient schema evidence.

`/api/v1/test/db` only declares `SELECT NOW()`; health readiness only reports configuration label and does not probe the DB.

Before any migration/query task, require authoritative table/column/PK/FK/unique/index/status/delete/timestamp/tenant rules. Query helpers do not commit; transaction ownership belongs to the future/current business use case that performs the write.
