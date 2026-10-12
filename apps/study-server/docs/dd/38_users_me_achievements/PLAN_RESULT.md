# PLAN_RESULT — Study API #38 DD

**Task:** Tạo DD draft cho GET /api/v1/users/me/achievements
**Status:** Draft — Needs Confirmation
**Date:** 2026-10-12

## Kết quả

Tạo tám sheet Markdown theo template Study Server, cùng OPEN_QUESTIONS.md, PLAN_RESULT.md và VERIFICATION_REPORT.md. Worklog được lưu tại [.agents/worklog/2026-10-12/create-study-api38-dd.md](../../../../../.agents/worklog/2026-10-12/create-study-api38-dd.md).

## Requirement matrix

| API | Method | Endpoint | Actor/Auth | Input | Response contract | Source behavior | Candidate inputs | Folder |
|---:|---|---|---|---|---|---|---|---|
| 38 | GET | /api/v1/users/me/achievements | Student / Bearer JWT | query course_id?:int64 | ApiEnvelope<Page<Achievement>> | AC-18: đọc achievement unlocked sau progress flow | Existing learning/assessment data; exact source/rule TBD | 38_users_me_achievements |

## Source and evidence classification

| Source | Role | Evidence used | Status |
|---|---|---|---|
| docs/lists/list_api.md | API catalog | Method/path/auth/input/envelope/status/business codes and Achievement/Page schemas | APPROVED_DESIGN_CONTRACT; not runtime-verified |
| docs/diagrams/AC_UNICA/00_AC_API_INDEX.md | AC index | AC-18 actor, precondition, postcondition and API list | Design evidence |
| docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio | Activity flow | API #38 reads unlocked achievements after progress calls | Design evidence; award semantics incomplete |
| docs/diagrams/DB_UNICA_TABLES.md | DB guide | V1 note: achievements/analytics computed from existing data; no award rule | DESIGN_ONLY |
| docs/diagrams/DB_UNICA_ERD.drawio | ERD | No physical achievements table in ERD V1 | DESIGN_ONLY |
| infra/postgres/study-server/DB.sql | Checked-in DDL | Candidate learning/assessment input tables; no achievements table | DESIGN_ONLY; live schema not verified |
| contracts/api-guidelines/README.md | API guideline | Envelope fields, error data=null, trace propagation | Contract convention |
| apps/study-server/app/api/v1.py | Runtime router | API #38 route absent | Current source |
| apps/study-server/app/utils/auth.py | Runtime auth helper | Current numeric JWT sub and Student role mapping | Current source; API #38 not wired |
| Related API #21 and #37 DDs | Adjacent design context | API #38 is separate; progress tables are not an approved award projection | Draft context |
| Canonical DD template | Markdown template | Eight sheet structures and workbook-source appendices | Read and fingerprinted |

## Input manifest and coverage

| Source set | In-scope units | Read | Use |
|---|---:|---:|---|
| API catalog | 1 file | 1 | Approved API #38 request/response/status contract and reusable schemas. |
| AC-18 index/diagram | 2 files | 2 | Actor, precondition, postcondition and flow ordering. |
| DB guide, ERD and checked-in DDL | 3 files | 3 | No achievements table; derived-from-existing-data design note; candidate input fields. |
| API guidelines and runtime router/auth source | 3 files | 3 | Envelope/error semantics and current route/principal boundary. |
| Related API #21/#37 DD | 3 files | 3 | Separate achievement call and adjacent progress source gaps. |
| Canonical Markdown DD template | 8 files | 8 | Sheet structure, appendices and baseline fingerprints. |
| Diagram directory inventory | 9 files | Inventory complete; target AC-18 and DB diagrams reviewed | Other AC flows do not define API #38. |
| Archive scan | Requested diagrams/catalog/template roots | 0 archives found | No archive extraction required. |

Checked-in database artifacts are design evidence, not live schema verification. Other AC pages were inventoried; detailed flow review is scoped to AC-18 and the DB ERD/table guide.

## Reconciliation summary

| Matrix | Decision in this draft | Remaining gap |
|---|---|---|
| Request Usage | Authorization maps to Student auth; optional course_id maps to filter step. | Parse/range policy, course filter and access semantics. |
| Query | Candidate lesson/quiz/assignment inputs only; no SQL authored. | Award criteria, source projection, joins, ordering and pagination predicates. |
| Mutation | None; GET is read-only. | None for mutation scope. |
| Response Source | Page<Achievement> fields match catalog reusable schemas. | Source/transform for Achievement fields, page defaults and empty result. |

## Scope and handoff

- Preserved API #38 catalog contract and error set without adding request fields, response fields or status codes.
- Recorded the DB design statement that achievements are derived from existing data; no persistence table or award rule was invented.
- Kept possible progress/assessment input tables explicitly candidate-only.
- Recorded award criteria, response projection, course filter/access, pagination, empty result and query validation in [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).
- No runtime source, API catalog, diagram, DB schema or migration changed; no ZIP created for Study Server.
- API #38 remains UNWIRED / NOT_FOUND; implementation or Ready/Final status requires decisions in OPEN_QUESTIONS.md.
