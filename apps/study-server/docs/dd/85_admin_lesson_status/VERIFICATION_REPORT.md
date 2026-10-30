# Báo cáo kiểm chứng — API #85

## Phạm vi

- API #85 locally wired at `PATCH /api/v1/admin/lessons/{lesson_id}/status`.
- Added module, route-template middleware entry, migration source 012, focused HTTP tests, DD and Study Server context entries.
- DD remains `Draft — Needs Confirmation`; live schema/migration deployment and dedicated AC-34 permission are not verified.
- No ZIP created under the Study Server workflow.

## Template fingerprints

SHA-256 baseline của bộ template registry createDD-markdown:

| File | SHA-256 |
|---|---|
| 00_Cover.md | fd5f568c5329d3069fbaff617a6f4ed3b5ffaf050e042c95b7c9100a05f79e63 |
| 01_Lich_su.md | d1cec6573433a9551812bf47552f8a44d7c533d790341941047c410e1d57771e |
| 02_Overview.md | c2879c2f0e007395558dfee4167484786c5aadb3fdd63ab135ca111e7c5f8aa6 |
| 03_Request.md | 37aaa1e9d7f3e83329e81ab38d922c9dff959284d5b7b3ae353878798dd4b7aa |
| 04_Response.md | 5bcb43ba5eb487302dd5d5efde4383b9f452f9fed2149f55315d64ff78a19ab8 |
| 05_Data_Mapping.md | 11bc77bc0522d3af27b9499114991c8819046ac32bde5c1efdc841be088dcc5b |
| 06_Error.md | e0160ea07fdbc74f2cafebd6ed3b21e60029662d28d67f5f6a0b4d95ba72be9b |
| 07_table.md | 4c9a0e037872333210aaf44ba9fbf00a0e63343a69d55250e537d2c3c5e2d356 |

## Checks

| Check | Result | Status |
|---|---|---|
| Catalog and AC-34 | Direct method/path/auth/response/error set retained; body/status/audit physical mapping explicitly DERIVED. | Source review |
| Runtime behavior | Shared ADMIN guard; signed-int64 path validation; lock/update/audit/map/commit flow. | HTTP tested |
| Status semantics | `{status}` and `DRAFT/PUBLISHED/SUSPENDED` reuse API #76 candidate; no transition matrix; same-status no-op. | DERIVED; owner approval open |
| Schema mapping | Legacy BIGINT Lesson + migration 012 audit; V1-PILOT UUID remains separate. | Local source only; deployment unverified |
| Focused API #85 tests | 28 passed. | VERIFIED |
| Linked #09/#47/#48/#82–#85 tests | 132 passed. | VERIFIED |
| Full Study suite | 1078 passed; one upstream Starlette/httpx deprecation warning. | VERIFIED |
| Ruff | `ruff check app tests` passes. | VERIFIED |
| OpenAPI | 50 `/api/v1` paths / 56 operations; #85 body required; 401/403/404/422/500 declared. | VERIFIED |
| DD package/appendix/static checks | 11 files; 8/8 appendix suffixes exact; 37 tables / 430 rows; 18 fence markers balanced; 4 JSON blocks parse; 40 local links resolve; no trailing whitespace. | PASS |
| `git diff --check` | No diagnostics. | PASS |
| Context validator | API #85 paths are present; validator fails only on pre-existing missing DB Admin context/source and unavailable baseline commit `9a70eb6764a6587093a92d3bd7e4cc0bea1651c4`. `--skip-drift` removes baseline findings but still fails on DB Admin scope. | PARTIAL |

## Limits

Fake DB HTTP tests cannot prove SQL execution against live PostgreSQL, migration application, current production schema, fine-grained permission enforcement or owner approval of the status policy.

## AC-34 macro-review

- API #85 owns status and audit; #84 remains metadata update; #86 remains delete; all successful branches return to API #82 list reload.
- Macro-review remains `VERIFIED_WITH_OPEN_QUESTIONS`, not owner approval or deployed verification.
- See the [consolidated review matrix](../86_admin_lesson_delete/VERIFICATION_REPORT.md#ac-34-macro-review).
