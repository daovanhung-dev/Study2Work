# Mobile conventions

`CONTEXT_STATUS: SOURCE_BACKED`

- Preserve existing public helper signatures and UI-facing model shapes while
  changing the data implementation underneath.
- All Neon SQL uses PostgreSQL parameters (`$1`, `$2`, ...) and quotes the
  case-sensitive table/column identifiers from the canonical schema.
- `NeonDatabase` normalizes driver rows, including `BIGINT` values, while
  models accept native PostgreSQL `DateTime`, nulls, and JSONB values.
- Do not log connection strings, credentials, or database row payloads that
  may contain secrets. Error handling should return the existing empty/false
  result shape where the old helper did so.
- Chat polling is a three-second `Timer`; every screen must cancel its timer in
  `dispose()`, and callbacks deduplicate messages by database `id`.
- The direct Neon mobile connection is a development/prototype convention only
  and must be replaced with a least-privilege backend boundary before release.
