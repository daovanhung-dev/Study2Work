# Báo cáo kiểm chứng — API #76

- DD status: Draft — Needs Confirmation.
- Endpoint: `PATCH /api/v1/admin/courses/{course_id}/status`.
- Current source: route/module/middleware template allowlist and focused HTTP tests are present locally. This does not prove deployed API or live DB behavior.
- Direct contract: Bearer/Admin actor; path `course_id:int64!`; response `ApiEnvelope<Page<Course>>`; HTTP 200 `DESIGN_RESOURCE_UPDATED`; errors exactly 401/403/404/422/500 with catalog codes. Direct request body is absent.
- DERIVED runtime fallback: strict `{status}` body with DRAFT/PUBLISHED/SUSPENDED; shared ADMIN role; legacy BIGINT course/user mapping; `course_status_audit_logs`; direct target assignment; same-status no-op; atomic status+audit transaction; singleton Page.
- Live/schema gaps: migration 010 is not verified as applied; dedicated course-management permission, transition/readiness/suspension access policy and audit retention/DB immutability remain unresolved.

## Kiểm tra

| Check | Kết quả | Trạng thái |
|---|---|---|
| Worklog preflight | Deno selector found 69 coding worklogs; selected #74, #75 and #34; all three read; shortage none. | PASS |
| Plan-before-code | Classification, expected/current behavior, source trace, discrepancies and detailed plan written before application/schema/DD/context edits. | PASS |
| Catalog/diagram/schema | AC-32 status→update+audit flow; exact #76 catalog codes; legacy BIGINT and V1-PILOT UUID conflict retained. | PASS — STATIC |
| HTTP API #76 | 18 passed; status/audit parameters, no-op, ADMIN, validation, missing row, malformed lock projection, transaction rollback, response and OpenAPI covered with fake DB. | PASS — LOCAL TESTS |
| Linked regression | #06/#08/#71/#73–#76: 134 passed. | PASS — LOCAL TESTS |
| Full Study suite | 890 passed; one upstream Starlette/httpx TestClient deprecation warning. | PASS — LOCAL TESTS |
| Ruff | `ruff check app tests`: all checks passed. | PASS — STATIC |
| OpenAPI | 43 `/api/v1` path templates / 47 operations; API #76 exposes exact catalog responses and enum body schema. | PASS — LOCAL SOURCE |
| Middleware | Strict body errors return `DESIGN_VALIDATION_ERROR` with `data:null`; exact `/admin/courses/{course_id}/status` template is registered. | PASS — LOCAL HTTP |
| DDL/migration | `DB.sql` and migration 010 table columns/FKs match; both indexes match. | PASS — STATIC |
| ERD | Draw.io XML parses; IDs are unique; both new audit relations point to existing Course/User and audit nodes. | PASS — STATIC |
| DD package | 11 Markdown files; 8 sheet appendices retained; 2 JSON examples parse; 18 local file links resolve. | PASS — STATIC |
| Context manifest | API #76 module, test and migration paths are registered and exist. | PASS — STATIC |
| `git diff --check` | No whitespace errors. | PASS — STATIC |
| Deno context validator | Fails on pre-existing missing DB Admin context/source roots and links outside Study scope; no Study #76 path/context errors reported. | BASELINE FAIL — OUT OF SCOPE |

## Giới hạn kết luận

HTTP tests use fake sessions and rows. They do not execute PostgreSQL SQL, prove migration 010 was applied, establish live database constraints/grants, or prove production deployment and authorization policy. The audit-table shape and request/status semantics remain DERIVED local fallbacks; owner approval is still needed. The DD intentionally remains Draft.

## Fingerprints

| Fingerprint | Phạm vi | SHA-256 |
|---|---|---|
| Registered template pack | 8 template sheets; sorted filename + NUL + raw file bytes + NUL | `3dc7fd2242dd1ed1bd9faba50aadad913a31b97ebf1392d6144bb905c5208137` |
| DD output payload | 8 sheets + `OPEN_QUESTIONS.md` + `PLAN_RESULT.md`; excludes this report; same hash algorithm | `4cbf949c4de75685c1584223ee752dee5831b7aed9161061c9a6e879d249f422` |
