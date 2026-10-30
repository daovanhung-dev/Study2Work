---
title: "Overview"
order: 2
dd_id: "90"
api_name: "Xóa quiz"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | #90 |
| Module | ADMIN / SYSTEM MANAGEMENT — AC-35 |
| Method | DELETE |
| Endpoint | `/api/v1/admin/quizzes/{quiz_id}` |
| Purpose | Admin xóa quiz; AC-35 yêu cầu soft delete nếu quiz đã có attempts. |
| Consumer/Actor | Admin có quiz-management permission |
| Authentication | Bearer JWT |
| Authorization | Runtime dùng shared `ADMIN` role guard. AC-35 fine-grained quiz-management permission chưa có policy source. |
| Basis | Contract và AC-35 soft-delete intent DIRECT; route/auth/transaction là SOURCE_BACKED local; no-attempt hard delete, tombstone value/time và answer-only protection DERIVED. |
| Status | Draft — Needs Confirmation |
| Transaction | Runtime khóa quiz → questions → choices, kiểm tra attempt/answer history, mutation và commit trong một transaction; policy phối hợp với API #29 vẫn cần xác nhận. |
| Side effects | Có attempt hoặc answer liên kết: đặt `status='DELETED'`, cập nhật `updated_at`, giữ child/history. Không có history: xóa choices → questions → quiz. Đây là policy DERIVED. |

## Sources

