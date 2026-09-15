# Study database status

```text
SCHEMA_STATUS: VERIFIED
MIGRATION_DIRECTORY_STATUS: NOT_FOUND
RUNTIME_DB_HELPER: VERIFIED
```

Current evidence establishes a Neon PostgreSQL connection URL in
`app/core/constants.py`, sync SQLAlchemy helpers, and live schema metadata.

`infra/postgres/study-server/DB.sql` was applied successfully to these five
non-public application schemas: `chu_van_viet`, `dao_van_hung`,
`hoang_xuan_long`, `nguyen_anh_duc`, and `tran_anh_duc`. Each now contains 16
tables, for 80 tables total. The `public` schema was not modified, and system
schemas (`information_schema`, `pg_catalog`, `pg_toast`) were intentionally
excluded.

Known discrepancy:
- runtime core parses `constants.URL_DATABASE`, uses `postgresql+psycopg`, preserves Neon SSL/channel-binding query options and does not send `search_path` in the pooled startup package;
- `alembic.ini` references migration setup/directory that is absent and is not sufficient schema evidence.

`/api/v1/test/db` only declares `SELECT NOW()`; health readiness only reports configuration label and does not probe the DB.

Before any future migration/query task, require authoritative table/column/PK/FK/unique/index/status/delete/timestamp/tenant rules. Query helpers do not commit; transaction ownership belongs to the future/current business use case that performs the write.
