---
task_id: "2026-10-24-create-study-api87-dd"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD Study API #87 — Lấy danh sách quiz

## PRIOR_WORKLOG_REVIEW

- primary_task_type: docs
- selector_command: deno run --allow-read --allow-env scripts/select-worklogs.mjs --type docs --limit 3
- prior_worklogs_reviewed:
  - path: .agents/worklog/2026-10-24/create-study-api48-dd.md
    - carry_forward: Giữ contract trực tiếp; tách source/schema candidate khỏi runtime và không bịa query/field để lấp gap.
  - path: .agents/worklog/2026-10-24/create-study-api49-dd.md
    - carry_forward: Khi list/tree intent mâu thuẫn response đơn, ghi discrepancy và proposal DERIVED; giữ nguồn schema và error codes rõ ràng.
  - path: .agents/worklog/2026-10-24/create-study-api50-dd.md
    - carry_forward: Chỉ suy diễn behavior đơn giản, ghi rõ DERIVED; không biến candidate persistence thành physical schema được xác nhận.
- shortage: none

## EXPECTED_BEHAVIOR

- Requirement: Tạo một DD tiếng Việt cho API #87, lập và ghi plan trước khi tạo DD; đọc AC-35 cùng diagram/schema liên quan; dùng Markdown templates; kiểm tra ngay package sau khi tạo.
- Canonical contract: docs/lists/list_api.md row #87 — GET /api/v1/admin/quizzes, Bearer JWT, role Admin, query course?:int64, status?:string, page?:int32, ApiEnvelope<Quiz>, HTTP 200 DESIGN_RESOURCE_RETRIEVED, errors 401/403/500.
- AC-35 flow: Admin mở trang → #87 truy vấn quizzes → Admin chọn #88 create, #89 update, #90 delete, hoặc #91 statistics. Đây là DD đầu của nhóm; macro-review #87–#91 chờ đủ các DD nhóm.
- Output: apps/study-server/docs/dd/87_admin_quizzes_list/, tám template sheets và ba report chuẩn; không tạo ZIP.

## CURRENT_BEHAVIOR

- Source/config: Không tìm thấy route /api/v1/admin/quizzes, marker API #87, module view hoặc test tương ứng trong apps/study-server/app và apps/study-server/tests. Middleware không có path này trong DESIGN_CONTRACT_PATHS; auth helper hiện kiểm tra role STUDENT. Mọi hậu quả khi route được thêm chỉ là conditional integration concern.
- Data sources: Catalog Quiz có id, course_id, title, duration_minutes?, passing_score, questions[]. QuizQuestion có id, text, type, choices[]. QuizChoice và QuestionType chưa có định nghĩa đầy đủ.
- Schema: infra/postgres/study-server/DB.sql là legacy candidate BIGINT với quizzes, quiz_questions, quiz_choices. infra/postgres/02_study_db.sql là V1-PILOT khác mô hình: UUID assessments, quiz_questions.assessment_id, quiz_options. Live schema chưa xác minh; không trộn hai mô hình.
- Tests/runtime: Không có test API #87; không chạy application tests cho task docs-only.

## SOURCE_TRACE

    Admin Bearer principal + quiz-management permission → GET #87 → lọc quiz theo course/status và trang → candidate đọc Quiz metadata/question set → dựng envelope theo contract hoặc proposal list cần xác nhận → UI chọn nhánh #88–#91.

## PLAN BEFORE DD AUTHORING

