---
title: "Overview"
order: 2
dd_id: "91"
api_name: "Xem thống kê quiz"
source_sheet: "Overview"
format: markdown
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | #91 |
| Module | ADMIN / SYSTEM MANAGEMENT — AC-35 |
| Method | GET |
| Endpoint | `/api/v1/admin/quizzes/{quiz_id}/statistics` |
| Purpose | Admin xem số liệu tổng hợp từ các attempt của một quiz. |
| Consumer/Actor | Admin có quiz-management permission |
| Authentication | Bearer JWT |
| Authorization | Role Admin theo catalog; AC-35 yêu cầu quiz-management permission. Study chưa có Admin guard/policy. |
| Basis | Endpoint/auth/input/direct response/status/errors DIRECT; metric và response thống kê DERIVED proposal. |
| Status | Draft — Needs Confirmation |
| Current implementation | UNWIRED / NOT_FOUND: không có route, module hoặc test API #91. |
| Transaction | N/A — API chỉ đọc. |
| Side effects | Không ghi dữ liệu. |

## Sources

- [API catalog và schemas](../../../../../docs/lists/list_api.md) — row #91, Quiz, QuizAttempt và ApiEnvelope.
- [AC/API index, AC-35](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) và [activity diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — STATISTICS → API #91 → Aggregate attempt statistics → hiển thị.
- [AC/API index, AC-16](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) và [activity diagram](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — attempt, submit, grading và result.
- [DB table design](../../diagrams/DB_UNICA_TABLES.md), [DB ERD](../../diagrams/DB_UNICA_ERD.drawio), [legacy DDL](../../../../../infra/postgres/study-server/DB.sql) — candidate BIGINT quiz/attempt schema.
- [V1-PILOT DDL](../../../../../infra/postgres/02_study_db.sql) — UUID assessment model riêng, không trộn với API int64.
- [API #87–#90](../87_admin_quizzes_list/02_Overview.md), [#88](../88_admin_quizzes_create/02_Overview.md), [#89](../89_admin_quizzes_update/02_Overview.md), [#90](../90_admin_quizzes_delete/02_Overview.md) và [API #29–#32](../29_quizzes_attempts/02_Overview.md), [#30](../30_attempts_answers/02_Overview.md), [#31](../31_attempts_submit/02_Overview.md), [#32](../32_attempts_result/02_Overview.md).
- [Current router](../../../app/api/v1.py), [middleware](../../../app/core/middleware.py), [response helper](../../../app/core/responses.py), [tests](../../../tests/).

## Tables read

| Relation | Candidate fields | Basis/status |
|---|---|---|
| Legacy `quizzes` | `id`, `passing_score`, `status` | BIGINT DDL candidate; enum/nullability/live schema chưa xác minh. |
| Legacy `quiz_attempts` | `id`, `quiz_id`, `submitted_at`, `score`, `status` | Candidate aggregate source; live schema chưa xác minh. |
| Legacy `quiz_answers` | Không đọc | Metric đề xuất chỉ dùng score cấp attempt. |
| V1-PILOT assessments/assessment_attempts | UUID/versioned | Discrepancy; không dùng làm mapping cho API này. |

## Tables write

Không có — GET chỉ đọc.

## Mục chú ý

- Catalog khai báo direct response `ApiEnvelope<Quiz>`; reusable Quiz không có field thống kê.
- AC-35 yêu cầu tổng hợp attempts nhưng không định nghĩa metric, response schema, denominator hoặc rounding.
- `QuizStatistics` là proposal DERIVED riêng, chưa được duyệt và không phải thay đổi catalog.
- `PENDING_GRADE` có thể có submitted_at nhưng chưa có score; đề xuất tính là submitted, không tính là graded/average.
- Tổng attempt đề xuất tính mọi row gắn với quiz, không lọc theo enum status chưa đầy đủ.
- DB guide/ERD/DDL là design artifacts; live schema chưa xác minh.

## Assumptions

- `attempt_count = COUNT(attempt.id)` cho mọi attempt gắn với quiz.
- `submitted_attempt_count` đếm `submitted_at IS NOT NULL`.
- `graded_attempt_count` đếm `score IS NOT NULL`.
- `average_score = AVG(score)` trên score không NULL.
- Khi threshold có giá trị, pass nếu `score >= passing_score`.
- Khi passing_score NULL, passed count và rate là NULL, không đổi unknown thành zero.
- `pass_rate_percent = passed_attempt_count / graded_attempt_count × 100`; NULL khi không có scored attempt.
- Metric và tombstone rules là DERIVED, cần owner xác nhận.

## Conflicts

- DISCREPANCY: statistics intent không khớp direct response `ApiEnvelope<Quiz>`; Quiz không có metric fields.
- DISCREPANCY: logical passing_score bắt buộc nhưng legacy DDL không đặt NOT NULL.
- DISCREPANCY: DB guide nói quiz_attempts.quiz_id required; legacy DDL cho phép NULL.
- DISCREPANCY: legacy BIGINT quiz model khác V1-PILOT UUID assessment model.
- SOURCE_REQUIRED: Admin permission, active schema, metric rounding và threshold/null policy.
- Middleware hiện chưa allowlist dynamic Admin quiz path; đây là conditional integration discrepancy, chưa phải behavior của route #91 vì route chưa tồn tại.

## Security note

- Xác thực Bearer và authorize Admin cùng quiz-management permission trước khi đọc dữ liệu.
- Không nhận user_id/role từ request.
- Chỉ trả aggregate; không đọc/tiết lộ answer rows, answer key hoặc Student identifiers.
- Không trả SQL, stack trace hoặc DB message.

## Performance note

- Một LEFT JOIN và aggregate theo quiz ID là candidate query đủ cho metrics đề xuất.
- Không tải answer rows; không thêm cache/index/SLA khi chưa có nguồn.
- Query plan và index live chưa được xác minh.

## Contract interpretation

- DIRECT: GET/path-only, Admin Bearer, quiz_id:int64!, ApiEnvelope<Quiz>, HTTP 200 và exact errors 401/403/404/500.
- DERIVED: QuizStatistics, metric definitions, aggregate query và tombstone visibility.
- SOURCE_REQUIRED: approved stats schema, rounding, threshold semantics, Admin policy, live DB và error wiring.
- DISCREPANCY: statistics intent không thể biểu diễn bằng schema Quiz hiện tại.

## Tình trạng nhóm AC-35

- Macro-review tài liệu #87–#91: VERIFIED_WITH_OPEN_QUESTIONS; hoàn tất sau khi có DD #91. Đây là review tài liệu, không phải owner approval hoặc xác minh runtime.
- Đề xuất DERIVED dùng chung: #90 soft-delete quiz có attempt và giữ lịch sử; #87 ẩn tombstone mặc định; #89 không sửa quiz đã tombstone hoặc có attempt/answer history; #29 chặn attempt mới sau tombstone; #30–#32 giữ khả năng xử lý/đọc attempt đã tạo; #91 tổng hợp lịch sử còn lưu; hard-delete/không có quiz row trả 404 theo contract #91.
- Giá trị tombstone, nhánh hard-delete khi chưa có attempt, xử lý attempt đang làm, status transition DRAFT → mở và cách ánh xạ lỗi vẫn cần xác nhận.
- Contract trực tiếp của từng API được giữ nguyên. #87 list/page response và #91 statistics/Quiz response vẫn là discrepancy.
- Chi tiết: [Verification Report nhóm AC-35](VERIFICATION_REPORT.md).
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
