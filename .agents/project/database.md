# Database context hiện hành

## Trạng thái

`infra/postgres/` hiện chứa bộ DDL bootstrap V1-PILOT cho ba database
`identity_db`, `study_db`, `work_db`; README và manifest mô tả tổng cộng 178
bảng. Đây là artifact bootstrap/schema tham khảo trong repository, không chứng
minh schema đã được áp dụng vào Neon hoặc database live. `setup_all.sh` tạo
database nếu chưa có, chạy các DDL file và xóa rồi tạo lại một số
trigger/policy; không chạy script này như một bước merge.

README của bộ DDL ghi nguồn sinh là `03_THIET_KE_CO_SO_DU_LIEU.md`. Chưa xác
nhận artifact này là migration chain của từng deployable. Không suy ra runtime
table/column chỉ từ DDL hoặc Git history; cần đối chiếu source, contract được
phê duyệt và live metadata theo đúng task.

| Scope | Runtime/config | Schema source hiện có |
|---|---|---|
| Study | sync SQLAlchemy `postgresql+psycopg`; Postgres/Redis compose | current queries reference `users`, `courses`, `lessons`, `categories`, `refresh_tokens`; migration artifacts and `infra/postgres/02_study_db.sql` are checked in, live schema remains unverified |
| AI | copied SQLAlchemy core, runtime không dùng | `NOT_FOUND`; không migration/model |
| Work | Prisma + PostgreSQL/Neon | `apps/work-server/prisma/schema.prisma` + migration history |
| DB Admin | SQLAlchemy + psycopg3 | two named backend-owned targets; runtime catalog plus independent `db_admin` control-plane bootstrap |

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
query primitive. Current app import được; `/api/v1/test/db` chỉ chứa `SELECT
NOW()` inline và `/health/ready` không probe DB. API source hiện references
`users`, `courses` và `lessons`; không suy rộng thành schema/table contract
ngoài current query, approved contract và live metadata. API #08/#09 source
wiring có trong checkout sau merge, nhưng chưa được runtime-verified ở task này.

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
confirmation state is bounded to the backend process, while audit entries have
bounded in-memory/structured-log fallback and a durable
`db_admin.admin_audit_events` path when the control-plane table exists. The SQL
bootstrap is not evidence that a live target has been applied.
