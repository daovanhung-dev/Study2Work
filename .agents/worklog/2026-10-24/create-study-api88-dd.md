---
task_id: "2026-10-24-create-study-api88-dd"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD Study API #88 — Tạo quiz mới

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-24/create-study-api48-dd.md`
    - carry_forward: Giữ direct contract, source mapping là candidate; ghi rõ enum/schema gap và không tự sửa catalog/runtime.
  - path: `.agents/worklog/2026-10-24/create-study-api49-dd.md`
    - carry_forward: Không biến mô hình V1-PILOT thành schema legacy; phân biệt expected/current và giữ SOURCE_REQUIRED khi thiếu mapping.
  - path: `.agents/worklog/2026-10-24/create-study-api50-dd.md`
    - carry_forward: Khi contract có chuỗi opaque nhưng diagram thiếu cấu trúc, chỉ đưa JSON shape thành proposal DERIVED; giữ transaction và gap persistence rõ ràng.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Tạo một DD tiếng Việt cho API #88 trong phiên này; ghi plan và ma trận trước khi authoring; đọc kỹ diagram AC-35, đối chiếu API #28/#87 và schema artifacts; kiểm tra ngay toàn bộ package sau khi tạo.
- Canonical contract: `docs/lists/list_api.md` row #88 — `POST /api/v1/admin/quizzes`, Bearer JWT, role Admin; body `config:string!`, `questions:string!`; HTTP 201 `DESIGN_RESOURCE_CREATED`, response `ApiEnvelope<Quiz>`, errors chính xác 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 422 `DESIGN_VALIDATION_ERROR`, 500 `DESIGN_INTERNAL_ERROR`.
- Reusable response: `Quiz{id:int64, course_id:int64, title:string, duration_minutes?:int32, passing_score:decimal-string, questions:QuizQuestion[]}`; `QuizQuestion{id:int64, text:string, type:QuestionType, choices:QuizChoice[]}`. `QuizChoice` và `QuestionType` chưa được định nghĩa đầy đủ.
- AC-35: Admin có quiz-management permission; flow đi từ list #87 sang Create #88, “INSERT Quiz + Questions”, rồi hiển thị kết quả. Update #89, delete #90 và statistics #91 là nhánh riêng.
- Output: Markdown DD trong `apps/study-server/docs/dd/88_admin_quizzes_create/`, gồm 7 sheet lõi trước DB mapping, ba mapping sheet cho ba bảng insert candidate, cùng 3 reports; không tạo ZIP.

## CURRENT_BEHAVIOR

- Source/config: Không tìm thấy `/api/v1/admin/quizzes`, API ID #88, module `api_88_*` hoặc test #88 dưới `apps/study-server/app` và `apps/study-server/tests`. Router source hiện có route/view cặp #01–#09, #12–#14; Admin helper chưa có, auth helper chỉ có Student guard. Path chưa nằm trong `DESIGN_CONTRACT_PATHS`.
- Error source: middleware hiện trả `VALIDATION_ERROR`/`INTERNAL_SERVER_ERROR` cho path ngoài allowlist; `error_response` serialize `data=None` thành `{}`. Đây là integration discrepancy có điều kiện, không phải current behavior của route chưa tồn tại.
- Schema artifact: Legacy `DB.sql` và ERD dùng BIGINT `quizzes`, `quiz_questions`, `quiz_choices`; `quiz_questions` không có QuestionType column. DDL nullable một số FK mà DB guide mô tả required. `02_study_db.sql` V1-PILOT dùng UUID `assessments`, UUID `quiz_questions` có `question_type`, và `quiz_options`; không khớp trực tiếp ID/API model. Live schema chưa xác minh.
- Runnable tests: Không có test API #88; application tests không chạy trong task docs-only.

## SOURCE_TRACE

```text
Admin Bearer + quiz-management permission
  -> parse/validate direct string fields (embedded JSON parsing is DERIVED)
  -> validate course reference (candidate)
  -> one transaction: insert quiz -> insert ordered question rows -> insert choice/answer-key rows
  -> assemble ApiEnvelope<Quiz> with generated IDs -> commit and return HTTP 201
