# Study database status

```text
SCHEMA_STATUS: SOURCE_BACKED; LIVE_STATUS: NOT_VERIFIED_HERE
MIGRATION_DIRECTORY_STATUS: NOT_FOUND
RUNTIME_DB_HELPER: VERIFIED
```

Current source establishes a Neon PostgreSQL connection URL in
`app/core/constants.py` and sync SQLAlchemy helpers. The register query
references `users`; do not infer additional schema rules without authoritative
schema/live metadata.

`infra/postgres/study-server/DB.sql` is a checked-in schema/design artifact;
its live application status is not established by source inspection alone.
Do not treat it as proof that every described table is available to the current
runtime.

Known discrepancy:
- current `constants.py` contains a user-specific `DB_SCHEMA` value, while the
  current engine path does not send `search_path` in the pooled startup package;
- runtime core parses `constants.URL_DATABASE`, uses `postgresql+psycopg` and
  preserves Neon SSL/channel-binding query options;
- `alembic.ini` references migration setup/directory that is absent and is not sufficient schema evidence.

`/api/v1/test/db` only declares `SELECT NOW()`; health readiness only reports configuration label and does not probe the DB.

Before any future migration/query task, require authoritative table/column/PK/FK/unique/index/status/delete/timestamp/tenant rules. Query helpers do not commit; transaction ownership belongs to the future/current business use case that performs the write.
