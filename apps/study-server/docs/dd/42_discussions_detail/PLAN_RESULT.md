# PLAN_RESULT — Study API #42 DD

**Task:** Tạo DD draft cho GET /api/v1/discussions/{discussion_id}
**Status:** Draft — Needs Confirmation
**Date:** 2026-10-23

## Kết quả

Tạo tám sheet Markdown theo template Study Server cùng ba báo cáo. Không tạo ZIP và không thay đổi runtime/API catalog/diagram/schema.

## Requirement matrix

| API | Method | Endpoint | Actor/Auth | Input | Response contract | Activity behavior | Folder |
|---:|---|---|---|---|---|---|---|
| 42 | GET | /api/v1/discussions/{discussion_id} | Student / Bearer JWT | path discussion_id:int64! | ApiEnvelope<Page<Discussion>> | AC-19 đọc topic + comments sau thao tác rồi hiển thị thread mới nhất | 42_discussions_detail |

## Source and evidence classification

| Source | Role | Evidence used | Status |
|---|---|---|---|
| docs/lists/list_api.md | API catalog | Exact #42 method/path/auth/input/response/200 and 401/403/404/500 set | APPROVED_DESIGN_CONTRACT; not runtime-verified |
| apps/study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md | AC index | AC-19 actor, precondition and sequence of four APIs | Design evidence |
| apps/study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio | Activity flow | #42 reads topic+comments after #40/#41 and displays latest thread | Design evidence |
| apps/study-server/docs/diagrams/DB_UNICA_TABLES.md | DB guide | discussions self-reference and status meaning | DESIGN_ONLY |
| apps/study-server/docs/diagrams/DB_UNICA_ERD.drawio | ERD | Discussion physical candidate fields and parent relation | DESIGN_ONLY |
| infra/postgres/study-server/DB.sql | Checked-in DDL | Discussion/user/enrollment columns, nullable FKs, ACTIVE defaults, TEXT content | DESIGN_ONLY; live schema unverified |
| apps/study-server/app/api/v1.py, app/utils/auth.py, module/test scan | Runtime source | No #42 route/module/test; current Student JWT helper precedent | Current source; #42 UNWIRED / NOT_FOUND |
| DD #39–#41 | Related designs | Current access, thread, write and response proposals | Draft context; macro reconciliation follows |
| Registered createDD-markdown template | Template | Eight sheet order/schema and source appendices | Source-backed; no archive found |

## Input and reconciliation coverage

| Source set | In-scope units | Read | Use |
|---|---:|---:|---|
| API catalog | #42 row and Discussion/DiscussionComment/Page schemas | 1/1 | Preserve response schema/status/error set; identify required title. |
| AC-19 | Index entry and full page nodes/edges | 2/2 | Read order, parent/reply branches, GET #42 output position. |
| DB diagram/schema | Diagram inventory, discussion ERD/table section and checked-in DDL | Relevant sources reviewed | Root/child mapping, columns, FKs, status and missing title/counter. |
| Runtime | Router, auth, module/test search | Relevant source reviewed | UNWIRED / NOT_FOUND; no runtime claim. |
| Template | Eight Markdown sheets and hashes | 8/8 | Match order, front matter and appendix format. |
| Archives | In-scope diagrams/catalog/adjacent DDs | None found | No extraction required. |

## Reconciliation summary

| Matrix | Draft treatment | Remaining confirmation |
|---|---|---|
| Authorization | ACTIVE enrollment in root course and ACTIVE topic | Confirm membership, status and concealment policy |
| Query | One root plus all direct ACTIVE comments; user summaries | Comment limits/indexes and nullable author integrity |
| Ordering | created_at ASC, id ASC | Confirm product display order |
| Response | One-item Page<Discussion> containing complete thread | Confirm page semantics; title source remains missing |
| Errors | Exact #42 code set; invalid path proposal maps to 404 | Align framework parsing with catalog and 403/404 policy |

## Scope and handoff

- Preserved exact API #42 contract and the declared 401/403/404/500 errors.
- Marked all inferred gates, sort, page values and parse behavior as DERIVED.
- No runtime, API catalog, diagram or schema file changed; runtime tests were not run.
- Read [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md) before approval/implementation.

