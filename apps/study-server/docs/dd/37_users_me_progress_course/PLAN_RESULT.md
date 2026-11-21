# PLAN_RESULT — Study API #37 DD

**Task:** Tạo DD draft cho GET /api/v1/users/me/progress/{course_id}
**Status:** Draft — Needs Confirmation
**Date:** 2026-10-12

## Kết quả

Đã tạo tám sheet Markdown theo template Study Server, cùng OPEN_QUESTIONS.md, PLAN_RESULT.md và VERIFICATION_REPORT.md. Worklog được lưu tại [.agents/worklog/2026-10-12/create-study-api37-dd.md](../../../../../.agents/worklog/2026-10-12/create-study-api37-dd.md).

## Requirement matrix

| API | Method | Endpoint | Actor/Auth | Input | Response contract | Source behavior | Candidate reads | Folder |
|---:|---|---|---|---|---|---|---|---|
| 37 | GET | /api/v1/users/me/progress/{course_id} | Student / Bearer JWT | path course_id:int64! | ApiEnvelope<UserProfile> | AC-18: sau chọn course, aggregate lesson + quiz + assignment progress | lesson_progress→lessons/courses; quiz_attempts→quizzes; assignment_submissions→assignments | 37_users_me_progress_course |

## Source and evidence classification

| Source | Role | Evidence used | Status |
|---|---|---|---|
| docs/lists/list_api.md | API catalog | Method/path/auth/input/envelope/status/business codes | APPROVED_DESIGN_CONTRACT; not runtime-verified |
| docs/diagrams/AC_UNICA/00_AC_API_INDEX.md | AC index | AC-18 actor, precondition, postcondition, API list | Design evidence |
| docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio | Sequence/flow | API #37 follows course selection; aggregate lesson + quiz + assignment | Design evidence; semantics incomplete |
| docs/diagrams/DB_UNICA_TABLES.md | DB guide | Table purpose, relations, candidate columns | DESIGN_ONLY |
| docs/diagrams/DB_UNICA_ERD.drawio | ERD | Candidate relations; no course_progress table | DESIGN_ONLY |
| infra/postgres/study-server/DB.sql | Checked-in DDL | Candidate physical types/nullability | DESIGN_ONLY; live schema not verified |
| app/api/v1.py and auth/response helpers | Runtime source | Current router/auth/envelope implementation boundary | API #37 is UNWIRED / NOT_FOUND |

## Input manifest and coverage

| Source set | In-scope units | Read | Use |
|---|---:|---:|---|
| API catalog `docs/lists/list_api.md` | 1 file | 1 | Approved API #37 contract and reusable schemas. |
| AC-18 index and Student Learning diagram | 2 files | 2 | Actor, precondition, postcondition and flow sequence. |
| DB table guide, ERD and checked-in DDL | 3 files | 3 | Candidate read tables, relations, columns and types. |
| API guidelines | 1 file | 1 | Envelope, error and trace conventions. |
| Runtime router, auth/response helpers and route/module/test inventory | 3 source files plus inventory review | Reviewed | Current wiring boundary; API #37 is not implemented. |
| Adjacent API #21 progress DD | 2 files | 2 | Existing progress response discrepancy context. |
| Canonical Markdown DD template | 8 files | 8 | Sheet structure, appendix and baseline fingerprints. |
| Relevant archive scan | 3 source roots | 0 archives found | No source archives required extraction. |

Coverage is complete for the scoped sources above. Checked-in DB design is not live-schema verification.

## Reconciliation summary

| Matrix | Decision in this draft | Remaining gap |
|---|---|---|
| Request Usage | Authorization and course_id map to identity/security and course scope. | Claim-to-user mapping; parse/range policy; query predicates. |
| Query | Candidate read relationships only; no executable SQL. | Join type, filters, inclusion rules, aggregation and ordering. |
| Mutation | None; GET is read-only. | None for mutation scope. |
| Response Source | ApiEnvelope fields follow catalog/guidelines; data remains UserProfile per catalog. | UserProfile has no progress payload; no confirmed source mapping. |

## Scope and handoff

- Preserved the catalog response and error set without adding fields or codes.
- Marked progress tables and DDL as design-only candidates.
- Recorded response, aggregation, attempt/submission selection, access, 403/404, empty state, path validation and JWT/live-schema questions in [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).
- No ZIP created for Study Server workflow.
- No runtime source, API catalog, diagram or DB schema changed.
- Implementation should wait for decisions in OPEN_QUESTIONS and a contract update where required.
