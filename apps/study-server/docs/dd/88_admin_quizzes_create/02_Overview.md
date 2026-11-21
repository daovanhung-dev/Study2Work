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
| Consumer/Actor | Admin |
| Authentication | Bearer JWT |
| Authorization | Catalog yêu cầu role Admin; AC-35 nêu quiz-management permission nhưng không có policy/claim source. Local fallback dùng shared ADMIN guard. |
| Basis | Method/path/outer body/response/status/errors DIRECT; embedded JSON, input mapping và schema extensions DERIVED. |
| Status | Draft — Needs Confirmation |
| Current implementation | Đang chuẩn bị implementation; trước khi code không có route/module/test API #88. |
| Transaction | Một transaction nguyên tử cho Quiz, Questions và Choices (DERIVED). |
| Side effects | INSERT legacy BIGINT Quiz, Question và Choice; không có external call. |

## Sources

- [API catalog và Quiz schema](../../../../../docs/lists/list_api.md) — row #88, body và logical Quiz/QuizQuestion fields.
- [AC/API index, AC-35](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — Admin quiz-management permission và nhóm API #87–#91.
- [AC-35 activity diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — nhánh CREATE gọi #88, “INSERT Quiz + Questions”, rồi hiển thị kết quả.
- [DB table design](../../diagrams/DB_UNICA_TABLES.md) và [DB ERD](../../diagrams/DB_UNICA_ERD.drawio) — legacy candidate quiz relations; new question-type/choice-order fields are local DERIVED extensions.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) and [migration 013](../../../../../infra/postgres/study-server/migrations/013_quiz_question_type_and_choice_order.sql) — BIGINT candidate model and additive columns; not live-schema proof.
- [V1-PILOT Study DDL](../../../../../infra/postgres/02_study_db.sql) — UUID assessment model; its three type labels are vocabulary evidence only and its IDs/tables are not reused.
- [API #28 Quiz detail DD](../28_quizzes_detail/02_Overview.md), [response](../28_quizzes_detail/04_Response.md), [data mapping](../28_quizzes_detail/05_Data_Mapping.md) — Student response must omit answer-key data.
- [API #87 Admin quiz list DD](../87_admin_quizzes_list/02_Overview.md) and [API #89 update DD](../89_admin_quizzes_update/02_Overview.md) — linked projections/schema dependencies.
- [API Guidelines](../../../../../contracts/api-guidelines/README.md) — envelope, error data and trace ID.
- [Current router](../../../app/api/v1.py), [middleware](../../../app/core/middleware.py), [auth helper](../../../app/utils/auth.py), [response helper](../../../app/core/responses.py), [Study tests](../../../tests/) — runtime boundaries.

## Tables read

| Relation | Candidate fields | Purpose | Basis/status |
|---|---|---|---|
| courses | id | Check course reference before insert | DERIVED; legacy BIGINT candidate, live schema unverified. |

## Tables write

| Relation | Operation | Candidate fields | Basis/status |
|---|---|---|---|
| Legacy quizzes | INSERT | course_id, name, passing_score, time_limit_minutes, status, created_at, updated_at | BIGINT DDL candidate; status uses existing DRAFT default. |
| Legacy quiz_questions | INSERT | quiz_id, question_text, question_type, sort_order, score | `question_type` is a new nullable migration column; API #88 always writes it. |
| Legacy quiz_choices | INSERT | question_id, choice_text, is_correct, sort_order | `sort_order` is a new migration column; preserves request order. |

## Mục chú ý

- Catalog giữ nguyên outer body `{config:string!, questions:string!}`; parse embedded JSON là fallback DERIVED.
- `config` được hiểu là `{course_id,title,duration_minutes?,passing_score}`; `questions` là array `{text,type,choices:[{text,is_correct?}]}`.
- `QuestionType` local dùng `SINGLE_CHOICE`, `MULTIPLE_CHOICE`, `TRUE_FALSE` theo vocabulary V1-PILOT; không dùng UUID tables hoặc IDs.
- Migration 013 thêm `quiz_questions.question_type` và `quiz_choices.sort_order` cho legacy BIGINT model, để response giữ đầy đủ type và thứ tự choices. Đây là schema fallback local, không phải schema đã được owner duyệt hoặc triển khai.
- Admin response lựa chọn `QuizChoice={id,text,is_correct}` là DERIVED; Student API #28 không được trả `is_correct`.
- Không đặt số câu/lựa chọn tối thiểu, giới hạn đáp án đúng theo type, course status/access, passing-score business range hay body-size limit khi chưa có rule.
- Quiz status dùng DDL default `DRAFT`; lifecycle chuyển sang trạng thái làm bài vẫn chưa được nhóm AC-35 quy định.
- `created_at`/`updated_at` bắt buộc nhưng không có default trong legacy DDL; insert gán cùng thời điểm.
- Tất cả DB/schema artifacts và fake-session tests chỉ chứng minh local source, không xác minh live DB, migration deployment hay endpoint deployment.

## Conflicts

- Catalog khai báo hai string nhưng không định nghĩa JSON lồng.
- Logical QuizQuestion yêu cầu type, trong khi DB diagram và legacy DDL ban đầu không có cột type.
- Catalog thiếu QuestionType values và QuizChoice shape; local choices order cũng không có cột ban đầu.
- AC-35 yêu cầu quiz-management permission nhưng Study source chỉ có shared ADMIN role guard.
- Legacy BIGINT model không tương thích ID với V1-PILOT UUID assessments/questions/options.

## Security and transaction notes

- Shared ADMIN JWT guard chạy trước khi parse body hoặc truy vấn DB; fine-grained quiz-management permission remains SOURCE_REQUIRED.
- Kiểm tra `courses.id` trước khi ghi. Course không tồn tại trả 422 do catalog không khai báo 404.
- Validate toàn bộ outer/embedded input trước write; không nhận Admin ID hoặc status từ request.
- Q0 và mọi INSERT nằm trong cùng transaction. Commit sau khi toàn bộ Quiz response đã map hợp lệ; mọi lỗi sau transaction start rollback toàn bộ.
- Không trả SQL/stack trace hoặc biến error DB thành validation error.

## Contract interpretation

- DIRECT: POST/path, Admin Bearer role, outer body names/types, ApiEnvelope<Quiz>, HTTP 201, DESIGN_RESOURCE_CREATED, errors 401/403/422/500.
- DERIVED: embedded JSON schema, type vocabulary, QuizChoice shape, course existence→422, migration columns, order preservation, atomic transaction và default `is_correct=false`.
- SOURCE_REQUIRED: fine-grained permission approval, answer-count rules, quiz publication lifecycle, live schema and migration deployment.
- DISCREPANCY: AC-35 diagram/legacy schema thiếu `question_type`/choice order so với required logical QuizQuestion and ordered nested response.

## Tình trạng nhóm AC-35

- API #87 vẫn trả metadata-only quiz rows; `questions=[]` là projection chưa hydrate, không có nghĩa quiz không có câu hỏi.
- API #88 local migration làm mới QuestionType và choice-order persistence khả dụng cho API #89/#28 source follow-up; cách xử lý lịch sử rows có `question_type=NULL` vẫn cần review.
- Macro-review #87–#91 giữ trạng thái `VERIFIED_WITH_OPEN_QUESTIONS`; không phải owner approval hoặc live runtime verification.
- API #89 body/replacement, API #90 deletion/attempt-history, API #91 statistics, DRAFT→open lifecycle và permission policy vẫn mở.
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
