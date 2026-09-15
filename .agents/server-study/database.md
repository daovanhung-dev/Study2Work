# Study database status

```text
SCHEMA_STATUS: NOT_FOUND
MIGRATION_DIRECTORY_STATUS: NOT_FOUND
RUNTIME_DB_HELPER: VERIFIED
```

Current evidence establishes a Neon PostgreSQL connection URL in
`app/core/constants.py` and sync SQLAlchemy helpers only. It does **not** establish any business table.

Known discrepancy:
- runtime core parses `constants.URL_DATABASE`, uses `postgresql+psycopg`, preserves Neon SSL/channel-binding query options and configurable `search_path`;
- `alembic.ini` references migration setup/directory that is absent and is not sufficient schema evidence.

`/api/v1/test/db` only declares `SELECT NOW()`; health readiness only reports configuration label and does not probe the DB.

Before any migration/query task, require authoritative table/column/PK/FK/unique/index/status/delete/timestamp/tenant rules. Query helpers do not commit; transaction ownership belongs to the future/current business use case that performs the write.
