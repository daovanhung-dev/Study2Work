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
- UI code consumes the shared `lib/app/theme/` Cobalt tokens and Material 3
  `ColorScheme`; new screen-specific primary colors, shadows or control styles
  should not be introduced. Keep white/transparent colors only where they are
  required for foreground, overlay or compositing semantics.
- Treat [`file-inventory.md`](file-inventory.md) and the two role pages as the
  source-backed map of file purpose. A file existing is not proof that it is
  wired: use `WIRED`, `UNWIRED`, `LEGACY`, `PLACEHOLDER` and UI-only labels from
  route/import evidence.
- Do not copy Neon URLs, Gemini keys, credentials or database row payloads into
  agent context. Document only configuration symbols, boundary behavior and
  prototype security risk.
