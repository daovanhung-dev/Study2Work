---
title: "Overview"
order: 2
dd_id: "89"
api_name: "Cập nhật quiz"
source_sheet: "Overview"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | #89 |
| Module | ADMIN / SYSTEM MANAGEMENT — AC-35 |
| Method | PUT |
| Endpoint | /api/v1/admin/quizzes/{quiz_id} |
| Purpose | Admin cập nhật Quiz và question set theo nhánh UPDATE của AC-35. |
| Consumer/Actor | Admin có quiz-management permission |
| Authentication | Bearer JWT |
| Authorization | Shared ADMIN role guard exists; AC-35 quiz-management permission has no source-backed policy. |
| Basis | Method/path/response/status/errors DIRECT; request body và replacement semantics DERIVED proposal. |
| Status | Draft — Needs Confirmation |
| Current implementation | SOURCE_BACKED locally: route, module và TestClient tests đã được thêm; live DB/deployment chưa xác minh. |
| Transaction | Parent update và child-set replacement dùng một transaction; map response trước commit. |
| Side effects | UPDATE quizzes; DELETE old choices/questions; INSERT replacement questions/choices khi Quiz chưa có attempt/answer history. |

## Sources

- [API catalog và Quiz schema](../../../../../docs/lists/list_api.md) — row #89, ApiEnvelope<Quiz>, reusable Quiz/QuizQuestion.
- [AC/API index, AC-35](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — Admin quiz-management permission và APIs #87–#91.
- [AC-35 activity diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — nhánh UPDATE gọi #89; backend node ghi “UPDATE quiz/question set”.
- [DB table design](../../diagrams/DB_UNICA_TABLES.md) và [DB ERD](../../diagrams/DB_UNICA_ERD.drawio) — candidate relations quiz/questions/choices/attempts/answers; không chứng minh live schema.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) and [migration 013](../../../../../infra/postgres/study-server/migrations/013_quiz_question_type_and_choice_order.sql) — BIGINT candidates plus DERIVED question-type/order additions.
- [V1-PILOT Study DDL](../../../../../infra/postgres/02_study_db.sql) — UUID assessment/question/option model khác, không ghép với legacy IDs.
- [API #88 tạo quiz](../88_admin_quizzes_create/02_Overview.md), [request](../88_admin_quizzes_create/03_Request.md), [mapping](../88_admin_quizzes_create/05_Data_Mapping.md), [open questions](../88_admin_quizzes_create/OPEN_QUESTIONS.md) — config/questions proposal và schema gaps.
- [API #87 Admin quiz list](../87_admin_quizzes_list/02_Overview.md) và [open questions](../87_admin_quizzes_list/OPEN_QUESTIONS.md) — cùng AC-35, response/cardinality và schema gaps.
- [API #28 Quiz detail](../28_quizzes_detail/04_Response.md) và [mapping](../28_quizzes_detail/05_Data_Mapping.md) — không trả is_correct cho Student; QuizChoice/QuestionType chưa đủ định nghĩa.
- [API #84 Admin lesson update](../84_admin_lesson_update/03_Request.md) và [open questions](../84_admin_lesson_update/OPEN_QUESTIONS.md) — precedent PUT path-only với body proposal tách khỏi direct contract.
- [API Guidelines](../../../../../contracts/api-guidelines/README.md) — envelope, trace ID và error data=null.
- [Current router](../../../app/api/v1.py), [middleware](../../../app/core/middleware.py), [auth helper](../../../app/utils/auth.py), [response helper](../../../app/core/responses.py), [Study tests](../../../tests/) — current wiring/error boundary.

## Tables read

| Relation | Candidate fields | Purpose | Basis/status |
|---|---|---|---|
| Legacy quizzes | id, course_id, name, passing_score, time_limit_minutes, status, updated_at | Load/update parent Quiz | BIGINT DDL candidate; live schema chưa xác minh. |
| Legacy quiz_questions | id, quiz_id, question_text, question_type, sort_order, score | Load/delete/insert replacement questions | `question_type` nullable local DERIVED column from migration 013. |
| Legacy quiz_choices | id, question_id, choice_text, is_correct, sort_order | Delete/insert replacement choices | `sort_order` local DERIVED column from migration 013. |
| Legacy quiz_attempts | id, quiz_id | Detect quiz attempt history | Safety query DERIVED; live schema chưa xác minh. |
| Legacy quiz_answers | attempt_id, question_id, choice_id | Detect history referencing child rows | ERD/DDL candidate; query handles both question_id and choice_id. |

## Tables write

| Relation | Operation | Candidate fields | Basis/status |
|---|---|---|---|
| Legacy quizzes | UPDATE | course_id, name, passing_score, time_limit_minutes, updated_at | Candidate from config; no status/description change. |
| Legacy quiz_choices | DELETE, INSERT | question_id, choice_text, is_correct, sort_order | Local Admin projection `{id,text,is_correct}` reuses API #88 and remains DERIVED. |
| Legacy quiz_questions | DELETE, INSERT | quiz_id, question_text, question_type, sort_order, score | `question_type` is a nullable local DERIVED candidate from migration 013. |

## Mục chú ý

- Catalog #89 là Conditional và chỉ khai báo path quiz_id:int64!; không khai báo body/query.
- AC-35 mô tả UPDATE “quiz/question set”, nhưng không nêu body fields, merge/replacement semantics hoặc attempt guard.
- Proposal DERIVED: body đầy đủ dùng lại config:string và questions:string của API #88; nested JSON shape cũng chỉ là proposal.
- Do body proposal không có child IDs, implementation thay toàn bộ question/choice set trong một transaction; đây vẫn là behavior DERIVED, không phải direct contract.
- Legacy answer rows tham chiếu question/choice IDs; attempts tham chiếu quiz. Implementation trả catalog 422 trước write khi có attempt/answer history; owner review và live FK behavior vẫn mở.
- Migration 013 supplies local `question_type` and choice order for new writes. #88 chooses the Admin choice shape `{id,text,is_correct}`; these remain DERIVED because the catalog has no enum/QuizChoice definition. Student API #28 must omit `is_correct`.
- V1-PILOT dùng UUID assessments/questions/options; không ghép với API ID int64 hoặc legacy Quiz tables.
- Không cập nhật quizzes.status, description, created_at hoặc question score từ input.
- Legacy updated_at NOT NULL nhưng không có default; thời điểm/owner ghi cần xác nhận.
- API #89 hiện dùng shared ADMIN guard trước raw path/body validation và query; dynamic path template đã có trong `DESIGN_CONTRACT_PATHS`. Fine-grained permission vẫn unavailable.

## Assumptions

- config chứa JSON object candidate {course_id,title,duration_minutes?,passing_score}.
- questions chứa JSON array candidate {text,type,choices[]}; choice input candidate {text,is_correct}.
- Full child-set replacement là local DERIVED implementation vì body không có IDs; chưa phải owner-approved behavior.
- Nếu Quiz có attempt hoặc answer history, implementation trả 422 trước mọi write để giữ tham chiếu lịch sử.
- `questions[i]` và `choices[i]` map sang `sort_order=i` zero-based theo #88; migration 013 là local DDL candidate, chưa xác minh live.
- `duration_minutes` bị omit hoặc null đều ghi NULL; question/choice arrays rỗng được chấp nhận và xóa child set hiện tại.
- Route response bao gồm `is_correct` trong Admin choice projection theo API #88; Student API #28 phải tiếp tục omit answer key.

## Conflicts

- Catalog path-only input so với diagram yêu cầu cập nhật quiz/question set.
- Quiz logical schema yêu cầu QuestionType và choices; migration 013 thêm local DERIVED type/order candidates, còn logical QuizChoice schema vẫn chưa có trong catalog.
- quiz_answers tham chiếu question/choice IDs; delete/reinsert có thể làm mất lịch sử hoặc bị FK từ chối.
- Legacy BIGINT tables khác V1-PILOT UUID model; live DB chưa xác minh.
- AC-35 yêu cầu Admin quiz-management permission; current Study source supports shared ADMIN role, but has no fine-grained quiz-management policy.
- API #89 dynamic path chưa có trong DESIGN_CONTRACT_PATHS; cần đăng ký khi wire route.
- Current shared error helper emits `data:null` and `meta.fieldErrors`, matching the API Guidelines.
- AC-35 macro-review #87–#91 chưa thể hoàn tất trước khi có DD #91.

## Security and transaction notes

- Chỉ ADMIN có Bearer JWT hợp lệ được runtime hiện tại cho phép; fine-grained quiz-management permission vẫn SOURCE_REQUIRED.
- Shared ADMIN role authentication must complete before reading quiz/attempt history; fine-grained permission remains unavailable.
- Không nhận Admin ID từ body và không dùng Student guard làm Admin authorization.
- Validate path/body proposal trước mutation.
- Kiểm tra target tồn tại và history policy trước thao tác destructive.
- Parent update và child replacement candidate phải atomic; lỗi giữa các mapping rollback toàn transaction.
- Admin response hiện trả `is_correct` theo local API #88 projection; Student API #28 phải tiếp tục omit answer key.
- Không trả SQL/stack trace hoặc đáp án trong error message.
- Candidate history check không chứng minh chống race; cần thống nhất lock/isolation với API tạo attempt.

## Contract interpretation

- DIRECT: PUT/path, Admin Bearer role, quiz_id:int64!, ApiEnvelope<Quiz>, HTTP 200 DESIGN_RESOURCE_UPDATED, errors 401/403/404/422/500.
- DERIVED: body config/questions, nested JSON, child replacement, attempt/history guard, atomicity, 404 condition và order candidate.
- SOURCE_REQUIRED: Admin permission, live schema, QuestionType storage, QuizChoice fields, course-move policy, null/omit semantics, lock/isolation, response serialization.
- DISCREPANCY: request body missing from catalog; response child schema không map đầy đủ vào legacy tables.

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
