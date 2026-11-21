---
title: "Overview"
order: 2
dd_id: "87"
api_name: "Lấy danh sách quiz"
source_sheet: "Overview"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | #87 |
| Module | ADMIN / SYSTEM MANAGEMENT — AC-35 |
| Method | GET |
| Endpoint | /api/v1/admin/quizzes |
| Purpose | Admin tra cứu quiz để chọn thao tác Create, Update, Delete hoặc Statistics theo AC-35. |
| Consumer/Actor | Admin có quiz-management permission |
| Authentication | Bearer JWT |
| Authorization | Runtime dùng shared `ADMIN` role guard trước query/DB; permission quiz-management riêng của AC-35 chưa có policy source. |
| Basis | Method/path/query/200/direct `ApiEnvelope<Quiz>`/401/403/500 DIRECT; `Page<Quiz>`, page defaults, metadata-only projection, tombstone filter và query-validation 422 là local DERIVED behavior. |
| Status | Draft — Needs Confirmation |
| Current implementation | WIRED locally: route, Admin module, middleware path and 20 focused HTTP tests are present. Tests use fake DB sessions; live database remains unverified. |
| Transaction | N/A — GET chỉ đọc. |
| Side effects | Không ghi dữ liệu. Thao tác tạo/sửa/xóa/thống kê thuộc #88–#91. |

## Sources