1. Giữ nguyên method/path/auth/query names/types, response type trực tiếp ApiEnvelope<Quiz>, HTTP 200 và đúng ba error codes 401/403/500. Không thêm 404/422.
2. Đối chiếu AC-35 node/edge: #87 là bước truy vấn danh sách trước decision Create/Update/Delete/Statistics; không đưa mutation, delete policy hoặc aggregate statistics vào #87.
3. Map course → candidate quizzes.course_id, status → candidate quizzes.status; khi có filter thì đề xuất exact match. Không áp dụng mặc định status.
4. Diễn giải page là trang 1-based, mặc định 1; đề xuất fixed size 20 và id ASC để phân trang ổn định, mượn convention của API #07. Đây là DERIVED, vì catalog không định nghĩa default, size, sort, total hoặc pagination response.
5. Ghi discrepancy: endpoint/diagram là list và có page, nhưng response catalog khai báo một Quiz; đề xuất ApiEnvelope<Page<Quiz>> dùng reusable Page<T> nếu owner chấp thuận, không ghi proposal thành direct contract.
6. Giữ đủ field theo reusable Quiz/QuizQuestion. Dùng legacy BIGINT table/column chỉ làm candidate. QuestionType, QuizChoice, choices ordering và field đáp án không có contract đầy đủ; không thêm is_correct hoặc giả định response shape.
7. Candidate reads: Q1 quiz metadata và filter; count cùng predicate chỉ áp dụng nếu proposal Page được duyệt; Q2 question rows theo quiz IDs; Q3 choices theo question IDs chỉ khi response cần nested questions. Ghi rõ AC-35 diagram chỉ nêu “Query quizzes” và nested reads là candidate để đáp ứng schema Quiz.
8. Ghi đúng auth boundary: AC-35 yêu cầu quiz-management permission; catalog role Admin; Study source chưa có Admin guard. Ghi conditional middleware error-code mismatch cho path chưa allowlist, không mô tả nó như runtime của API chưa tồn tại.
9. Tạo tám sheet từ template baseline và PLAN_RESULT.md, OPEN_QUESTIONS.md, VERIFICATION_REPORT.md; 07_table.md là read-only candidate mapping. Static-check exact package, template suffix, catalog/errors, JSON, tables, fences, links và whitespace.
10. Giữ trạng thái Draft — Needs Confirmation, không sửa router/schema/catalog/diagram/context pages. Sau #91 thực hiện macro-review AC-35 trên toàn nhóm #87–#91.

### API Requirement Matrix

| API ID | Method/path | Actor/auth | Input | Response/success | Errors | Basis/status |
|---|---|---|---|---|---|---|
| #87 | GET /api/v1/admin/quizzes | Bearer JWT; Admin | course?:int64, status?:string, page?:int32; không body/path | ApiEnvelope<Quiz>; 200 DESIGN_RESOURCE_RETRIEVED | 401 DESIGN_AUTHENTICATION_REQUIRED; 403 DESIGN_ACCESS_DENIED; 500 DESIGN_INTERNAL_ERROR | Catalog DIRECT; AC-35 list intent DIRECT; filters/page semantics DERIVED/open |

### Request Usage Matrix

| Request field | Source/use | Query use | Rule/status |
|---|---|---|---|
| Authorization | Bearer principal + Admin role/permission | Gate before quiz query | Catalog role DIRECT; AC permission DIRECT; Study Admin guard NOT_FOUND |
| course | Optional int64 course filter | Candidate quizzes.course_id = :course_id | Exact match DERIVED; range/malformed mapping open |
| status | Optional string filter | Candidate quizzes.status = :status | Exact match DERIVED; enum/casing SOURCE_REQUIRED |
| page | Optional int32 page index | Candidate page offset | 1-based/default 1 DERIVED; page size/response pagination open |
| Body/path | Not declared | None | DIRECT from catalog |

### Query Matrix

| Query | Purpose | Candidate source/fields | Predicate/order | Status |
|---|---|---|---|---|
| Q1 | Quiz metadata page | Legacy quizzes: id, course_id, name, passing_score, time_limit_minutes; status only for filter | Optional course/status exact match; id ASC; page window if approved | Legacy candidate; semantics DERIVED |
| Q1C | Total matching quizzes | Legacy quizzes.id | Same optional filters as Q1 | Only for proposed Page<Quiz>; not direct contract |
| Q2 | Nested question set | Legacy quiz_questions: id, quiz_id, question_text, sort_order | quiz_id IN page quiz IDs; sort_order ASC, id ASC candidate | Schema requires questions; diagram omits read detail; DERIVED |
| Q3 | Choice set | Legacy quiz_choices: id, question_id, choice_text; no chosen output shape | question_id IN page question IDs; no order field in legacy source | SOURCE_REQUIRED until QuizChoice contract/order defined; do not select key field as response |

### Mutation Matrix

| Operation | Target | Condition | Fields | Status |
|---|---|---|---|---|
| None | N/A | GET list only; #88–#90 own mutations | No INSERT/UPDATE/DELETE | N/A — READ-ONLY API |

### Response Source Matrix

