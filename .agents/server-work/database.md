# Work database

Canonical schema: `apps/work-server/prisma/schema.prisma`; migration: `prisma/migrations/20260811000000_init_work_postgres/migration.sql`.

## `SystemRecord` / `system_records`

| Field | Database |
|---|---|
| `id` | UUID PK, default uuid |
| `key` | varchar(120), required, unique |
| `value` | nullable text |
| `createdAt` | `created_at`, timestamptz(6), default now |
| `updatedAt` | `updated_at`, timestamptz(6), Prisma `@updatedAt` |

No FK/relation/enum/soft-delete/domain ownership is present. Current services do not use the model.

Readiness uses raw `SELECT 1`; it does not query `system_records`.

Before a domain schema change, require current canonical design/approved requirement. Do not port old Flutter/Supabase/MySQL models into this clean PostgreSQL datasource by inference.
