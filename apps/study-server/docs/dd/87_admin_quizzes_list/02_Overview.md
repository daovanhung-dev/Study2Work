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
| Authorization | Catalog yêu cầu role Admin; tiền điều kiện AC-35 yêu cầu quiz-management permission. Guard/policy chưa có trong Study source. |
| Basis | Method/path/query/response/status/errors DIRECT; filter/page defaults và list projection DERIVED hoặc cần xác nhận. |
| Status | Draft — Needs Confirmation |
| Current implementation | UNWIRED / NOT_FOUND: không có route, module hoặc test API #87 trong source hiện tại. |
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
- [API #82 Admin list DD](../82_admin_lessons_list/02_Overview.md) và [open questions](../82_admin_lessons_list/OPEN_QUESTIONS.md) — precedent giữ response singleton trực tiếp khi list intent không khớp schema.
- [API Guidelines](../../../../../contracts/api-guidelines/README.md) — envelope, trace và error data convention.
- [Current router](../../../app/api/v1.py), [middleware](../../../app/core/middleware.py), [auth helper](../../../app/utils/auth.py), [Study tests](../../../tests/) — current wiring boundary.

## Tables read

| Relation | Candidate fields | Basis/status |
|---|---|---|
| Legacy quizzes | id, course_id, name, passing_score, time_limit_minutes; status làm filter nếu được gửi | Candidate BIGINT DDL; name → title; live schema chưa xác minh. |
| Legacy quiz_questions | id, quiz_id, question_text, sort_order | Candidate nested QuizQuestion source; type không có trong legacy table. |
| Legacy quiz_choices | id, question_id, choice_text | Candidate relation; QuizChoice schema và choice order chưa được định nghĩa. |
| V1-PILOT assessments/quiz_questions/quiz_options | UUID versioned model | Không tương thích trực tiếp với Quiz IDs int64 và legacy table names; không chọn làm mapping cho endpoint này. |

## Tables write

Không có — GET chỉ đọc.

## Mục chú ý

- Catalog khai báo ApiEnvelope<Quiz>, trong khi API name, AC-35 và query page thể hiện danh sách. DD giữ direct type và ghi ApiEnvelope<Page<Quiz>> là proposal DERIVED chưa duyệt.
- Reusable Quiz yêu cầu questions[]; AC-35 diagram chỉ ghi “Query quizzes”. Nested question/choice reads là candidate để đáp ứng schema response, cần xác nhận list có phải tải toàn bộ question set không.
- Catalog không định nghĩa QuizChoice hoặc QuestionType; legacy quiz_questions không có type column. Không thêm is_correct vào response khi schema không khai báo field đó.
- Query course và status được đề xuất exact match nếu được gửi; khi vắng mặt không thêm predicate. Không lọc status mặc định.
- Query page được đề xuất 1-based, default 1, fixed page size 20 theo convention API #07; đây không phải catalog contract. Catalog không khai báo size, sort hoặc pagination response.
- Legacy quizzes.course_id cho phép NULL trong DDL nhưng Quiz.course_id là required. Legacy quizzes.status không có enum đầy đủ. Live database/schema chưa xác minh.
- Không trả quizzes.description, status, created_at hoặc updated_at vì reusable Quiz không khai báo các field này.
- Không thêm 404 cho danh sách rỗng; catalog chỉ liệt kê 401/403/500. Empty list 200 là proposal nếu collection response được xác nhận.

## Assumptions

- Filter course/status dùng phép so sánh bằng chính xác; status giữ nguyên giá trị client gửi, không trim/uppercase hoặc whitelist khi chưa có enum.
- page mặc định 1, size nội bộ cố định 20 và thứ tự id ASC là proposal DERIVED để có trang ổn định theo convention API #07.
- Nếu owner xác nhận list response, đề xuất ApiEnvelope<Page<Quiz>> với items và PageMeta hiện có; không xem đây là direct response contract.
- Nếu nested questions được yêu cầu, đọc theo batch cho các quiz trên trang, không query từng quiz; QuizChoice shape và question type vẫn SOURCE_REQUIRED.

## Conflicts

- Catalog response ApiEnvelope<Quiz> xung đột với list intent và query page; response cardinality chưa được chốt.
- Quiz schema yêu cầu questions[] nhưng diagram AC-35 chỉ nêu query quizzes; nested list projection chưa được xác nhận.
- Legacy BIGINT quizzes model khác V1-PILOT UUID assessments model; live schema chưa xác minh.
- QuizQuestion.type không có physical legacy column và QuizChoice không có reusable schema.
- AC-35 yêu cầu Admin quiz-management permission nhưng Study source hiện chỉ có Student guard.
- Catalog lỗi 401/403/500 xung đột với middleware fallback cho path chưa nằm trong DESIGN_CONTRACT_PATHS nếu route được thêm mà không cập nhật wiring.
- API Guidelines yêu cầu error data=null; current error_response mặc định {} khi data không truyền.

## Security note

- Chỉ Admin có Bearer JWT hợp lệ và quiz-management permission mới được query.
- Authorization phải hoàn tất trước khi đọc quiz/question/choice data; query filter course không thay thế quyền truy cập.
- Không dùng Student guard làm Admin authorization.
- Không thêm answer key hoặc field nhạy cảm ngoài Quiz/QuizQuestion/QuizChoice schema đã được công bố.
- Không trả SQL, stack trace hoặc thông tin database nội bộ.

## Performance note

- Page size 20, nếu được duyệt, giới hạn kích thước candidate list; chưa phải contract.
- Nested questions/choices cần batch theo quiz/question IDs để tránh N+1 query nếu response list yêu cầu nested data.
- Catalog/AC-35 không quy định SLA, index hoặc maximum total count.
- Legacy và V1-PILOT DDL không chứng minh index hoặc live query plan.

## Contract interpretation

- DIRECT: GET/path, Admin Bearer, query names/types, ApiEnvelope<Quiz>, HTTP 200 và errors 401/403/500.
- DERIVED: exact-match filters, page 1-based/default, fixed size 20, id ASC và Page response proposal.
- SOURCE_REQUIRED: active schema, Admin guard/permission mapping, status enum, nested list inclusion, QuestionType, QuizChoice shape, query parse errors và error-envelope integration.
- DISCREPANCY: list/page intent so với ApiEnvelope<Quiz> trực tiếp.

## Tình trạng nhóm AC-35

- Macro-review tài liệu #87–#91: VERIFIED_WITH_OPEN_QUESTIONS; hoàn tất sau khi có DD #91. Đây là review tài liệu, không phải owner approval hoặc xác minh runtime.
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
