# Work database

Canonical schema: `apps/work-server/prisma/schema.prisma`.

The Work server uses PostgreSQL on Neon through a shared Prisma client. Runtime
requests use the pooled URL; Prisma CLI migration/generate commands use the
direct URL supplied by `scripts/prisma-with-constants.ts`.

The current database is the legacy Work schema with 12 Prisma models:
`SinhVien`, `DoanhNghiep`, `Chat`, `Cv`, `DoanChat`, `JD`, `ThongBaoDN`,
`ThongBaoSV`, `TopJD`, `TopCV`, `UngVien`, and `BanNganh` mapped to `bannganh`.
No authentication session table, token denylist or cookie-backed auth state is
stored in PostgreSQL.

Password columns are `VARCHAR(255)` in the Prisma schema, checked-in SQL
documentation and the `20260918120000_harden_password_storage` migration.
Runtime API projections never select these columns for public responses.

Do not drop or seed the Neon database during auth changes. Schema changes must
be made through the checked-in Prisma schema and migration chain.