- [API catalog và reusable schemas](../../../../../docs/lists/list_api.md) — row #90, DeleteResult, Quiz/QuizAttempt và business codes.
- [AC/API index, AC-35](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — Admin quiz-management permission và nhóm #87–#91.
- [AC-35 activity diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — nhánh DELETE #90 → “Soft delete nếu đã có attempts” → hiển thị kết quả.
- [AC-16 activity diagram](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — API #29 tạo attempt `IN_PROGRESS`; #30–#32 giữ câu trả lời, submit và đọc kết quả.
- [DB table guide](../../diagrams/DB_UNICA_TABLES.md) và [DB ERD](../../diagrams/DB_UNICA_ERD.drawio) — candidate relation quiz/question/choice/attempt/answer; không chứng minh live schema.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — candidate BIGINT tables; không có delete marker hoặc `ON DELETE CASCADE` trong chuỗi quiz.
- [V1-PILOT Study DDL](../../../../../infra/postgres/02_study_db.sql) — UUID/versioned `assessments` model với FK RESTRICT; không map ngầm sang API int64.
- [API #87 list](../87_admin_quizzes_list/02_Overview.md), [#88 create](../88_admin_quizzes_create/02_Overview.md), [#89 update](../89_admin_quizzes_update/02_Overview.md) — cùng nhóm AC-35.
- [API #29 create attempt](../29_quizzes_attempts/02_Overview.md), [#30 answers](../30_attempts_answers/02_Overview.md), [#31 submit](../31_attempts_submit/02_Overview.md), [#32 result](../32_attempts_result/02_Overview.md) — dependency lịch sử do Student sử dụng.
- [API #86 Admin lesson delete](../86_admin_lesson_delete/02_Overview.md) — precedent tách logical delete policy khỏi physical tombstone/timestamp.
- [Current router](../../../app/api/v1.py), [auth helper](../../../app/utils/auth.py), [middleware](../../../app/core/middleware.py), [response helper](../../../app/core/responses.py) — current wiring/error boundary.
- [API Guidelines](../../../../../contracts/api-guidelines/README.md) — envelope, trace và error `data:null` convention.

## Tables read

| Relation | Candidate fields/relationship | Basis/status |
|---|---|---|
| Legacy `quizzes` | `id`, `status`, `updated_at` | BIGINT DDL artifact; `status` enum chưa chốt; không có `deleted_at`; live schema chưa xác minh. Runtime dùng các cột candidate này. |
| Legacy `quiz_attempts` | `id`, `quiz_id`, `status` | Candidate existence check; mọi status được tính là attempt; DDL cho phép NULL `quiz_id` dù DB guide mô tả required; live schema chưa xác minh. |
| Legacy `quiz_questions` | `id`, `quiz_id` | Candidate child relation để xóa khi chưa có attempts. |
| Legacy `quiz_choices` | `id`, `question_id` | Candidate child relation; DDL cho phép NULL `question_id` dù DB guide nói required; xóa trước question rows nếu hard-delete branch được duyệt. |
| Legacy `quiz_answers` | `attempt_id`, `question_id`, `choice_id` | History query kiểm tra answer trỏ tới question/choice của quiz; answer-only reference cũng chọn nhánh soft để tránh orphan. |
| V1-PILOT assessment relations | UUID `assessments`, `quiz_questions`, `quiz_options`, `assessment_attempts`, `assessment_answers` | Schema khác int64; chỉ ghi nhận discrepancy, không dùng làm mapping cho API #90. |

## Tables write

- Runtime soft-delete branch: UPDATE `quizzes.status='DELETED'` và `updated_at`; value và timestamp meaning là lựa chọn DERIVED, chưa có enum/source được duyệt.
- Runtime no-history branch: DELETE `quiz_choices`, `quiz_questions`, rồi `quizzes` trong một transaction; không dựa vào cascade.
- Không xóa `quiz_attempts` hoặc `quiz_answers` ở bất kỳ nhánh có lịch sử nào.

## Mục chú ý

- Catalog trực tiếp chỉ khai báo path `quiz_id:int64!`; không thêm body/query, `reason`, confirmation flag hay idempotency field.
- AC-35 trực tiếp yêu cầu soft delete nếu có attempts; diagram không mô tả rõ nhánh không có attempt. Hard-delete branch là đề xuất `DERIVED`.
- Legacy `quizzes.status` có `VARCHAR(20)` nhưng không có enum canonical; legacy DDL không có `deleted_at`. Runtime dùng `status='DELETED'` và `updated_at` làm tombstone/timestamp candidate; owner cần xác nhận.
- `DeleteResult` yêu cầu `id`, literal `status="deleted"`, `deleted_at:date-time`. Runtime map từ `updated_at` trên soft delete/repeat và lấy `CURRENT_TIMESTAMP` trong `DELETE RETURNING` trên hard delete.
- #29 chưa chốt predicate quiz-open/status/concurrency. Sau soft delete phải ngăn tạo attempt mới, nhưng vẫn giữ #30–#32 và #91 đọc lịch sử theo policy.
- #87 list visibility, #89 update eligibility, #91 statistics visibility cần được đối chiếu trong macro-review sau khi #91 DD tồn tại.
- API #90 đã có route/module/test trong source cục bộ; shared ADMIN guard và path template được dùng. Fine-grained quiz-management permission vẫn chưa có policy source.

## Assumptions

- Q2 kiểm tra attempt tồn tại với bất kỳ `quiz_attempts.status` nào; không lọc `IN_PROGRESS`/`SUBMITTED` vì catalog/diagram nói attempts, không nói chỉ attempt đang chạy.
- Runtime cũng kiểm tra answer rows gắn với question/choice của quiz; answer-only reference chọn soft delete như một integrity safeguard DERIVED.
- Nếu quiz đã có tombstone `DELETED`, đề xuất giữ nguyên timestamp và trả cùng DeleteResult 200 (no-op); đây là idempotency proposal `DERIVED`, cần duyệt.
- Khi có attempt, giữ nguyên question/choice/attempt/answer rows để giữ lịch sử và candidate statistics; đây là hệ quả an toàn `DERIVED` của soft delete.
- Khi không có attempt, đề xuất hard delete child-first `quiz_choices` → `quiz_questions` → `quizzes`, dựa trên quan hệ legacy và việc DDL không khai báo cascade.
- Dùng `quizzes.status='DELETED'` và `updated_at` làm tombstone/timestamp candidate; state value và map `deleted_at` từ `updated_at` cần phê duyệt. Hard delete lấy timestamp từ transaction DB.
- Không tự ánh xạ attempts dependency thành 422; nhánh có attempts được AC-35 xử lý bằng soft delete. Trigger của catalog 422 chưa được đặc tả.

## Conflicts

- AC-35 soft-delete intent không khớp physical legacy DDL vốn không có `deleted_at` và không định nghĩa status `DELETED`.
- No-attempt hard delete là nhánh suy diễn, không được activity diagram mô tả trực tiếp.
- V1-PILOT schema dùng UUID/versioned assessment, khác catalog BIGINT và legacy `quizzes`.
- API #29 chưa chốt trạng thái quiz mở và concurrency; AC-35 tombstone cần đồng bộ với tạo attempt.
- API Guidelines và current helper trả error `data:null`; API #90 tests xác minh response này.
- Shared ADMIN guard và dynamic `/api/v1/admin/quizzes/{quiz_id}` template đã được dùng bởi route #89/#90. Fine-grained permission vẫn chưa có policy source.

## Security note

- Shared ADMIN Bearer guard chạy trước path parsing và database lookup; fine-grained quiz-management authorization chưa được triển khai vì policy source chưa có.
- Không dùng Student guard thay Admin guard.
- Không trả attempt/answer details trong DeleteResult hoặc log dữ liệu Student.
- Không xóa attempt/answer history. Hard delete chỉ được chọn khi không tìm thấy attempt hoặc answer link tới question/choice của quiz.

## Performance note

- Một existence lookup và một `EXISTS` attempt query đủ chọn nhánh; không load toàn bộ attempts/answers.
- Hard-delete branch thao tác theo quiz/question relationship; row counts, indexes, transaction duration và query plan chưa live-verified.
- Không có SLA, retry/idempotency, locking hoặc concurrency contract.

## Contract interpretation

- DIRECT: DELETE/path/Admin Bearer, DeleteResult, HTTP 200, exact five error codes; AC-35 soft-delete intent when attempts exist.
- SOURCE_BACKED local: raw route, shared ADMIN guard, positive signed-int64 validation, row locks, transaction/rollback, exact envelope and error codes.
- DERIVED: hard delete when no attempt/answer reference; use status tombstone and timestamp mapping; answer-only protection; idempotent repeat DELETE.
- SOURCE_REQUIRED: allowed status values, persistent deleted timestamp, Admin authorization, #29 coordination/locking, repeat-delete semantics and visibility across #87/#89/#91.

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
