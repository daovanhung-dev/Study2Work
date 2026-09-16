# Database context hiện hành

## Trạng thái

Các standalone SQL/schema từng được README nhắc tới không tồn tại trong working
tree hiện tại. Không lấy table/column từ Git history hoặc diagram để code.

| Scope | Runtime/config | Schema source hiện có |
|---|---|---|
| Study | sync SQLAlchemy `postgresql+psycopg`; Postgres/Redis compose | `NOT_FOUND`; không có `alembic/` |
| AI | copied SQLAlchemy core, runtime không dùng | `NOT_FOUND`; không migration/model |
| Work | Prisma + PostgreSQL/Neon | `apps/work-server/prisma/schema.prisma` + migration history |
| DB Admin | SQLAlchemy + psycopg3 | two named externally configured Neon targets (`work_server`, `study_server`); runtime catalog only, no migrations |

## Work PostgreSQL/Neon

Canonical source is `apps/work-server/prisma/schema.prisma`, with migrations in
`apps/work-server/prisma/migrations/`. The current schema has 12 Prisma models:
`SinhVien`, `DoanhNghiep`, `Chat`, `Cv`, `DoanChat`, `JD`, `ThongBaoDN`,
`ThongBaoSV`, `TopJD`, `TopCV`, `UngVien`, and `BanNganh` mapped to lowercase
`bannganh`.

The two checked-in migrations create the PostgreSQL baseline and add/backfill
the `bannganh` lookup plus the unique `(jd_id, sinhvien_id)` application key.
Domain IDs are PostgreSQL identity `BIGINT`; timestamps use `timestamptz(3)`;
`Cv.social` uses `JSONB`. The mobile clients query the same quoted legacy table
names directly through the `postgres` pooler driver.

No `system_records` model/table, Work health probe, token denylist, or
cookie-backed auth state is present in the current Work source.

`apps/work-server/docs/database/schema.sql` is the retained MySQL-era reference;
`apps/work-server/docs/database/neon.sql` is the PostgreSQL-oriented companion.
Prisma schema and migrations remain the runtime source of truth.

## Study DB helper contract

`apps/study-server/app/core/database.py` có factory/session và parameterized
query primitive, nhưng không xác nhận table nào. `/api/v1/test/db` chỉ chứa
`SELECT NOW()` inline và app không import được. `/health/ready` không probe DB.

`alembic.ini` trỏ tới directory thiếu và dùng URL asyncpg cứng, trong khi runtime
core dùng psycopg sync. Ghi discrepancy, không tạo migration theo config này nếu
chưa có requirement.

## Database change rule

Trước khi thêm query/migration phải có schema/requirement xác nhận table,
column, PK/FK, unique/check/index, enum/status, delete/timestamp policy và tenant/
transaction boundary. Query module không sở hữu commit; use case sở hữu atomic
transaction theo architecture thực tế của scope.

## DB Admin target

`apps/db-admin-server/` deliberately does not infer or copy the Study/Work
schema. The backend-owned `DATABASE_TARGETS` mapping provides the named
`work_server` and `study_server` connections; credentials are never exposed to
Angular. Catalog queries use `information_schema` and `pg_catalog`; DDL, row
CRUD and SQL execution use request-isolated transactions. DDL and row mutation
confirmation state is bounded to the backend process, while audit entries are
bounded in memory and structured logs only.
