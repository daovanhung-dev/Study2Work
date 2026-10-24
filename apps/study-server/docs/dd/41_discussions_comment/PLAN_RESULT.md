# PLAN_RESULT — Study API #41 DD

**Task:** Tạo DD draft cho POST /api/v1/discussions/{discussion_id}/comments
**Status:** Draft — Needs Confirmation
**Date:** 2026-10-23

## Kết quả

Tạo tám sheet Markdown theo template Study Server, cùng OPEN_QUESTIONS.md, PLAN_RESULT.md, VERIFICATION_REPORT.md và worklog. Không tạo ZIP; không thay đổi runtime, API catalog, diagram hoặc schema.

## Requirement matrix

| API | Method | Endpoint | Actor/Auth | Input | Response contract | Source behavior | Folder |
|---:|---|---|---|---|---|---|---|
| 41 | POST | /api/v1/discussions/{discussion_id}/comments | Student / Bearer JWT | path discussion_id:int64!; body content:int64! | ApiEnvelope<Page<Discussion>> | AC-19: INSERT Comment + update counters, then API #42 reloads thread; direct-child/counter interpretation is marked DERIVED | 41_discussions_comment |

## Source and evidence classification

| Source | Role | Evidence used | Status |
|---|---|---|---|
| docs/lists/list_api.md | API catalog | Exact #41 method, path, actor, inputs, response, HTTP 201 and 401/403/404/422/500 codes | APPROVED_DESIGN_CONTRACT; not runtime-verified |
| apps/study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md | AC index | AC-19 actor, precondition, postcondition and API mapping | Design evidence |
| apps/study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio | Activity flow | Reply branch, insert-comment node, counter instruction, then GET #42 | Design evidence; counter storage unspecified |
| apps/study-server/docs/diagrams/DB_UNICA_TABLES.md | DB guide | discussions.parent_id self-reference and expected required relations | DESIGN_ONLY |
| apps/study-server/docs/diagrams/DB_UNICA_ERD.drawio | ERD | Discussion columns and parent-child relationship | DESIGN_ONLY |
| infra/postgres/study-server/DB.sql | Checked-in DDL | Candidate columns, nullable FKs, TEXT content, ACTIVE default, required timestamps | DESIGN_ONLY; live schema unverified |
| apps/study-server/app/api/v1.py, app/utils/auth.py, module/test scan | Runtime source | No #41 route/module/test; current Student JWT helper precedent | Current source; #41 UNWIRED / NOT_FOUND |
| apps/study-server/docs/dd/39_discussions and 40_discussions_create | Adjacent DDs | Existing access/title/content/PageMeta gaps and AC-19 sequencing | Draft context; not runtime evidence |
| .agents/skills/create_dd_api/docs/dd/DD_API_Template_MD | Canonical template | Eight-sheet structure and Markdown format | Read; Study workflow overrides ZIP output |

## Input manifest and coverage

| Source set | In-scope units | Read | Use |
|---|---:|---:|---|
| API catalog | API #41 row and reusable schemas | 1/1 | Preserve input/response/status/business codes and flag content type mismatch. |
| AC-19 index and activity flow | AC index plus relevant activity page | 2/2 | Identify Student precondition, reply branch, mutation label and API #42 reload. |
| DB design artifacts | Full diagram inventory; discussion ERD/table section and checked-in DDL | Relevant sources reviewed | Candidate row mapping and explicit absence of title/counter columns. |
| Runtime | Router, auth helper, module/test scan | Relevant source reviewed | State UNWIRED / NOT_FOUND; no runtime claim. |
| Adjacent DDs | API #39 and #40 request/mapping/open questions/reports | Relevant sections reviewed | Keep group behavior coherent and preserve unresolved contract conflicts. |
| Canonical Markdown template | Eight sheets | 8/8 | Required sheet order/front matter; source appendix retained from matching template sheets. |

## Reconciliation summary

| Matrix | Draft treatment | Remaining confirmation |
|---|---|---|
| Request | Exact path/body fields and types from catalog | Content meaning/conversion; root versus nested reply target |
| Write mapping | One child discussions row; parent_id from path; course from parent and user from JWT are DERIVED | Active-enrollment/topic access proposal, status and live nullability need confirmation |
| Counters | No physical counter update invented | Confirm whether counter is persisted or calculated from child rows |
| Response | Exact ApiEnvelope<Page<Discussion>>; propose one updated root item with every direct ACTIVE comment ordered like API #42, then reload | Page metadata/item semantics; title source and author projection |
| Errors | Exact catalog HTTP/business-code set | 403/404 concealment policy and detailed access predicate |

## Scope and handoff

- Preserved the #41 catalog contract and its HTTP 201, 401, 403, 404, 422 and 500 outcomes.
- Marked inferred behavior as DERIVED; kept explicit type/schema mismatches as DISCREPANCY.
- Current route/module/test state is UNWIRED / NOT_FOUND; runtime tests were not run.
- No runtime, catalog, diagram, or schema file was changed.
- Read [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md) before approval or implementation.
