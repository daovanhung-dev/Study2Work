# PLAN_RESULT — Study API #24

## Kết quả

| Thuộc tính | Giá trị |
|---|---|
| API | #24 — Nạp nội dung bài học / Lấy nội dung chính |
| Endpoint | `GET /api/v1/lessons/{lesson_id}` |
| DD output | [`24_lessons_detail/`](.) |
| DD lifecycle status | Draft — Needs Confirmation |
| Authoring result | PARTIALLY COMPLETED — DD draft authored; contract gaps remain in `OPEN_QUESTIONS.md`. |
| Package | Markdown folder only; no ZIP per Study Server workflow. |

## Basis and sources

- `docs/lists/list_api.md` — approved design contract row for API #24 and reusable `Lesson`/`ApiEnvelope` schemas.
- `apps/study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md` — AC-14/15 actor, preconditions, postconditions and API sequence.
- `apps/study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio` — AC-14 lesson learning sequence and AC-15 access/publish check.
- `apps/study-server/docs/diagrams/DB_UNICA_TABLES.md` and `infra/postgres/study-server/DB.sql` — candidate schema/mappings only; not live metadata.
- `apps/study-server/app/api/v1.py`, `apps/study-server/app/modules/`, and `apps/study-server/tests/` — current runtime and focused-test inventory.
- `.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/` — eight-sheet Markdown template.
- `.agents/server-study/workflows/README.md` — Study API DD is Markdown-only; no new ZIP.

## Contract summary

- Actor/auth: Student Bearer JWT.
- Request: required path `lesson_id:int64`; no query or body declared.
- Success: HTTP 200 `DESIGN_RESOURCE_RETRIEVED`, `ApiEnvelope<Lesson>`.
- Errors: 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 500 `DESIGN_INTERNAL_ERROR`.
- Read candidate: `lessons`; access/publish candidate sources are not fixed.
- Write tables: N/A — read-only GET.

## Expected versus current behavior

- Expected: catalog defines API #24 contract; AC-14 and AC-15 place it in the learning/content flow. AC-15 says check access and publish status before reading Lesson/content.
- Current: no API #24 route, module, query or focused test was found in Study source. API #12's parent-lesson lookup is a separate resource-detail implementation.
- Runtime status: `UNWIRED / NOT_FOUND`.

## Assumptions and conflicts

- Access predicate, token-to-enrollment binding, publish scope, 403/404 split, error payload, optional/null behavior, `LessonStatus` values and exact query remain unresolved; no behavior was invented.
- Catalog declares `ApiEnvelope<Lesson>` while diagrams show generic `ApiEnvelope`; the DD preserves catalog's specific response type.
- Checked-in DDL omits `NOT NULL` for `lessons.course_id`; DB design text and catalog model it as required. This remains a design discrepancy.
- Checked-in DDL/ERD are design evidence and do not establish live schema.

## Verification

- Required output: eight template sheets plus this plan, `OPEN_QUESTIONS.md` and `VERIFICATION_REPORT.md`.
- Static checks passed: 11 deliverables present, 8 sheet metadata/order checked, tables/fences/whitespace validated, JSON examples parsed, local links/anchors resolved and response error-code set matched to catalog; details/fingerprints are in `VERIFICATION_REPORT.md`.
- Runtime tests: not run; API #24 is not wired and the approved plan excludes application tests.
- Context validator: not run; no canonical context page or registry changed.
