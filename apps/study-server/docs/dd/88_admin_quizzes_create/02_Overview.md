---
title: "Overview"
order: 2
dd_id: "88"
api_name: "Tạo quiz mới"
source_sheet: "Overview"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | #88 |
| Module | ADMIN / SYSTEM MANAGEMENT — AC-35 |
| Method | POST |
| Endpoint | /api/v1/admin/quizzes |
| Purpose | Admin tạo Quiz cùng tập câu hỏi và lựa chọn thuộc Quiz. |
| Consumer/Actor | Admin có quiz-management permission |
| Authentication | Bearer JWT |
| Authorization | Catalog yêu cầu role Admin; AC-35 yêu cầu quiz-management permission. Guard/policy chưa có trong Study source. |
| Basis | Method/path/body/response/status/errors DIRECT; JSON lồng trong hai string và mapping bảng DERIVED/CANDIDATE. |
| Status | Draft — Needs Confirmation |
| Current implementation | UNWIRED / NOT_FOUND: không có route, module hoặc test API #88 trong source hiện tại. |
| Transaction | Một transaction cho Quiz, Questions và Choices; atomicity DERIVED từ thao tác tạo resource cha/con. |
| Side effects | Ba nhóm INSERT candidate; không có external call. |

## Sources

- [API catalog và Quiz schema](../../../../../docs/lists/list_api.md) — row #88, body và direct response; QuizQuestion fields.
- [AC/API index, AC-35](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — Admin quiz-management permission và nhóm API #87–#91.
- [AC-35 activity diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — từ list #87, nhánh CREATE gọi #88, “INSERT Quiz + Questions”, sau đó hiển thị kết quả.
- [DB table design](../../diagrams/DB_UNICA_TABLES.md) và [DB ERD](../../diagrams/DB_UNICA_ERD.drawio) — legacy candidate tables/relations; không chứng minh live schema.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — candidate BIGINT quizzes, quiz_questions, quiz_choices.
- [V1-PILOT Study DDL](../../../../../infra/postgres/02_study_db.sql) — UUID assessments/questions/options; model khác và không ghép vào legacy ID.
- [API #28 Quiz detail DD](../28_quizzes_detail/02_Overview.md), [response](../28_quizzes_detail/04_Response.md), [data mapping](../28_quizzes_detail/05_Data_Mapping.md) — QuizQuestion projection; QuestionType/QuizChoice/answer-key gaps.
- [API #87 Admin quiz list DD](../87_admin_quizzes_list/02_Overview.md), [data mapping](../87_admin_quizzes_list/05_Data_Mapping.md), [open questions](../87_admin_quizzes_list/OPEN_QUESTIONS.md) — cùng AC-35, Quiz schema và list/cardinality gap.
- [API Guidelines](../../../../../contracts/api-guidelines/README.md) — envelope, error data, trace ID.
- [Current router](../../../app/api/v1.py), [middleware](../../../app/core/middleware.py), [auth helper](../../../app/utils/auth.py), [response helper](../../../app/core/responses.py), [Study tests](../../../tests/) — wiring/error boundary hiện tại.

## Tables write

| Relation | Operation | Candidate fields | Basis/status |
|---|---|---|---|
| Legacy quizzes | INSERT | course_id, name, passing_score, time_limit_minutes, status, created_at, updated_at | BIGINT DDL candidate; live schema chưa xác minh. |
| Legacy quiz_questions | INSERT | quiz_id, question_text, sort_order, score | Candidate relation; logical QuestionType không có physical column trong legacy DDL. |
| Legacy quiz_choices | INSERT | question_id, choice_text, is_correct | Candidate answer-key relation; QuizChoice chưa được định nghĩa. |
| Courses | SELECT only | id | Candidate existence check theo config.course_id; DERIVED, không đọc status/owner. |

## Mục chú ý

- Catalog khai báo body gồm hai chuỗi bắt buộc: config:string và questions:string. DD không đổi outer body thành object.
- Đề xuất DERIVED: config chứa JSON object cấu hình Quiz; questions chứa JSON array câu hỏi. Keys bên trong không thuộc contract trực tiếp.
- Đề xuất choice input {text, is_correct} dựa trên legacy choice_text/is_correct để lưu text và answer key candidate; đây chưa phải reusable QuizChoice contract.
- Logical QuizQuestion bắt buộc type, nhưng legacy quiz_questions không có cột type. V1-PILOT có question_type nhưng dùng UUID assessment model.
- AC-35 diagram chỉ ghi “INSERT Quiz + Questions”. Insert choices là DERIVED theo QuizQuestion.choices và candidate DB relation.
- Một transaction atomic cho Quiz, Questions và Choices là đề xuất DERIVED để tránh ghi dở dang.
- Legacy quizzes.status default DRAFT; body và Quiz response không có status. Vòng đời chuyển sang trạng thái mở chưa được nhóm AC-35 giải quyết.
- Legacy created_at/updated_at là NOT NULL nhưng không có default; candidate insert phải gán cùng thời điểm tạo.
- Không thêm description, status, question score hoặc is_correct vào response khi reusable schema không khai báo.

## Assumptions

- config được parse thành JSON object với course_id, title, duration_minutes? và passing_score.
- questions được parse thành array theo thứ tự client gửi, với text, type và choices.
- QuestionType value trong ví dụ lấy từ pilot constraint chỉ để minh họa; enum API/storage vẫn SOURCE_REQUIRED.
- Course ID không tồn tại đề xuất trả 422 DESIGN_VALIDATION_ERROR vì catalog không có 404.
- Question array index được candidate map vào sort_order zero-based; choice order chưa có cột lưu trong legacy DDL.

## Conflicts

- Catalog chỉ định config/questions là string nhưng không có embedded schema.
- Response Quiz yêu cầu questions[].type và choices[], trong khi legacy table thiếu type và QuizChoice chưa có logical schema.
- Legacy BIGINT tables khác V1-PILOT UUID assessments/options; live DB chưa xác minh.
- AC-35 yêu cầu quiz-management permission nhưng Study source hiện chỉ có Student guard.
- Path #88 chưa ở middleware allowlist; route mới không wire path sẽ trả fallback code khác catalog.
- API #87 có list/cardinality discrepancy; API #89 catalog chưa khai báo body dù diagram mô tả update quiz/question set.
- API Guidelines yêu cầu error data=null; current helper serialize data=None thành {}.

## Security and transaction notes

- Chỉ Admin có Bearer JWT hợp lệ và quiz-management permission mới được tạo quiz.
- Kiểm tra quyền trước khi đọc course hoặc ghi dữ liệu.
- Không dùng Student guard làm Admin authorization; không trả SQL/stack trace.
- Không đưa is_correct vào Quiz response khi QuizChoice chưa được định nghĩa.
- Validate body trước transaction; Q0 course lookup và các insert chạy trong cùng transaction. Nếu Q0 không có course thì kết thúc không ghi; lỗi insert/commit rollback toàn bộ.
- Không tự đặt payload limit, số question/choice, SLA hoặc status whitelist.

## Contract interpretation

- DIRECT: POST/path, Admin Bearer role, body field names/types, ApiEnvelope<Quiz>, HTTP 201, DESIGN_RESOURCE_CREATED và errors 401/403/422/500.
- DERIVED: JSON text schema, course existence→422, atomic transaction và input order mapping.
- SOURCE_REQUIRED: QuestionType enum/storage, QuizChoice shape, correct-answer rules, choice order, active schema, Admin permission và error serialization.
- DISCREPANCY: logical QuizQuestion fields so với legacy question table; BIGINT contract so với UUID pilot model.

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