- [API catalog và reusable schemas](../../../../../docs/lists/list_api.md) — row #87, Quiz, QuizQuestion, ApiEnvelope, Page và business codes.
- [AC/API index, AC-35](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — actor, permission, postcondition và nhóm #87–#91.
- [AC-35 activity diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — mở trang, query quizzes, sau đó chọn Create/Update/Delete/Statistics.
- [DB table design](../../diagrams/DB_UNICA_TABLES.md) và [DB ERD](../../diagrams/DB_UNICA_ERD.drawio) — legacy candidate quiz/question/choice columns; không chứng minh live schema.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — candidate BIGINT tables quizzes, quiz_questions, quiz_choices.
- [V1-PILOT Study DDL](../../../../../infra/postgres/02_study_db.sql) — mô hình UUID assessments/quiz_questions/quiz_options khác contract; không map ngầm.
- [API #28 Quiz detail DD](../28_quizzes_detail/02_Overview.md) và [response mapping](../28_quizzes_detail/04_Response.md) — precedent cho Quiz fields, question gaps và không tự thêm answer-key field.
- [API #07 public search](../07_courses_search/02_Overview.md) và [API #78 Admin list](../78_admin_content_pending/02_Overview.md) — page default, fixed-size count/page precedent; [API #82](../82_admin_lessons_list/02_Overview.md) là precedent ẩn Lesson tombstone.
- [API Guidelines](../../../../../contracts/api-guidelines/README.md) — envelope, trace và error data convention.
- [Current route/module/tests](../../../app/api/v1.py) and [`api_87_admin_quizzes_list`](../../../app/modules/admin/api_87_admin_quizzes_list/) — current local implementation; [middleware](../../../app/core/middleware.py) and [auth helper](../../../app/utils/auth.py) — shared error/auth boundary.

## Tables read

| Relation | Candidate fields | Basis/status |
|---|---|---|
| Legacy quizzes | id, course_id, name, passing_score, time_limit_minutes, status | Candidate BIGINT DDL; current count/page reads metadata; status filter exact and `DELETED` is always excluded. Live schema chưa xác minh. |
| Legacy quiz_questions | id, quiz_id, question_text, question_type, sort_order | Not queried by list projection; migration 013 supplies a local DERIVED type field. |
| Legacy quiz_choices | id, question_id, choice_text, is_correct, sort_order | Not queried by list projection; #88 defines a DERIVED Admin choice shape, and migration 013 supplies order. |
| V1-PILOT assessments/quiz_questions/quiz_options | UUID versioned model | Không tương thích trực tiếp với Quiz IDs int64 và legacy table names; không chọn làm mapping cho endpoint này. |

## Tables write

Không có — GET chỉ đọc.

## Mục chú ý

- Catalog khai báo `ApiEnvelope<Quiz>`, trong khi API name, AC-35 và query `page` thể hiện danh sách. Runtime chọn `ApiEnvelope<Page<Quiz>>` theo reusable Page và #07/#78; đây vẫn là DERIVED, chưa được owner duyệt.
- Runtime trả `questions: []` trong từng list item và không đọc child tables. Đây là projection metadata-only theo nhánh list; không khẳng định Quiz không có questions. Schema child local hiện có qua migration 013/API #88, nhưng AC-35 list node chỉ nêu “Query quizzes” và API #87 chưa tải nested tree.
- Catalog vẫn không định nghĩa QuestionType values hoặc QuizChoice fields. API #88 bổ sung local DERIVED `question_type`, `sort_order` và Admin choice `{id,text,is_correct}`; API #87 không query choices. Student API #28 phải tiếp tục omit `is_correct`.
- Query `course` và `status` dùng exact match; khi vắng mặt filter tương ứng không áp dụng. `status` được giữ nguyên, không trim/case-normalize/whitelist.
- `page` là 1-based, default 1, fixed page size 20, `id ASC`, count/page dùng cùng filter; đây là DERIVED theo #07/#78. API không nhận `size` hoặc `sort`.
- Quiz có `status='DELETED'` luôn bị ẩn, kể cả khi filter gửi `status=DELETED`, theo local AC-35/#90 proposal và precedent #82. Tombstone value vẫn chưa canonical.
- Legacy `quizzes.course_id` và `passing_score` cho phép NULL dù Quiz yêu cầu cả hai; current mapper trả safe 500 nếu row không đáp ứng required fields. `duration_minutes` null bị omit. Live database/schema chưa xác minh.
- Không trả quizzes.description, status, created_at hoặc updated_at vì reusable Quiz không khai báo các field này.
- Không thêm 404 cho list rỗng hoặc course không tồn tại; không có course existence query. Collection rỗng trả 200 `Page` với `items=[]`.

## Assumptions

- Filter course/status dùng phép so sánh bằng chính xác; status giữ nguyên giá trị client gửi, không trim/uppercase hoặc whitelist khi chưa có enum.
- Local query/page behavior uses page 1, fixed size 20, `id ASC`, exact optional filters and matched total count.
- Response uses `ApiEnvelope<Page<Quiz>>`; each metadata-only Quiz item contains `questions=[]` because the required nested schema cannot be built from selected legacy sources.
- Query validation returns 422 `DESIGN_VALIDATION_ERROR` for malformed/out-of-range `course`/`page`; this adds local behavior beyond the direct catalog error set.

## Conflicts

- Catalog response `ApiEnvelope<Quiz>` conflicts with list intent and query `page`; local code returns a derived Page.
- Quiz requires `questions[]`, but local list returns an empty array and does not query actual nested question data; owner/schema confirmation remains open.
- Legacy BIGINT quizzes model khác V1-PILOT UUID assessments model; live schema chưa xác minh.
- `question_type`/choice ordering hiện là local migration candidate từ API #88; owner approval/live schema chưa xác nhận. Catalog QuizChoice shape vẫn thiếu.
- AC-35 requires quiz-management permission; local code enforces shared `ADMIN` role, not a dedicated permission policy.
- Direct catalog errors are 401/403/500; local input validation also returns 422 `DESIGN_VALIDATION_ERROR`. The route is now in `DESIGN_CONTRACT_PATHS`.
- Current `error_response` serializes omitted `data` as JSON null, matching API Guidelines.

## Security note

- Runtime requires Bearer JWT and shared `ADMIN` role before query parsing/DB access. Fine-grained quiz-management permission is not source-backed.
- Authorization phải hoàn tất trước khi đọc quiz/question/choice data; query filter course không thay thế quyền truy cập.
- Không dùng Student guard làm Admin authorization.
- Không thêm answer key hoặc field nhạy cảm ngoài Quiz/QuizQuestion/QuizChoice schema đã được công bố.
- Không trả SQL, stack trace hoặc thông tin database nội bộ.

## Performance note

- Page size 20 limits metadata rows. The current list performs count + page SQL only and no nested/N+1 reads.
- Catalog/AC-35 không quy định SLA, index hoặc maximum total count.
- Legacy và V1-PILOT DDL không chứng minh index hoặc live query plan.

## Contract interpretation

- DIRECT: GET/path, Admin Bearer role, query names/types, `ApiEnvelope<Quiz>`, HTTP 200 and catalog errors 401/403/500.
- DERIVED/current locally: shared ADMIN role fallback, exact filters, positive page default 1, fixed size 20, `id ASC`, `Page<Quiz>`, metadata-only `questions=[]`, hidden `DELETED`, empty Page 200 and 422 query validation.
- SOURCE_REQUIRED: dedicated permission, active schema, canonical tombstone/status policy, complete QuestionType/QuizChoice contract and live DB behavior.
- DISCREPANCY: catalog singleton response vs list/Page runtime; nested Quiz fields vs empty list projection; local 422 vs catalog error set.

## Tình trạng nhóm AC-35

- Macro-review #87–#91: document-level `VERIFIED_WITH_OPEN_QUESTIONS`; API #87 is now locally wired with 20 focused fake-DB HTTP tests. Other APIs in the group remain design-only in this task; neither document review nor local tests imply owner approval/live deployment.
- Đề xuất DERIVED dùng chung: #90 soft-delete quiz có attempt và giữ lịch sử; #87 ẩn tombstone mặc định; #89 không sửa quiz đã tombstone hoặc có attempt/answer history; #29 chặn attempt mới sau tombstone; #30–#32 giữ khả năng xử lý/đọc attempt đã tạo; #91 tổng hợp lịch sử còn lưu; hard-delete/không có quiz row trả 404 theo contract #91.
- Giá trị tombstone, nhánh hard-delete khi chưa có attempt, xử lý attempt đang làm, status transition DRAFT → mở và cách ánh xạ lỗi vẫn cần xác nhận.
- Contract trực tiếp của từng API được giữ nguyên. #87 list/page response và #91 statistics/Quiz response vẫn là discrepancy.
- Chi tiết: [Verification Report nhóm AC-35](../91_admin_quizzes_statistics/VERIFICATION_REPORT.md).
---
## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `Overview`
- Dimension: `A1:BA10`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `4`
- Số vùng merge: `0`

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 1 | `A1` | 【Khái quát】 |  |
| 3 | `B3` | Get thông tin…. |  |
| 5 | `A5` | 【Mục chú ý】 |  |
| 7 | `B7` | Không có |  |

</details>
