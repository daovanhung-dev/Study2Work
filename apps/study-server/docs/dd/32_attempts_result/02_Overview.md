---
title: "Overview"
order: 2
dd_id: "32"
api_name: "Lấy điểm/kết quả được phép xem"
source_sheet: "Overview"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | 32 |
| Module | STUDENT / LEARNING & INTERACTION |
| Method | GET |
| Endpoint | /api/v1/attempts/{attempt_id}/result |
| Purpose | Đọc điểm, trạng thái chấm và kết quả được phép xem của một quiz attempt. |
| Consumer/Actor | Student |
| Authentication | Student Bearer JWT theo API catalog. |
| Authorization | Catalog yêu cầu role Student. Điều kiện sở hữu attempt, availability state và cách xử lý attempt của Student khác chưa được chốt. |
| Basis | DIRECT — API catalog và AC-16; candidate persistence mapping từ DB design. |
| Status | Draft — Needs Confirmation |
| Transaction | N/A — GET chỉ đọc theo contract. |
| Side effects | N/A — không có mutation hoặc external side effect được mô tả. |

## Sources

- [API catalog](../../../../../docs/lists/list_api.md) — method, endpoint, request, response và error codes API #32.
- [AC API index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — trace API #32 tới AC-16.
- [AC-16 activity diagram](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — hai nhánh AUTO GRADED và PENDING GRADE cùng đi tới API #32; sơ đồ ghi đọc score + feedback/status.
- [DB table map](../../diagrams/DB_UNICA_TABLES.md), [DB ERD](../../diagrams/DB_UNICA_ERD.drawio) và [checked-in DDL](../../../../../infra/postgres/study-server/DB.sql) — chỉ là design evidence.
- [API Guidelines](../../../../../contracts/api-guidelines/README.md) — envelope và error response convention.
- [Current router](../../../app/api/v1.py), [current auth helper](../../../app/utils/auth.py), [Study modules](../../../app/modules/) và [Study tests](../../../tests/) — trạng thái runtime hiện tại.

## Tables read

- quiz_attempts — candidate source cho attempt ID, owner ID, status, thời gian và aggregate score.
- quiz_answers — candidate source cho câu trả lời, correctness và score từng câu nếu được phép trả.

## Tables write

- N/A — API catalog khai báo GET; không có mutation.

## Mục chú ý

- API catalog là APPROVED_DESIGN_CONTRACT. Contract khai báo HTTP 200 DESIGN_RESOURCE_RETRIEVED; 401 DESIGN_AUTHENTICATION_REQUIRED; 403 DESIGN_ACCESS_DENIED; 404 DESIGN_RESOURCE_NOT_FOUND; 500 DESIGN_INTERNAL_ERROR.
- AC-16 gọi API #32 sau cả hai nhánh AUTO GRADED và PENDING GRADE; kết quả hiển thị có thể là điểm hoặc trạng thái đang chờ chấm.
- Reusable QuizAttempt gồm id, quiz_id, status, started_at, submitted_at?, score? và answers[]. Full AttemptStatus enum chưa được định nghĩa; AC-16 chỉ nêu PENDING_GRADE và GRADED tại bước kết quả.
- DB design mô tả quiz_attempts.score và quiz_answers.is_correct/score_received. Các bảng và cột này chưa xác nhận là live schema.
- AC-16 nhắc feedback nhưng QuizAttempt schema và các bảng ứng viên không có field/cột feedback.

## Assumptions

- Giữ nguyên API contract và error-code set hiện tại; không thêm error code hoặc response field.
- Ghi DB access như candidate mapping; không khẳng định query runtime, live schema hay serialization.
- Giữ Draft — Needs Confirmation cho tới khi các câu hỏi trong OPEN_QUESTIONS.md được chốt.

## Conflicts

- DISCREPANCY: AC-16 ghi score + feedback/status; reusable QuizAttempt không có feedback và quiz_attempts/quiz_answers cũng không có feedback column.
- SOURCE_REQUIRED: AC-16 cho cả GRADED và PENDING_GRADE đi tới API #32 nhưng không định nghĩa field nào được trả ở mỗi trạng thái hoặc điều kiện attempt được phép đọc.
- DISCREPANCY: Logical QuizAnswer có choice_ids? và text_answer?; physical design chỉ có một choice_id, không có text_answer.
- SOURCE_REQUIRED: Logical QuizAnswer có correct? và score?; quy tắc tiết lộ cho Student qua API kết quả chưa được mô tả.
- UNWIRED / NOT_FOUND: Current Study router, modules and tests không có API #32.

## Security note

- API chỉ nhận attempt_id từ path; không nhận user_id từ client.
- Current Student auth helper có thể trả user_id từ JWT, nhưng API #32 chưa được wire và policy đối chiếu quiz_attempts.user_id chưa được đặc tả.
- Không trả đáp án đúng từ quiz_choices hoặc correctness/score từng câu cho Student cho tới khi được policy nguồn xác nhận; không lộ SQL, stack trace hoặc nội dung nội bộ.
- Cách phân biệt 403 với 404 khi attempt thuộc user khác là open question.

## Performance note

- Contract đọc một attempt theo path và không khai báo pagination, cache hay latency objective.
- Số answer rows và ordering không được quy định; không tự thêm giới hạn, index hoặc thứ tự kết quả.

## Phụ thuộc AC-35 — quiz tombstone proposal

- API #32 đọc kết quả của attempt; AC-35 #90 đề xuất giữ attempt/answer history khi soft-delete quiz có attempt.
- Đề xuất DERIVED: kết quả của attempt đã tồn tại vẫn đọc được khi quiz bị tombstone; API #91 tổng hợp cùng lịch sử còn lưu.
- Quyền đọc, trạng thái attempt được phép xem và error mapping vẫn theo câu hỏi hiện hữu của AC-16.
- Câu hỏi liên quan: [API #90](../90_admin_quizzes_delete/OPEN_QUESTIONS.md) và [API #91](../91_admin_quizzes_statistics/OPEN_QUESTIONS.md).
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
