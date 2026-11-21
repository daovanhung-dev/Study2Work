# PLAN_RESULT — Study API #26

## Kết quả

| Thuộc tính | Giá trị |
|---|---|
| Status | Draft — Needs Confirmation; authoring/verification complete, owner decisions pending. |
| API ID | 26 |
| API name | Lấy tài nguyên đính kèm |
| Method / endpoint | `GET /api/v1/lessons/{lesson_id}/resources` |
| Output folder | `apps/study-server/docs/dd/26_lessons_resources/` |
| Basis | DIRECT contract + AC-15 flow; candidate data mapping is DESIGN_ONLY. |
| Scope | DD Markdown folder and docs worklog only. |

## Sources used

- `docs/lists/list_api.md` — API #26 contract and reusable schema.
- `apps/study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md` — AC-15 behavior and API grouping.
- `apps/study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio` — AC-15 sequence/design nodes.
- `apps/study-server/docs/diagrams/DB_UNICA_TABLES.md` — resource relation/columns and visibility discrepancy.
- `infra/postgres/study-server/DB.sql` — checked-in candidate DDL; not live schema evidence.
- `apps/study-server/app/api/v1.py`, `app/modules/`, `tests/` — current wiring/test inventory.
- `apps/study-server/docs/dd/24_lessons_detail/`, `25_lessons_progress/` — adjacent DD conventions and worklog context.
- `.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/` — eight-sheet Markdown template.

## Data scope

- Tables read: `resources` candidate; `lessons` candidate for parent/access context.
- Tables written: `N/A — READ-ONLY API`.
- External calls: none confirmed for API #26; signed URL behavior remains open.

## Assumptions and conflicts

- Preserve catalog request, response type, actor and status/business-code set.
- Keep `ApiEnvelope<Lesson>` while flagging that Resource/list payload is not represented by the declared reusable schema.
- Keep resource query, cardinality, ordering, empty-result, entitlement, publish, visibility and signed URL behavior unresolved; see [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).
- API #26 current runtime status is `UNWIRED / NOT_FOUND`; API #12 is a separate resource-detail route.
- Do not modify runtime, API catalog, diagrams, DDL, context pages or existing DDs.

## Verification

- Markdown/template/JSON/link/contract and source status checks passed; details are in [VERIFICATION_REPORT.md](./VERIFICATION_REPORT.md).
- Study application tests are not part of this docs-only task and will be recorded as `NOT_RUN`.
- No ZIP is produced per the Study Server workflow.

