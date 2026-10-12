# PLAN_RESULT — Study API #25

## Kết quả

| Thuộc tính | Giá trị |
|---|---|
| API | #25 — Lưu vị trí và trạng thái |
| Endpoint | `PATCH /api/v1/lessons/{lesson_id}/progress` |
| DD output | [`25_lessons_progress/`](.) |
| DD lifecycle status | Draft — Needs Confirmation |
| Authoring result | PARTIALLY COMPLETED — DD draft authored; contract/schema questions remain in `OPEN_QUESTIONS.md`. |
| Package | Markdown folder only; no ZIP per Study Server workflow. |

## Basis and sources

- `docs/lists/list_api.md` — approved design contract row for API #25 and reusable `Lesson`/`ApiEnvelope` schemas.
- `apps/study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md` — AC-14 actor, precondition, postcondition and API sequence.
- `apps/study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio` — progress update, course aggregate and completion branches.
- `apps/study-server/docs/diagrams/DB_UNICA_TABLES.md` and `infra/postgres/study-server/DB.sql` — candidate `lesson_progress` mapping only; not live schema metadata.
- `apps/study-server/app/api/v1.py`, `apps/study-server/app/modules/` and `apps/study-server/tests/` — current runtime and focused-test inventory.
- `.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/` — eight-sheet Markdown template.
- `.agents/server-study/workflows/README.md` — Study API DD is Markdown-only; no new ZIP.

## Contract summary

- Actor/auth: Student Bearer JWT.
- Request: required path `lesson_id:int64`; body `position:int32`, `percent:int32`, `completed:boolean`; no query parameters.
- Success: HTTP 200 `DESIGN_RESOURCE_UPDATED`, `ApiEnvelope<Lesson>`.
- Errors: 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 422 `DESIGN_VALIDATION_ERROR`, 500 `DESIGN_INTERNAL_ERROR`.
- Mutation intent: AC-14 says update lesson progress and course aggregate; checked-in DB design identifies `lesson_progress` as a candidate only.

## Tables read

- `lessons` — candidate Lesson response/context source; API #25 query is not defined.
- `lesson_progress` — candidate current progress context; identity/lookup query is not defined.
- `enrollments` — possible access-policy source only; API #25 predicate is not confirmed.

## Tables write

- `lesson_progress` — candidate update/upsert target from AC-14 and DB design.
- Course aggregate target — SOURCE_REQUIRED; no physical table or formula is identified.

## Business code delta

- None. DD preserves the existing API #25 catalog business codes; no `BUSINESS_CODE_DELTA.md` is needed.

## Tables read

- `lessons` — candidate Lesson response/context source; API #25 query is not defined.
- `lesson_progress` — candidate current progress context; identity/lookup query is not defined.
- `enrollments` — possible access-policy source only; API #25 predicate is not confirmed.

## Tables write

- `lesson_progress` — candidate update/upsert target from AC-14 and DB design.
- Course aggregate target — SOURCE_REQUIRED; no physical table or formula is identified.

## Business code delta

- None. DD preserves the existing API #25 catalog business codes; no `BUSINESS_CODE_DELTA.md` is needed.

## Expected versus current behavior

- Expected: catalog defines API #25 request/response/codes; AC-14 says completion true marks `COMPLETED`, false keeps `IN_PROGRESS`, and names a course aggregate update.
- Current: Study router/module/test scan found no API #25 endpoint implementation or focused test. Checked-in ERD/DDL has candidate `lesson_progress`, no `position` column and no declared unique `(user_id, lesson_id)` key.
- Runtime status: `UNWIRED / NOT_FOUND`.

## Assumptions and conflicts

- Position unit/storage, percent range/conversion, state/timestamp transitions, upsert/retry semantics, authorization, 404/422 triggers, aggregate formula/target/transaction and response payload assembly remain unresolved.
- Catalog declares `ApiEnvelope<Lesson>` while the AC diagram uses generic `ApiEnvelope`; this DD preserves the catalog response and records the difference.
- ERD marks `user_id` and `lesson_id` required; checked-in DDL omits `NOT NULL`. Both artifacts are design evidence; live schema was not checked.
- No runtime, catalog, diagram, DDL, migration or context page was changed.

## Verification

Static DD verification results and template/output fingerprints are recorded in [VERIFICATION_REPORT.md](./VERIFICATION_REPORT.md). Application tests were not run because this task is documentation-only and API #25 is not wired. Context validation was not required because no canonical context page or registry changed.