| Response field | Candidate source | Mapping/status |
|---|---|---|
| Envelope | Reusable ApiEnvelope<T> | Direct shape; error data guideline/current helper discrepancy remains |
| data.id | quizzes.id | Candidate direct |
| data.course_id | quizzes.course_id | Candidate direct; legacy nullable vs contract required |
| data.title | quizzes.name | Alias candidate |
| data.duration_minutes | quizzes.time_limit_minutes | Alias candidate; nullable |
| data.passing_score | quizzes.passing_score | NUMERIC→decimal-string candidate |
| data.questions[] | quiz_questions and quiz_choices | Catalog-required nested field; type and QuizChoice schema unresolved |
| data collection/page shape | List name, AC-35 and page input vs catalog ApiEnvelope<Quiz> | DISCREPANCY; proposed ApiEnvelope<Page<Quiz>> needs confirmation |

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| List vs response cardinality | Catalog says ApiEnvelope<Quiz>; operation/AC say list and accept page | DISCREPANCY | Direct contract retained; proposed Page wrapper is not approved |
| Quiz nesting | Quiz schema requires questions; AC-35 says only “Query quizzes” | DERIVED / SOURCE_REQUIRED | Candidate batched nested reads; full mapping blocked by type/choice gaps |
| Physical model | Legacy BIGINT quiz tables vs V1-PILOT UUID assessment model; live schema absent | DISCREPANCY / NOT_VERIFIED | No model treated as deployed |
| Admin authorization | Catalog role + AC-35 permission; current helper Student-only | SOURCE_REQUIRED / NOT_FOUND | No runtime authorization claim |
| Error integration | Contract 401/403/500; path absent from middleware design allowlist | DISCREPANCY / CONDITIONAL_FUTURE_WIRING | Future route may return generic fallback codes unless wiring is updated |

## CHANGES

- Files changed: `.agents/worklog/2026-10-24/create-study-api87-dd.md`, `apps/study-server/docs/dd/87_admin_quizzes_list/` (11 Markdown files), and the API-count inventory worklog.
- CONTEXT_UPDATES: None.
- Context pages changed: None; no runtime, schema, catalog, diagram, router, or test source changed.
- Assumptions: Exact-match filters, page 1/default, fixed page size 20, and id ASC remain explicitly labeled DERIVED proposals; direct catalog contract is preserved.

## VERIFICATION

| Check | Result | Status |
|---|---|---|
| DD package | 11 Markdown files: eight template sheets and three standard reports. | `PASS — STATIC` |
| Template suffix parity | All eight appendix suffixes byte-match the registered Markdown templates. | `PASS — STATIC` |
| Contract and examples | Direct endpoint/query/response/success/error contract retained; four JSON blocks parse. | `PASS — STATIC` |
| Markdown structure | 450 table lines have consistent widths; five code fence pairs balanced; 32 local links including 15 anchors resolve; final newline and whitespace checks pass. | `PASS — STATIC` |
| Runtime source scan | No API #87 route/path/ID marker or matching module/test found under `apps/study-server/app` and `apps/study-server/tests`. | `UNWIRED / NOT_FOUND` |
| Application tests | Not run; task is docs-only and API #87 has no route. | `NOT_RUN` |
| `git diff --check` | Tracked inventory worklog edit clean; custom whitespace scan covered the untracked DD folder and task worklog. | `PASS` |
| Context validation | No `.agents/server-study` page or registry changed. | `NOT_APPLICABLE` |

## HANDOFF

- DD #87 is verified statically and remains `Draft — Needs Confirmation`; list cardinality/page response, nested question projection, Admin permission policy, active physical model, and query/error behavior remain open.
- Current inventory after authoring: 103 catalog IDs; 87 DD folders, 75 full report packages, 16 IDs (#88–#103) without a DD; 12 route-plus-view IDs and 91 without that source pair.
- AC-35 macro-review for #87–#91 remains pending until #88–#91 DDs exist. Continue with #88 in the next DD session.

## GROUP_MACRO_REVIEW — completed after API #91

- Status: VERIFIED_WITH_OPEN_QUESTIONS; document-level review of AC-35 #87–#91 and its AC-16 dependency #29–#32 is complete.
- Shared DERIVED proposal: #90 soft-deletes when attempts exist and retains history; #87 hides tombstones by default; #89 refuses updates to tombstones/history-bearing quizzes; #29 blocks new attempts; #30–#31 may continue an existing attempt; #32 reads retained results; #91 aggregates retained history; hard-delete/no row maps to #91's direct 404.
- Unresolved: tombstone enum/timestamp, no-attempt hard delete, DRAFT-to-open lifecycle, request/response cardinality, nested Quiz schema, metric definitions, Admin policy, in-flight attempt behavior, and transaction/concurrency.
- This supersedes the pending-after-#91 handoff recorded at DD authoring time. It is not owner approval or runtime verification; no application tests were run.
