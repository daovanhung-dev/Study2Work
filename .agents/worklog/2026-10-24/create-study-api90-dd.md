---
task_id: "2026-10-24-create-study-api90-dd"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD Study API #90 — Xóa quiz

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-24/create-study-api48-dd.md`
    - carry_forward: Giữ contract catalog; tách `DERIVED` khỏi source đã xác minh; không tự thêm bảng, field hay policy khi schema/runtime thiếu.
  - path: `.agents/worklog/2026-10-24/create-study-api49-dd.md`
    - carry_forward: Tôn trọng AC/API boundary; ghi rõ nguồn persistence, identity, quyền và response còn `SOURCE_REQUIRED` thay vì biến thành executable fact.
  - path: `.agents/worklog/2026-10-24/create-study-api50-dd.md`
    - carry_forward: Giữ API liên kết theo flow, trạng thái/moderation cần căn AC liên quan; ghi exact success/error codes và giới hạn source evidence.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Tạo đúng một Markdown DD tiếng Việt cho API #90; lập plan trước authoring; đọc kỹ AC-35 diagram và DD #87–#89; kiểm tra ngay sau authoring, ghi rõ phần cần xác nhận.
- Canonical contract: Catalog row #90 — `DELETE /api/v1/admin/quizzes/{quiz_id}`, Bearer JWT, role Admin, `path{quiz_id:int64!}`, response `ApiEnvelope<DeleteResult>`, HTTP 200 `DESIGN_RESOURCE_DELETED`; lỗi đúng 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 422 `DESIGN_VALIDATION_ERROR`, 500 `DESIGN_INTERNAL_ERROR`. Marked Conditional; không có body/query được khai báo.
- AC-35 relation: Catalog mô tả “kiểm tra attempts”; chi tiết behavior/persistence phải xác minh diagram, schema artifacts và API #87–#89 trước khi đề xuất.

## CURRENT_BEHAVIOR

- Source/config: Không có route `/api/v1/admin/quizzes/{quiz_id}`, module `api_90_*`, hoặc test API #90 trong `apps/study-server/app`, `apps/study-server/tests`. Router hiện chỉ import các module guest API #01–#09, #12–#14. Auth helper có guard Student, chưa có Admin/quiz-management guard. `DESIGN_CONTRACT_PATHS` là các exact path public/auth hiện tại, không có path Admin quiz; handler lỗi framework vì vậy sẽ chọn fallback `VALIDATION_ERROR`/`INTERNAL_SERVER_ERROR` nếu route được wire mà không cập nhật.
- Database artifacts: Legacy `DB.sql` có `quizzes.status VARCHAR(20)` và quan hệ `quiz_questions.quiz_id`, `quiz_choices.question_id`, `quiz_attempts.quiz_id`, `quiz_answers.attempt_id/question_id/choice_id`; không khai báo `ON DELETE` cascade, `deleted_at`, hay enum status. `DB_UNICA_TABLES.md` gọi các quan hệ attempt/answer là historical candidate. V1-PILOT dùng UUID `assessments`/`quiz_questions`/`quiz_options`/`assessment_attempts`, FK `ON DELETE RESTRICT`; không tương thích trực tiếp với catalog int64. Live schema chưa xác minh.
- Related flows: AC-16 #29 tạo attempt `IN_PROGRESS`; #30–#32 lưu/nộp/đọc answer và kết quả. API #29 DD chưa chốt predicate quiz-open/status, identity, transaction hoặc concurrency.
- Runnable tests: Không có test API #90; không chạy application tests, docs-only.
- Runtime wiring: `UNWIRED / NOT_FOUND`; source inventory hiện tại không chứng minh runtime behavior cho #90.

## SOURCE_TRACE

```text
Admin Bearer + quiz-management permission -> path quiz_id -> load quiz -> EXISTS attempt (all states) -> if yes: soft-delete quiz and retain questions/choices/attempts/answers; if no: candidate delete choices -> questions -> quiz in one transaction -> map DeleteResult -> HTTP 200/catalog error -> AC-35 shows operation result
```

`EXISTS` and AC-35 soft-delete branch are source-backed design intent; the hard-delete no-attempt branch, tombstone persistence, timestamp source and cross-request concurrency are DERIVED/SOURCE_REQUIRED. Current runtime has no API #90 route.

## PLAN BEFORE DD AUTHORING — REFINED AFTER SOURCE REVIEW

1. Giữ trực tiếp catalog: `DELETE /api/v1/admin/quizzes/{quiz_id}`, Admin Bearer, path `quiz_id:int64!`, không body/query, `ApiEnvelope<DeleteResult>`, HTTP 200 `DESIGN_RESOURCE_DELETED` và đúng 5 lỗi 401/403/404/422/500; không thêm code/status.
2. Bám AC-35 branch #90: kiểm tra attempts; nếu có attempt thì soft delete (DIRECT từ diagram) và giữ nguyên quiz questions/choices cùng attempt/answers để #30–#32 và #91 không mất lịch sử.
3. Nếu không có attempt, đề xuất hard delete (DERIVED) theo thứ tự `quiz_choices` → `quiz_questions` → `quizzes`, vì legacy DDL thể hiện FK chain nhưng không khai báo cascade. Chỉ dùng legacy BIGINT làm candidate; V1-PILOT UUID/RESTRICT là model riêng.
4. Không phát minh cột tombstone: đề xuất `quizzes.status='DELETED'` chỉ là DERIVED dùng cột `status` có sẵn; enum/value chưa có source. Đề xuất DELETE lặp lại trên tombstone là no-op 200 giữ `updated_at`; cần xác nhận. `deleted_at` bắt buộc trong DeleteResult nhưng không tồn tại trong legacy `quizzes`; timestamp mapping/timezone cần xác nhận.
5. Tạo Request Usage, Query, Mutation, Response Source matrices trước authoring: Q1 locate quiz, Q2 `EXISTS quiz_attempts` (không lọc trạng thái); M1 soft update parent khi có attempt; M2–M4 hard delete children/parent khi không có attempt; response id/status constant/deletion timestamp.
6. Ghi rủi ro concurrency với API #29: DELETE check và attempt INSERT phải phối hợp; API #29 chưa chốt quiz-open predicate, deleted-status handling, transaction/lock. Không tự thêm 409 vì catalog #90 không có.
7. Dùng 8 template registered và tạo mapping sheet riêng cho mỗi thao tác mutation (1 UPDATE, 3 DELETE), cùng `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md`. Markdown-only theo Study workflow; không sửa API #87–#89 trong lượt này, đánh dấu AC-35 macro-review chờ #91.
8. Static-check exact file set/template appendix, catalog/error set, AC-35 nodes/edges, field/column/operation coverage, examples, links/anchors, table widths, fences, whitespace, fingerprint và source absence; không chạy application tests.

### API Requirement Matrix

| API ID | Contract item | Giá trị | Basis/status |
|---|---|---|---|
| #90 | Method/path | `DELETE /api/v1/admin/quizzes/{quiz_id}` | Catalog + AC-35; DIRECT |
| #90 | Actor/auth | Admin; Bearer JWT; quiz management permission | Catalog + AC-35; role/permission intent DIRECT, runtime guard SOURCE_REQUIRED |
| #90 | Path | `quiz_id:int64!` | Catalog; DIRECT |
| #90 | Body/query | Không khai báo | Catalog; DIRECT absence |
| #90 | Success | HTTP 200 `DESIGN_RESOURCE_DELETED`; `ApiEnvelope<DeleteResult>` | Catalog; DIRECT |
| #90 | Errors | 401 auth, 403 access, 404 not found, 422 validation, 500 internal | Catalog; exact codes DIRECT |
| #90 | Attempt policy | Có attempts → soft delete | AC-35 node n10; DIRECT intent, physical mapping SOURCE_REQUIRED |
| #90 | No-attempt branch | Hard delete choices → questions → quiz | DERIVED from delete intent + legacy FK order; requires confirmation |

### Request Usage Matrix

| Request item | Type/source | Use | Validation/branch | Status |
|---|---|---|---|---|
| Authorization | Bearer JWT | Admin + quiz-management authorization | Before existence/history reads | Contract DIRECT; current Admin guard missing |
| `quiz_id` | required int64 path | Q1 target lookup | Missing row → catalog 404; exact malformed/positive rules unspecified | Type DIRECT; details SOURCE_REQUIRED |
| Body/query | None | None | Do not add fields | DIRECT absence |

### Query Matrix

| Query | Candidate operation/source | Predicate | Purpose | Status |
|---|---|---|---|---|
| Q1 | SELECT `quizzes` | `id = :quiz_id` | Locate target and read candidate `status` | Legacy BIGINT candidate; live schema unverified |
| Q2 | EXISTS `quiz_attempts` | `quiz_id = :quiz_id`, any status | Choose AC-35 soft-delete branch | Diagram DIRECT; legacy relation candidate; transaction/race policy open |
| Q3 | N/A before hard-delete branch | Child relationship through `quiz_questions.quiz_id` | Target choices/questions for ordered physical delete | DERIVED legacy relation; only when Q2 is false |

### Mutation Matrix

| Mutation | Target | Condition | Operation/fields | Mapping file | Status |
|---|---|---|---|---|---|
| M1 | `quizzes` | Q2 true and not already tombstoned | UPDATE candidate `status='DELETED'`, preserve timestamp on repeat | `07_quizzes_soft_delete.md` | Logical branch DIRECT; state/idempotency DERIVED; no `deleted_at` column |
| M2 | `quiz_choices` | Q2 false | DELETE choices joined through questions where `quiz_id=:quiz_id` | `08_quiz_choices_delete.md` | DERIVED; explicit order because no cascade declared |
| M3 | `quiz_questions` | Q2 false | DELETE where `quiz_id=:quiz_id` | `09_quiz_questions_delete.md` | DERIVED; preserve if attempts exist |
| M4 | `quizzes` | Q2 false | DELETE where `id=:quiz_id` | `10_quizzes_delete.md` | DERIVED; transaction and live FK constraints open |

### Response Source Matrix

| Field | Contract type | Candidate source/value | Status |
|---|---|---|---|
| `data.id` | int64 | Q1 target `quizzes.id` | Candidate BIGINT mapping |
| `data.status` | literal `deleted` | Fixed result literal | DIRECT reusable schema |
| `data.deleted_at` | date-time | Deletion time at successful mutation | Required logical field; generator/UTC/persistence SOURCE_REQUIRED |
| Envelope fields | ApiEnvelope | Shared Study envelope convention | Contract shape DIRECT; current error `data` differs from guideline |

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #90 source/wiring | Pending focused current source scan | `PENDING_VERIFICATION` | Do not claim route/runtime presence yet. |
| Delete and attempt policy | Catalog says check attempts; detail pending AC-35/schema inspection | `PENDING_SOURCE_REVIEW` | Do not choose physical deletion/cascade/soft-delete before evidence review. |
| Request contract | Catalog row #90 is path-only | `DIRECT` | Do not add body/query fields. |

## CHANGES

- Files changed: 14 Markdown files under `apps/study-server/docs/dd/90_admin_quizzes_delete/`, this task worklog, and `.agents/worklog/2026-10-24/inventory-study-api-dd-counts.md`.
- CONTEXT_UPDATES: None; no runtime source, schema, catalog, diagram, context page or API #87–#89 DD changed.
- Context pages changed: None; context validator not applicable.
- Assumptions: Exact catalog behavior remains authoritative; no-attempt hard delete, `DELETED` tombstone, timestamp mapping and repeated soft-delete no-op remain explicitly `DERIVED` proposals.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Worklog preflight | Selector returned #48/#49/#50; all three read in full. | `VERIFIED` |
| AC-35 diagram | Parsed full AC-35 page; #90 DELETE → “Soft delete nếu đã có attempts” → show result; Create/Update/Statistics branches remain separate. | `VERIFIED_STATIC_ONLY` |
| AC-16/attempt history | Read AC-16 diagram and DD #29–#32; #29 inserts IN_PROGRESS, #30–#32 read/write answer/history; open status/concurrency remains. | `VERIFIED_STATIC_ONLY` |
| Catalog/DDL/prior DD | Read API #90 exact row, DeleteResult, legacy and pilot schemas, DB guide, #87–#89, #86 and relevant attempt DDs. | `VERIFIED_STATIC_ONLY` |
| Current source scan | No API #90 route/module/test; Admin guard absent, middleware exact path set omits Admin quiz, error helper returns `{}` for absent data. | `VERIFIED_STATIC_ONLY` |
| Template/source archive | Registry wires createDD-markdown; 8 templates present, archive scan under Study docs/skill resources found 0 in-scope archives. | `VERIFIED_STATIC_ONLY` |
| API #90 DD static checks | Exact 14-file manifest; 11/11 template appendix parity; exact catalog contract; 2 JSON blocks; 34 tables / 407 data rows; 4 fence pairs; 37 local links / 12 anchors; whitespace/source boundary pass. Fingerprints recorded in report. | `VERIFIED` |
| Application tests | Not run; docs-only and API #90 remains unwired. | `NOT_RUN` |
| Context validator | Not run; no context page or manifest changed. | `NOT_APPLICABLE` |

## HANDOFF

- Remaining open questions: Approve `status='DELETED'`/`updated_at` timestamp mapping, no-attempt hard delete, repeated-delete behavior, Admin permission source, and concurrency coordination with API #29; keep DD `Draft — Needs Confirmation`.
- Inventory after #90: 90/103 APIs have DD folders; 13 (#91–#103) do not. 12/103 are source-wired by router-plus-view criterion; 91 lack that pair. No application tests were run.
- Next owner/action: Create API #91 DD, then macro-review AC-35 group #87–#91 and reconcile #87–#90 visibility/lifecycle with statistics.

## GROUP_MACRO_REVIEW — completed after API #91

- Status: VERIFIED_WITH_OPEN_QUESTIONS; document-level review of AC-35 #87–#91 and its AC-16 dependency #29–#32 is complete.
- Shared DERIVED proposal: #90 soft-deletes when attempts exist and retains history; #87 hides tombstones by default; #89 refuses updates to tombstones/history-bearing quizzes; #29 blocks new attempts; #30–#31 may continue an existing attempt; #32 reads retained results; #91 aggregates retained history; hard-delete/no row maps to #91's direct 404.
- Unresolved: tombstone enum/timestamp, no-attempt hard delete, DRAFT-to-open lifecycle, request/response cardinality, nested Quiz schema, metric definitions, Admin policy, in-flight attempt behavior, and transaction/concurrency.
- This supersedes the pending-after-#91 handoff recorded at DD authoring time. It is not owner approval or runtime verification; no application tests were run.
