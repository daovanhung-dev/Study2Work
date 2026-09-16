# Work database

Canonical schema: `apps/work-server/prisma/schema.prisma`; migration history:
`prisma/migrations/20260811000000_init_work_postgres/` and
`prisma/migrations/20260916100000_work_domain/`. The portable design artifact is
`infra/postgres/work-server/schema.sql`; `infra/mysql/work-server/schema.sql` is
legacy/design-only and is not a runtime source.

## `SystemRecord` / `system_records`

| Field | Database |
|---|---|
| `id` | UUID PK, default uuid |
| `key` | varchar(120), required, unique |
| `value` | nullable text |
| `createdAt` | `created_at`, timestamptz(6), default now |
| `updatedAt` | `updated_at`, timestamptz(6), Prisma `@updatedAt` |

No FK/relation/enum/soft-delete/domain ownership is present. Current services do not use the model.

The Neon deployment was verified with `prisma migrate deploy`: two migration
rows, 55 application tables, 99 foreign keys, 31 unique constraints, 30 checks
and 151 indexes were observed in `public`. Readiness uses raw `SELECT 1`; it
does not query `system_records`.

The domain models use PostgreSQL identity `BIGINT` IDs, UUID operation/event
IDs, `timestamptz(6)` UTC timestamps and `jsonb` snapshots/metadata. Applications
retain job/CV revision IDs and submission snapshots. Payment rows retain
provider references and money/status metadata only.

Database URLs are selected from the local-only Work constants profile. The
Prisma wrapper renders that URL into a temporary schema for `generate`,
`validate`, and `migrate deploy`; the checked-in schema contains only a valid
placeholder URL and never reads `.env`.

Before a domain schema change, require current canonical design/approved requirement. Do not port old Flutter/Supabase/MySQL models into this clean PostgreSQL datasource by inference.
