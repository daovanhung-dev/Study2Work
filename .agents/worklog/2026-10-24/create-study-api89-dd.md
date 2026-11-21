---
task_id: "2026-10-24-create-study-api89-dd"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD Study API #89

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-24/create-study-api48-dd.md`
    - carry_forward: Tách contract khỏi current source; chỉ dùng `DERIVED` khi diagram/schema không quyết định; giữ discrepancy và runtime boundary rõ.
  - path: `.agents/worklog/2026-10-24/create-study-api49-dd.md`
    - carry_forward: Giữ miền Quiz riêng khỏi Content; đọc diagram theo flow, không mở rộng contract bằng response/persistence giả định.
  - path: `.agents/worklog/2026-10-24/create-study-api50-dd.md`
    - carry_forward: Không invent physical schema/field/business code; giữ các suy diễn đơn giản ở trạng thái proposal cần xác nhận.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Tạo đúng một DD Markdown tiếng Việt cho API #89 trong phiên này; lập plan và ma trận trước khi authoring; đọc kỹ AC-35 và DD Quiz liên quan; static-check ngay sau khi tạo.
- Canonical contract: `docs/lists/list_api.md` row #89 đánh dấu Conditional; `PUT /api/v1/admin/quizzes/{quiz_id}`, Bearer JWT, role Admin, `path{quiz_id:int64!}`, `ApiEnvelope<Quiz>`, HTTP 200 `DESIGN_RESOURCE_UPDATED`, lỗi đúng 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 422 `DESIGN_VALIDATION_ERROR`, 500 `DESIGN_INTERNAL_ERROR`. Catalog không khai báo query hoặc body field.
- AC-35: Actor Admin có quiz-management permission; flow từ decision Update gọi #89, node backend ghi `UPDATE quiz/question set`, sau đó hiển thị kết quả. Nhánh #88 create, #90 delete và #91 statistics là riêng.
- Reusable response: `Quiz{id:int64, course_id:int64, title:string, duration_minutes?:int32, passing_score:decimal-string, questions:QuizQuestion[]}`; `QuizQuestion{id:int64, text:string, type:QuestionType, choices:QuizChoice[]}`. `QuizChoice` và `QuestionType` chưa định nghĩa đủ.
- Body proposal để review: reuse `config:string` và `questions:string` từ #88 làm DERIVED candidate vì #89 là PUT cập nhật chính Quiz/question set; không coi là direct contract.

## CURRENT_BEHAVIOR

- Source/config: Không có route/API #89, module `api_89_*`, path `/api/v1/admin/quizzes/{quiz_id}` hoặc test tương ứng trong Study app/tests. Router API markers hiện là #01–#09 và #12–#14. Current auth helper chỉ có Student guard; Admin guard/policy chưa có. Path Admin quiz không có trong `DESIGN_CONTRACT_PATHS`; framework validation/unhandled errors cho future wiring có thể dùng fallback business code. `error_response(data=None)` serialize `data` thành `{}`, còn API Guidelines quy định error `data:null`.
- Schema: Legacy `DB.sql` dùng BIGINT/BIGSERIAL `quizzes`, `quiz_questions`, `quiz_choices`; `quiz_questions` thiếu QuestionType, `quiz_choices` thiếu order. `quiz_attempts` và `quiz_answers` tham chiếu quiz/question/choice nên thay toàn bộ child rows có nguy cơ làm hỏng lịch sử. DB guide/ERD mô tả các relation; live schema chưa xác minh. V1-PILOT dùng UUID assessment/question/options và không khớp trực tiếp API int64; không ghép hai mô hình.
- Related DD: #87 ghi direct response `ApiEnvelope<Quiz>` dù list intent khác; #88 có direct create body `config:string!`, `questions:string!` nhưng embedded JSON là DERIVED và persistence gaps còn mở; #28 không trả `is_correct` cho Student. #84 là precedent PUT path-only với body proposal tách khỏi contract.
- Runnable tests: Không có test API #89; không chạy application tests trong task docs-only.
- Runtime wiring: `UNWIRED / NOT_FOUND`; source scan không xác nhận runtime behavior cho API #89.

## SOURCE_TRACE

```text
Admin Bearer + quiz-management permission -> path quiz_id + body candidate (config/questions tái sử dụng từ #88, DERIVED) -> đọc quiz -> kiểm tra attempt/history trước khi thay question set -> một transaction cập nhật quizzes và thay child set theo candidate -> dựng ApiEnvelope<Quiz> -> trả 200 hoặc catalog errors
```

## PLAN BEFORE DD AUTHORING

1. Giữ method/path/auth/path `quiz_id:int64!`, response `ApiEnvelope<Quiz>`, HTTP 200 `DESIGN_RESOURCE_UPDATED` và exact 5 error codes; không thêm 409 hoặc business code.
2. Bám AC-35 branch UPDATE: backend cập nhật quiz/question set, rồi UI hiển thị kết quả. Không gộp Create #88, Delete #90/attempt policy hoặc Statistics #91.
3. Giữ direct catalog là path-only. Đề xuất body full replacement dùng lại hai string `config` và `questions` của #88, cùng embedded JSON shape của #88, chỉ là `DERIVED` để cụ thể hóa update; ghi rõ chưa được duyệt.
4. Candidate `config`: `course_id`, `title`, `duration_minutes?`, `passing_score`; candidate `questions[]`: `text`, `type`, `choices[{text,is_correct}]`. Không thêm `status`, `description`, question score hoặc fields khác. Omission/null semantics và khả năng đổi course cần xác nhận.
5. Candidate parent mutation: update legacy `quizzes` metadata; giữ `status` nguyên trạng vì API #89 body candidate không có status và API #90/#91 không quyết định lifecycle.
6. Vì body candidate không có child IDs, đề xuất thay toàn bộ question/choice set atomically. Trước delete, kiểm tra attempts/answer references; candidate 422 nếu có history để không xóa dữ liệu được API #29–#32 tham chiếu. Đây là policy `DERIVED`, cần owner review; không claim race-safe/live-schema verified.
7. Lập 5 mapping sheets tách `quizzes UPDATE`, `quiz_choices DELETE`, `quiz_questions DELETE`, `quiz_questions INSERT`, `quiz_choices INSERT`; mỗi write có Data Mapping step link. Không thêm cột QuestionType/order vào schema.
8. Response map theo Quiz logical schema; không trả answer key `is_correct`; `QuestionType` persistence và QuizChoice output vẫn `SOURCE_REQUIRED`, nên giữ `Draft — Needs Confirmation`.
9. Dùng 8 registered sheet templates; verify template pack fingerprint `3dc7fd2242dd1ed1bd9faba50aadad913a31b97ebf1392d6144bb905c5208137`. Study workflow giao Markdown, không tạo ZIP. Không sửa source/schema/catalog/diagram/context.
10. Static-check exact file set, template appendix parity, direct contract, DERIVED body JSON, nested examples, field coverage, mapping tables, links/anchors, table widths, fences, whitespace, fingerprint và source boundary. Không chạy app tests.
11. AC-35 macro-review #87–#91 tiếp tục pending đến sau DD #91; trong DD #89 chỉ cross-reference các discrepancy đã biết.

### API Requirement Matrix

| API ID | Contract item | Giá trị | Basis/status |
|---|---|---|---|
| #89 | Method/path | `PUT /api/v1/admin/quizzes/{quiz_id}` | Catalog + AC-35; DIRECT |
| #89 | Actor/auth | Admin, Bearer JWT | Catalog; role DIRECT, permission theo AC-35 |
| #89 | Path | `quiz_id:int64!` | Catalog; DIRECT |
| #89 | Body/query | Catalog ghi path; không khai báo body/query | DIRECT absence; update body gap |
| #89 | Success | HTTP 200 `DESIGN_RESOURCE_UPDATED`; `ApiEnvelope<Quiz>` | Catalog; DIRECT |
| #89 | Errors | 401 auth, 403 access, 404 not found, 422 validation, 500 internal | Catalog; exact codes DIRECT |
| #89 | Update body | `config:string`, `questions:string` candidate | DERIVED reuse từ API #88; chưa được duyệt |

### Request Usage Matrix

| Item | Direct/proposed type | Purpose | Validation/use | Status |
|---|---|---|---|---|
| Authorization | Bearer JWT | Admin + quiz-management gate | Before reads/writes | Role DIRECT; policy SOURCE_REQUIRED |
| `quiz_id` | required int64 path | Select target quiz | Existing quiz → 404 candidate mapping | Type DIRECT; positivity/parsing open |
| `config` | candidate string | Quiz metadata replacement | Parse JSON using #88 proposal | DERIVED; absent from #89 catalog |
| `questions` | candidate string | Full question-set replacement | Parse JSON array using #88 proposal | DERIVED; child-ID/replacement policy open |
| Query | None declared | None | Do not add | DIRECT |

### Query Matrix

| Query | Candidate source | Purpose | Predicate/columns | Status |
|---|---|---|---|---|
| Q1 | legacy `quizzes` | Load target | `id = :quiz_id`; metadata for response/update | DERIVED mapping; schema candidate |
| Q2 | legacy `quiz_attempts` | Protect active/historical work before child replacement | existence by `quiz_id` | DERIVED safety proposal; policy/concurrency open |
| Q3 | legacy `quiz_answers` joined through target questions | Detect direct child references before delete | question/choice IDs belonging to quiz | DERIVED safety proposal; exact constraints/live schema open |

### Mutation Matrix

| Mutation | Candidate target | Candidate action | Transaction/order | Status |
|---|---|---|---|---|
| M1 | `quizzes` | UPDATE config fields; preserve `status` | Same transaction as child-set change | DERIVED; legacy candidate |
| M2 | `quiz_choices` | DELETE old choices for target question set | Before question delete; only if safety checks pass | DERIVED replacement strategy |
| M3 | `quiz_questions` | DELETE old questions for target quiz | After choices; only if safety checks pass | DERIVED replacement strategy |
| M4 | `quiz_questions` | INSERT replacement question rows | After deletes; array order candidate for `sort_order` | DERIVED; type column absent |
| M5 | `quiz_choices` | INSERT replacement choices | Per new question; order column absent | DERIVED; answer-key input candidate |

### Response Source Matrix

| Response field | Candidate source | Status |
|---|---|---|
| Envelope/code/trace | Catalog `ApiEnvelope<Quiz>` + current envelope convention | Contract shape DIRECT; runtime absent |
| `data.id` | loaded `quizzes.id` | Candidate BIGSERIAL/BIGINT mapping |
| `data.course_id` | proposed `config.course_id` / updated row | DERIVED key; nullability discrepancy |
| `data.title` | proposed `config.title` → `quizzes.name` | DERIVED alias |
| `data.duration_minutes` | config → `time_limit_minutes` | DERIVED; null/omit open |
| `data.passing_score` | config → `passing_score` | Candidate decimal serialization/scale open |
| `data.questions[]` | inserted replacement rows | Required logical field; response projection DERIVED |
| `data.questions[].type` | no legacy column | SOURCE_REQUIRED / DISCREPANCY |
| `data.questions[].choices[]` | candidate `quiz_choices` rows | QuizChoice shape SOURCE_REQUIRED; omit `is_correct` unless approved |

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Request body | Catalog row #89 contains only path; AC-35 says update quiz/question set; #88 has config/questions create contract | `DISCREPANCY / DERIVED` | Reused body proposal is not direct contract; keep open and Draft. |
| Child replacement/history | Legacy `quiz_answers` references quiz questions/choices; attempts point to quizzes | `DERIVED / SOURCE_REQUIRED` | Full replacement can invalidate attempt history; candidate history guard needs owner/concurrency review. |
| QuestionType/QuizChoice | Reusable Quiz response requires both; legacy question type and choice order are missing | `DISCREPANCY / SOURCE_REQUIRED` | Cannot claim complete response persistence mapping. |
| Physical schema | Legacy BIGINT candidate versus V1-PILOT UUID assessment model; live DB unverified | `DISCREPANCY / NOT_VERIFIED` | Keep models separate; no runtime schema claim. |
| Admin access/error wiring | AC-35 permission; current helper Student-only; Admin path absent allowlist | `SOURCE_REQUIRED / CONDITIONAL_FUTURE_WIRING` | DD is design-only; future integration must implement Admin policy and catalog errors. |

## CHANGES

- Files changed: 15 Markdown files under `apps/study-server/docs/dd/89_admin_quizzes_update/`, this task worklog, and the API DD inventory worklog.
- CONTEXT_UPDATES: None; no source/schema/catalog/diagram/context page changed.
- Context pages changed: None.
- Assumptions: Exact catalog contract is preserved; inferred update-body and replacement behavior remains `DERIVED` and unapproved.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Worklog preflight | Selector returned #48/#49/#50; all three read in full. | `VERIFIED` |
| API #89 DD checks | Package, template parity, contract, JSON, table/fence, links/anchors, whitespace and source-boundary checks pass; see `VERIFICATION_REPORT.md`. | `VERIFIED` |

## HANDOFF

- Remaining open questions: Update body and full child-set replacement are DERIVED proposals; history guard/concurrency, QuestionType/QuizChoice persistence, live schema and Admin guard need owner/source confirmation. DD remains `Draft — Needs Confirmation`.
- Next owner/action: API #90 is next; complete AC-35 macro-review after #91 DD exists.
- Inventory after #89: 89/103 APIs have DD folders; 14 (#90–#103) do not. 12/103 are source-wired by the router-plus-view criterion; 91 lack that pair. No application tests were run.

## GROUP_MACRO_REVIEW — completed after API #91

- Status: VERIFIED_WITH_OPEN_QUESTIONS; document-level review of AC-35 #87–#91 and its AC-16 dependency #29–#32 is complete.
- Shared DERIVED proposal: #90 soft-deletes when attempts exist and retains history; #87 hides tombstones by default; #89 refuses updates to tombstones/history-bearing quizzes; #29 blocks new attempts; #30–#31 may continue an existing attempt; #32 reads retained results; #91 aggregates retained history; hard-delete/no row maps to #91's direct 404.
- Unresolved: tombstone enum/timestamp, no-attempt hard delete, DRAFT-to-open lifecycle, request/response cardinality, nested Quiz schema, metric definitions, Admin policy, in-flight attempt behavior, and transaction/concurrency.
- This supersedes the pending-after-#91 handoff recorded at DD authoring time. It is not owner approval or runtime verification; no application tests were run.