```

## PLAN BEFORE DD AUTHORING

1. Giữ nguyên method/path/auth, body field names/types, response type, HTTP 201 và exact error set; không thêm `course_id` hoặc object field ở tầng body, không thêm 404/409.
2. Đọc flow AC-35 đúng ranh giới: #88 là Create sau #87, chỉ `INSERT Quiz + Questions`, rồi hiển thị kết quả. Không gộp update #89, soft delete/attempt policy #90 hoặc statistics #91.
3. Giữ body trực tiếp là hai required string. Đề xuất `config` là JSON text object với `course_id`, `title`, `duration_minutes?`, `passing_score`; `questions` là JSON text array với `text`, `type`, `choices`. Đây là shape DERIVED theo Quiz/QuizQuestion vì catalog không mô tả nội dung hai string.
4. Đề xuất choice input `{text, is_correct}` chỉ như DERIVED candidate: `text` khớp QuizQuestion naming; `is_correct` có physical precedent trong legacy DDL và phục vụ grading. `QuizChoice`, enum values, choice output shape và quy tắc cardinality/correct-answer vẫn SOURCE_REQUIRED. Có thể dùng `SINGLE_CHOICE` làm ví dụ từ pilot constraint nhưng không chốt enum hay map pilot UUID vào legacy.
5. Candidate writes theo legacy schema riêng: `quizzes` map `course_id`, `title→name`, `passing_score`, `duration_minutes→time_limit_minutes`; `quiz_questions` map `text→question_text` và thứ tự mảng→`sort_order`; `quiz_choices` map `text→choice_text`, `is_correct`. Không thêm type column hoặc bảng mới. Ghi discrepancy vì legacy `quiz_questions` thiếu type trong logical response.
6. Candidate kiểm tra course tồn tại trong transaction ngay trước insert; course không tồn tại đề xuất 422 vì catalog không có 404. Không kiểm tra status/owner của course khi không có rule AC-35. Ghi đây là DERIVED và cần chốt.
7. Ghi một transaction atomic cho quiz, questions và choices; lỗi giữa các insert rollback toàn bộ. Candidate ID do BIGSERIAL sinh; legacy `created_at`/`updated_at` NOT NULL phải được set cùng transaction timestamp; status DRAFT, question score 1 là default DDL candidate nếu schema này được chọn.
8. Response chỉ dùng `ApiEnvelope<Quiz>` và logical Quiz fields; không thêm `status`, `description`, `score` hoặc answer key `is_correct` vào response khi contract không khai báo. Ghi full nested response mapping chưa thể chốt cho đến khi QuestionType/QuizChoice được định nghĩa và type được persistence.
9. Tách riêng legacy BIGINT schema và V1-PILOT UUID assessment schema; live DB chưa xác minh. Ghi current Admin guard, middleware allowlist và error-envelope discrepancies có điều kiện.
10. Rà macro boundary với #87–#91: #87 direct response vẫn có list/cardinality conflict; #89 catalog chưa khai báo body dù diagram ghi update quiz/question set; #90 soft delete phụ thuộc attempts; #91 statistics. Không sửa các DD khác; macro-review toàn nhóm chờ đủ #91.
11. Author 10 sheets (`00`–`06`, `07_quizzes_insert`, `08_quiz_questions_insert`, `09_quiz_choices_insert`) + `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md`. Dùng 8 registered template roles; ba mapping sheets reuse template table appendix. Static-check exact 13-file set, template suffixes, direct contract/errors, outer/embedded JSON, field coverage, transaction/mapping tables, relative links, anchors, code fences, whitespace, fingerprints, source boundary và `git diff --check`.
12. Không sửa runtime/schema/catalog/diagram/context pages và không chạy app tests. Giữ trạng thái `Draft — Needs Confirmation` với đề xuất DERIVED tách khỏi contract.

### API Requirement Matrix

| API ID | Contract item | Giá trị | Basis/status |
|---|---|---|---|
| #88 | Method/path | `POST /api/v1/admin/quizzes` | Catalog + AC-35; DIRECT |
| #88 | Actor/auth | Admin, Bearer JWT | Catalog; role DIRECT; permission theo AC-35 |
| #88 | Body | `config:string!`, `questions:string!` | Catalog; DIRECT |
| #88 | Success | HTTP 201 `DESIGN_RESOURCE_CREATED`; `ApiEnvelope<Quiz>` | Catalog; DIRECT |
| #88 | Errors | 401 auth, 403 access, 422 validation, 500 internal | Catalog; exact codes DIRECT |
| #88 | Embedded string schema | JSON config object + JSON question array | DERIVED proposal; not in catalog/diagram |

### Request Usage Matrix

| Request field | Direct type | Proposed use | Validation/status |
|---|---|---|---|
| Authorization | Bearer JWT | Admin + quiz-management gate before DB writes | Role DIRECT; permission/policy source missing |
| `config` | required string | JSON text with `course_id`, `title`, `duration_minutes?`, `passing_score` | JSON/object shape DERIVED; field schema/open |
| `questions` | required string | JSON text array of question inputs | Array/object shape DERIVED; minimum/count/type rules open |
| Nested `text` | proposed string | Question text and choice text | DERIVED mapping to `question_text`/`choice_text` candidates |
| Nested `type` | proposed string | `QuestionType` | Logical field required for response; values/storage unresolved |
| Nested `is_correct` | proposed boolean | Candidate answer-key input to `quiz_choices.is_correct` | DERIVED; not a QuizChoice contract field |

### Query Matrix

| Query/read | Source/columns | Purpose | Status |
|---|---|---|---|
| Q0 | Candidate `courses.id` by `config.course_id` | Check requested course exists before writes so invalid reference maps to 422 | DERIVED; no 404 code; no status/owner filter |
| Q1 | `quizzes` generated id | Parent insert and response `data.id` | Legacy BIGINT candidate only |
| Q2 | `quiz_questions` generated ids, question text/order | Child insert and `QuizQuestion` candidate response | Legacy type column missing; response gap |
| Q3 | `quiz_choices` generated ids, text/correct flag | Child insert and grading data | Choice order/schema unresolved; candidate only |

### Mutation Matrix

| Mutation | Table | Candidate fields | Order/transaction | Status |
|---|---|---|---|---|
| M1 | `quizzes` | course_id, name, passing_score, time_limit_minutes, created_at, updated_at | First; parent ID feeds children | Legacy candidate; status default DRAFT; timestamps required |
| M2 | `quiz_questions` | quiz_id, question_text, sort_order; type absent | Per input array order; same transaction | Legacy candidate; no QuestionType mapping |
| M3 | `quiz_choices` | question_id, choice_text, is_correct | Per nested input order; same transaction | Legacy candidate; choice order absent |

### Response Source Matrix

| Response field | Candidate source | Status |
|---|---|---|
| Envelope/business code/trace | Reusable `ApiEnvelope<Quiz>` + catalog | DIRECT shape; current error serialization discrepancy |
| `data.id` | `quizzes.id` generated BIGSERIAL | Candidate mapping |
| `data.course_id` | parsed `config.course_id` / stored row | DERIVED embedded key; candidate physical mapping |
| `data.title` | parsed `config.title` → `quizzes.name` | DERIVED alias |
| `data.duration_minutes` | parsed config → `time_limit_minutes` | Optional; null/omit unresolved |
| `data.passing_score` | parsed config → `passing_score` | Decimal-string precision policy open |
| `data.questions[]` | inserted question rows plus input order | Required by Quiz schema; nested projection DERIVED |
| `data.questions[].type` | no legacy column; pilot UUID model has `question_type` | SOURCE_REQUIRED / DISCREPANCY |
| `data.questions[].choices[]` | `quiz_choices` candidate | QuizChoice logical/output shape SOURCE_REQUIRED; do not expose `is_correct` by assumption |

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Embedded JSON contract | Catalog only says required strings; no nested schema in AC-35 | DERIVED / SOURCE_REQUIRED | Body structure remains proposal |
| Question type | Logical QuizQuestion requires type; legacy quiz_questions has no type; pilot type belongs to UUID model | DISCREPANCY | Cannot map complete response using selected legacy candidate without schema decision |
| QuizChoice | Reusable schema absent; legacy has choice_text/is_correct; pilot options differ | SOURCE_REQUIRED / DISCREPANCY | Input answer-key and output fields need confirmation |
| Persistence model | Contract int64 + legacy BIGINT vs pilot UUID/versioned model | DISCREPANCY / NOT_VERIFIED | Never combine table models; live schema unknown |
| Course reference | Body hides course_id inside proposed config; catalog has 422 but no 404 | DERIVED | Candidate course existence → 422; confirm semantics |
| Admin policy/wiring | AC-35 permission; runtime Student-only guard and absent Admin route | SOURCE_REQUIRED / UNWIRED | No runtime behavior claim |
| Middleware/error envelope | Path absent allowlist; current error helper uses `{}` for null data | DISCREPANCY / CONDITIONAL_FUTURE_WIRING | Future integration must align catalog/guidelines |
| Cross-API consistency | #87 list response mismatch; #89 request body absent in catalog; #90/#91 depend on same Quiz model | OPEN | Preserve direct contracts; macro-review after #91 |

## CHANGES

- Files changed: `apps/study-server/docs/dd/88_admin_quizzes_create/` (10 sheets + 3 reports), this task worklog, and `.agents/worklog/2026-10-24/inventory-study-api-dd-counts.md` for the requested current totals.
- CONTEXT_UPDATES: None planned; no runtime/schema/catalog/diagram changes.
- Context pages changed: None.
- Assumptions: Only embedded JSON shape, nested create fields, course validation and insertion ordering are DERIVED proposals; direct API contract remains unchanged.

## PLAN REFINEMENT DURING REVIEW

- Q0 course-existence read được đặt trong cùng transaction với M1/M2/M3 và ngay trước parent insert. Lý do: tránh khoảng hở do precheck ngoài transaction; live FK/DB isolation vẫn chưa xác minh.

## VERIFICATION

| Check | Result | Status |
|---|---|---|
| Package manifest | Exact 13 Markdown files: 10 sheets + 3 reports | VERIFIED_STATIC_ONLY |
| Template appendix parity | 10/10 appendix suffixes byte-identical to registered templates | PASS — STATIC |
| Catalog contract | Direct #88 endpoint, required string fields, envelope/status and exact four catalog error codes retained | PASS — STATIC |
| JSON examples | Four fenced JSON blocks parsed; embedded config object and questions array decoded | PASS — STATIC |
| Tables and fences | 45 Markdown tables / 544 lines have consistent widths; four fence pairs balanced | PASS — STATIC |
| Links and anchors | 39 local links and 19 anchors resolved | PASS — STATIC |
| Whitespace | UTF-8 files end with newline; no trailing whitespace | PASS — STATIC |
| Source scan | No API #88 route/module/test marker under Study app/tests | VERIFIED_ABSENT |
| DD payload fingerprint | `c968202b7c1ecdbc658a83dc1ec5e3a85c2cbe6f268f9c907f3c2fc434803814` over 10 sheets + PLAN_RESULT + OPEN_QUESTIONS | RECORDED |
| Application tests/runtime | Not run; docs-only task and API #88 route is absent | NOT_RUN |
| Context validator | No `.agents/` context page or manifest changed | NOT_APPLICABLE |

## HANDOFF

- DD status: `Draft — Needs Confirmation`; embedded JSON shape, QuestionType persistence, QuizChoice shape, Admin policy, physical schema and error integration need owner/source confirmation.
- Next action: create API #89 DD in the next session. AC-35 macro-review for #87–#91 remains pending until #91 DD exists.
- Runtime/source boundary: #88 remains unwired; static DD validation does not establish runtime behavior.

## GROUP_MACRO_REVIEW — completed after API #91

- Status: VERIFIED_WITH_OPEN_QUESTIONS; document-level review of AC-35 #87–#91 and its AC-16 dependency #29–#32 is complete.
- Shared DERIVED proposal: #90 soft-deletes when attempts exist and retains history; #87 hides tombstones by default; #89 refuses updates to tombstones/history-bearing quizzes; #29 blocks new attempts; #30–#31 may continue an existing attempt; #32 reads retained results; #91 aggregates retained history; hard-delete/no row maps to #91's direct 404.
- Unresolved: tombstone enum/timestamp, no-attempt hard delete, DRAFT-to-open lifecycle, request/response cardinality, nested Quiz schema, metric definitions, Admin policy, in-flight attempt behavior, and transaction/concurrency.
- This supersedes the pending-after-#91 handoff recorded at DD authoring time. It is not owner approval or runtime verification; no application tests were run.
