# PLAN_RESULT — Study API #39 DD

**Task:** Tạo DD draft cho GET /api/v1/discussions
**Status:** Draft — Needs Confirmation
**Date:** 2026-10-12

## Kết quả

Tạo tám sheet Markdown theo template Study Server, cùng OPEN_QUESTIONS.md, PLAN_RESULT.md, VERIFICATION_REPORT.md và worklog. Không tạo ZIP; không thay đổi runtime hoặc canonical design inputs.

## Requirement matrix

| API | Method | Endpoint | Actor/Auth | Input | Response contract | Source behavior | Folder |
|---:|---|---|---|---|---|---|---|
| 39 | GET | /api/v1/discussions | Student / Bearer JWT | query course_id?:int64, page?:int32, sort?:string | ApiEnvelope<Page<Discussion>> | DERIVED: đọc root ACTIVE trong scope enrollment ACTIVE, kèm direct comments ACTIVE; policy cần xác nhận | 39_discussions |

## Source and evidence classification

| Source | Role | Evidence used | Status |
|---|---|---|---|
| docs/lists/list_api.md | API catalog | Method/path/auth/query/envelope/status/business codes and Discussion/Page schemas | APPROVED_DESIGN_CONTRACT; not runtime-verified |
| apps/study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md | AC index | AC-19 actor, precondition, postcondition and API mapping | Design evidence |
| apps/study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio | Activity flow | API #39 list; API #42 separately reads topic + comments | Design evidence; semantics incomplete |
| apps/study-server/docs/diagrams/DB_UNICA_TABLES.md | DB guide | discussions fields, self-reference and API #39–#42 DESIGN_ONLY status | DESIGN_ONLY |
| apps/study-server/docs/diagrams/DB_UNICA_ERD.drawio | ERD | discussions fields and relationships | DESIGN_ONLY |
| infra/postgres/study-server/DB.sql | Checked-in DDL | discussion/user candidate columns and nullability | DESIGN_ONLY; live schema unverified |
| contracts/api-guidelines/README.md | API guideline | Envelope and error data behavior | Contract convention |
| apps/study-server/app/api/v1.py, app/utils/auth.py, tests/ | Runtime source | No API #39 route/module/test; shared Student auth helper is only adjacent evidence | Current source |
| apps/study-server/docs/dd/10_courses_reviews | Related DD | Similar discussion self-reference; review-specific visibility/title assumptions not copied | Draft context |
| .agents/skills/create_dd_api/docs/dd/DD_API_Template_MD | Canonical template | Eight sheet structures and workbook audit appendices | Read and fingerprinted |

## Input manifest and coverage

| Source set | In-scope units | Read | Use |
|---|---:|---:|---|
| API catalog | API #39 row and reusable schema definitions | 1/1 | Approved request/response/status contract. |
| AC-19 index and activity flow | AC index plus matching AC page | 2/2 | Actor, precondition, flow and thread-list position. |
| DB diagrams | Diagram inventory; discussion ERD/table definition reviewed | Relevant discussion sources reviewed | Candidate fields, parent-child relationship and source gaps. |
| Checked-in DB DDL | users and discussions definitions | 2 table definitions | Candidate physical types/nullability; not live-schema evidence. |
| Runtime router/auth/tests | Discussion scan and current auth boundary | 3 source areas | API #39 absent; no runtime claim. |
| Related API #10 DD | Overview, response/data mapping and read-only pattern | Relevant sheets | Candidate discussion mapping only; review semantics excluded. |
| Canonical Markdown template | Eight files | 8/8 | Required sheet order and audit appendices. |
| Archive scan | Requested source/template roots | No in-scope archive identified | No extraction required. |

## Reconciliation summary

| Matrix | Draft treatment | Remaining gap |
|---|---|---|
| Request usage | Authorization plus the three catalog query fields only | Query parsing/range and access semantics |
| Query | Root discussions, users, enrollment access and direct ACTIVE comments are proposed; page=1/size=20 and created_at ordering are DERIVED | Confirm access/status, full-comment list boundary, sort and pagination/parse policy |
| Mutation | None; GET is read-only | None |
| Response source | Reusable Discussion/Page schemas preserved; comments and PageMeta use shared DERIVED proposals with API #42 | title source and approval of access/comment/page proposals |

## Scope and handoff

- Preserved API #39 catalog request fields, response schema and exact 200/401/403/500 error set.
- Kept title source and approval of access, visibility, comment scope, sort and pagination proposals open; the current proposal is aligned with API #40–#42.
- Marked API #39 UNWIRED / NOT_FOUND; database artifacts remain design evidence.
- No runtime, catalog, diagram, ERD, DDL, API #38 DD or shared context files changed.
- Review [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md) before marking Ready/Final or implementing API #39.
