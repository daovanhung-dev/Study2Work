# Báo cáo kiểm chứng — API #77

- DD status: `Draft — Needs Confirmation`.
- Endpoint: `DELETE /api/v1/admin/courses/{course_id}`.
- Runtime status: `SOURCE_BACKED / LOCAL_TESTED` — DELETE route/module, shared ADMIN guard and focused HTTP tests are wired.
- Direct contract: Bearer/Admin; `course_id:int64!`; không body/query; `ApiEnvelope<DeleteResult>`; HTTP 200 `DESIGN_RESOURCE_DELETED`; đúng năm error code catalog 401/403/404/422/500.
- DeleteResult fields: `id:int64`, `status:"deleted"`, `deleted_at:date-time`. Runtime maps `deleted_at` from DB-returned `courses.updated_at` (`DERIVED`, API #72 precedent).
- Derived behavior: block any enrollment, active generic Content, lesson, quiz or assignment with 422; set `courses.status='DELETED'`; repeat/missing target returns 404. No hard delete, cascade, migration or #76 audit write.
- Focused application tests: 20 passed; fake sessions do not execute PostgreSQL or prove deployed schema.

## Kiểm tra

| Check | Kết quả | Trạng thái |
|---|---|---|
| Worklog preflight | Deno selector chọn #74/#75/#76; cả ba worklog được đọc trước khi inspect sâu. | PASS |
| Plan trước code | Source trace, discrepancy table and implementation plan were written before source edits. | PASS |
| Catalog/diagram/source/schema | API #77/reusable DeleteResult, AC-32, current router/auth/middleware/error helpers and both schema candidates were compared. | PASS — STATIC |
| Direct contract/error set | DELETE path/auth/int64/no-body/no-query/response/status and exact 401/403/404/422/500 codes are exposed in OpenAPI/tests. | PASS |
| DeleteResult/mutation coverage | Three response fields map to runtime; status/timestamp/dependency choices are explicitly DERIVED; no cascade/audit. | PASS_WITH_OPEN_QUESTIONS |
| Focused HTTP tests | API #77 route tests cover auth, path, dependencies, success, DB projection/query/commit errors, rollback, trace and OpenAPI. | PASS — 20 passed |
| Exact package | Đúng 11 Markdown files: 8 template sheets + `OPEN_QUESTIONS.md`, `PLAN_RESULT.md`, `VERIFICATION_REPORT.md`; không có ZIP. | PASS — STATIC |
| Template appendices | 8/8 sheets preserve the exact template suffix; byte-identical trailing appendix lines: 62, 51, 19, 108, 88, 78, 61 and 45 by sheet order. | PASS — STATIC |
| JSON/tables/fences | Both `~~~json` examples parse; 31 Markdown table separator rows; 14 fence markers are balanced. | PASS — STATIC |
| Links/anchors/whitespace | 26 relative links resolve; all 9 checked local anchors resolve; all 11 files end with newline and have no trailing whitespace. | PASS — STATIC |
| Output fingerprints | Recomputed after final DD content edits; report excluded from output payload hash to avoid self-reference. | PASS — STATIC |
| AC-32 macro-review | #73–#76 runtime behavior reviewed; visibility/restore and Mentor writer gaps remain explicit in Open Questions. | COMPLETED_WITH_OPEN_QUESTIONS |
| Focused HTTP tests | API #77 route suite. | PASS — 20 passed |
| Linked AC regression | #06/#08/#72–#77 relevant HTTP suite. | PASS — 143 passed |
| Full Study regression | `.venv/bin/pytest -q`. | PASS — 910 passed; 1 upstream Starlette/httpx warning |
| Ruff | `.venv/bin/ruff check app tests`. | PASS — all checks passed |
| OpenAPI composition | Inspect current application OpenAPI paths and operations. | PASS — 43 path templates / 48 operations; shared Admin course path has GET/PUT/DELETE |
| Context validator | `deno run -A scripts/validate-agent-context.mjs --skip-drift`. | OUT-OF-SCOPE BASELINE — validator reports missing `db-admin` context/source tree only; no Study Server/API #77 path is reported missing. |

## Kết quả macro-review AC-32 #73–#77

- Ranh giới chức năng: #73 list/filter; #74 detail; #75 metadata-only update; #76 status update + audit intent theo diagram; #77 soft-delete theo policy. Không đưa status/audit vào #75 hoặc #77, không hard-delete/cascade.
- Giữ response theo catalog: #73–#76 dùng `Page<Course>`; #77 dùng `DeleteResult`. Singleton Page cho #74–#76 và body của #75/#76 là proposal, không phải contract mới.
- Flow nhắc counters cho #74 nhưng Course contract không định nghĩa counter fields; category relation của #73–#75 cũng chưa có source. Không thêm field, query hoặc relation.
- #73/#74 expose `DELETED` for Admin visibility; #75 can change metadata; #76 can replace status and thereby restore a course. This policy remains open.
- Shared unresolved items include dedicated course-management permission, live legacy schema, completeness of dependency set, repeated-delete semantics and whether Mentor writers must reject DELETED courses.
- Focused HTTP tests verify local route behavior, not live PostgreSQL, migration state, grants, deployed authorization policy or production delivery.

## Fingerprints

| Fingerprint | Phạm vi | SHA-256 |
|---|---|---|
| Registered template pack | 8 template filenames đã sort + NUL + raw bytes + NUL | `3dc7fd2242dd1ed1bd9faba50aadad913a31b97ebf1392d6144bb905c5208137` |
| DD output payload | 8 sheets + `OPEN_QUESTIONS.md` + `PLAN_RESULT.md`; loại report này khỏi digest để tránh self-reference; cùng thuật toán | `6d070c45f1f135ee7cbbf3f17b3eb6b49b47215411022284c09407ac9e305108` |

## Giới hạn kết luận

Local verification confirms the wired route and fake-session branches; it does not prove policy approval, live schema, database constraints, deployment or production behavior.
