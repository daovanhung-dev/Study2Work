---
title: "Overview"
order: 2
dd_id: "30"
api_name: "Autosave/lưu câu trả lời"
source_sheet: "Overview"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | 30 |
| Module | Student / Assessment |
| Method | PUT |
| Endpoint | /api/v1/attempts/{attempt_id}/answers |
| Purpose | Autosave một câu trả lời thuộc quiz attempt của Student. |
| Consumer/Actor | Student |
| Authentication | Bearer JWT. |
| Authorization | Role Student theo API catalog; quy tắc ownership và trạng thái attempt chưa được đặc tả cho API #30. |
| Basis | DIRECT — API catalog là APPROVED_DESIGN_CONTRACT; AC-16 mô tả autosave qua UPSERT AttemptAnswer. |
| Status | Draft — Needs Confirmation |
| Transaction | TBD — thao tác upsert và transaction boundary chưa được định nghĩa. |
| Side effects | Candidate INSERT/UPDATE vào quiz_answers; mapping vật lý chưa được chốt. |

## Sources

- [docs/lists/list_api.md](../../../../../docs/lists/list_api.md) — API #30, ApiEnvelope, QuizAttempt, QuizAnswer và business codes.
- [00_AC_API_INDEX.md](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — actor, precondition và các API của AC-16.
- [AC_02_STUDENT_LEARNING.drawio](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — AC-16 ghi bước UPSERT AttemptAnswer sau khi Student trả lời.
- [DB_UNICA_TABLES.md](../../diagrams/DB_UNICA_TABLES.md) và [DB_UNICA_ERD.drawio](../../diagrams/DB_UNICA_ERD.drawio) — candidate relationship/schema cho quiz answers.
- [DB.sql](../../../../../infra/postgres/study-server/DB.sql) — checked-in design DDL; không xác nhận live schema.
- [auth.py](../../../../../apps/study-server/app/utils/auth.py) — helper hiện tại xác thực Student và ánh xạ JWT sub thành numeric user ID.
- [29_quizzes_attempts](../29_quizzes_attempts/00_Cover.md) — DD liền trước trong cùng AC-16.

## Tables read

- quiz_attempts — candidate attempt, quiz, owner và status lookup.
- quiz_questions — candidate question-to-quiz relationship.
- quiz_choices — candidate relationship nếu answer được chốt là choice-based.
- quiz_answers — candidate upsert target; physical shape chưa khớp đầy đủ contract answer.

## Tables write

- quiz_answers — candidate target theo DB table map và quan hệ UPSERT AttemptAnswer trong AC-16.

## Mục chú ý

- Request giữ nguyên cách ghi answer(s):string! của API catalog; key JSON thực tế và cách biểu diễn đáp án chưa được xác nhận.
- Logical QuizAnswer cho phép choice_ids hoặc text_answer, trong khi physical quiz_answers chỉ có một choice_id.
- AC-16 đặt bước nộp/chấm bài sau API #30 tại API #31; checked-in DDL lại yêu cầu quiz_answers.is_correct NOT NULL mà API #30 không nhận giá trị chấm.
- API #30 chưa có route/module/test trong Study Server hiện tại.

## Assumptions

- Đây là DD design-only theo workflow Study Server; trạng thái giữ Draft — Needs Confirmation và không tạo ZIP.
- application/json được dùng như media type dự thảo cho body có cấu trúc; API catalog không ghi rõ Content-Type.
- Có thể dùng helper auth hiện tại để lấy user ID từ JWT sub; chưa có bằng chứng API #30 gọi helper đó.

## Conflicts

- API catalog body answer(s):string! chưa ánh xạ được sang logical QuizAnswer.choice_ids / text_answer.
- DB design yêu cầu quiz_answers.choice_id, is_correct; DDL cho phép FK null nhưng yêu cầu is_correct NOT NULL. ERD/DDL không có trường text answer hay unique key cho cặp attempt/question.
- Diagram nói UPSERT AttemptAnswer nhưng không định nghĩa natural key, update condition hoặc concurrency behavior.

## Security note

- Không nhận user_id từ request; current Study helper lấy numeric ID từ JWT sub.
- Ownership check và cách ánh xạ attempt không thuộc Student sang 403 hay 404 chưa được chốt.
- Không đưa correct hoặc score vào response autosave nếu chưa có contract cho phép; tránh tiết lộ đáp án/chấm điểm.

## Performance note

- AC-16 mô tả autosave nhưng không đặt ngưỡng tần suất, batching, retry hoặc latency.
- Không chọn chiến lược chống ghi đồng thời khi chưa có unique key hoặc concurrency policy.

## Phụ thuộc AC-35 — quiz tombstone proposal

- API #30 ghi answer cho attempt đã tồn tại; AC-35 #90 giữ attempt/answer history khi soft-delete quiz có attempt.
- Đề xuất DERIVED: attempt IN_PROGRESS được tạo trước tombstone có thể tiếp tục autosave để không làm mất câu trả lời; owner cần xác nhận.
- Chưa chốt phối hợp transaction/lock giữa autosave và API #90; không thêm status/error behavior ngoài catalog.
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

