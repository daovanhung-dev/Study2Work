# Plan Result — Study API #33

## Status

Draft — Needs Confirmation.

## Output

- DD folder: `apps/study-server/docs/dd/33_assignments_detail/`.
- Sheets: `00_Cover.md`, `01_Lich_su.md`, `02_Overview.md`, `03_Request.md`, `04_Response.md`, `05_Data_Mapping.md`, `06_Error.md`, `07_table.md`.
- Reports: `OPEN_QUESTIONS.md` and `VERIFICATION_REPORT.md`.
- ZIP: N/A — Study Server workflow does not package DDs as ZIP.

## Basis and sources

- `docs/lists/list_api.md` — `APPROVED_DESIGN_CONTRACT`; API #33 method/path, Student Bearer, `Assignment` response and status/business-code set.
- `apps/study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md` — API #33 to AC-17 trace.
- `apps/study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio` — AC-17 assignment fetch, submission-rule step, deadline/access decision and later API calls.
- `apps/study-server/docs/diagrams/DB_UNICA_TABLES.md` and `DB_UNICA_ERD.drawio` — candidate assignment fields and relationships.
- `infra/postgres/study-server/DB.sql` — checked-in design DDL; not live-schema evidence.
- `contracts/api-guidelines/README.md` — shared envelope/error convention.
- `apps/study-server/app/api/v1.py`, `app/utils/auth.py`, module and test inventory — current route/auth/runtime status.
- `.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/` — canonical eight-sheet Markdown template.

## Tables read

- Candidate: `assignments`.
- `enrollments`: considered only as a possible access source; no query/predicate is selected because AC-17 does not define it.

## Tables write

- None; API #33 is GET/read-only.

## Query and response basis

- Candidate lookup: `assignments.id = assignment_id`; selected candidates are `id`, `course_id`, `name`, `description`, `due_at`, and `max_score`.
- Logical `Assignment.title` maps to physical `assignments.name` per DB table notes.
- Response fields follow the reusable `Assignment` schema only; no submission-rule property is invented.
- No runtime SQL, live-schema claim, mutation or external call is included.

## Assumptions and conflicts

- Follow the exact API #33 catalog contract and preserve its 401/403/404/500 error set.
- AC-17's overdue/no-permission branch includes 409, which conflicts with the API #33 catalog; no 409 is added.
- AC-17 mentions a submission rule, but the `Assignment` response schema does not define rule fields.
- Checked-in DDL permits NULL for `course_id` and `max_score`; the logical response requires both. Live schema is not verified.
- Current Study router/module/test surface does not include API #33; this DD is design-only.
