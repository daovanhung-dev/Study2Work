---
title: "Overview"
order: 2
dd_id: "29"
api_name: "Tạo attempt"
source_sheet: "Overview"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | 29 |
| Module | STUDENT / LEARNING & INTERACTION |
| Method | POST |
| Endpoint | /api/v1/quizzes/{quiz_id}/attempts |
| Purpose | Tạo một lần làm bài kiểm tra cho quiz theo AC-16. |
| Consumer/Actor | Student |
| Authentication | Bearer JWT theo API catalog. |
| Authorization | Catalog yêu cầu role Student. Điều kiện enrollment, quiz open, giới hạn lượt và hạn làm bài chưa được định nghĩa. |
| Basis | DIRECT — API catalog và AC-16; candidate persistence mapping từ DB design/DDL. |
| Status | Draft — Needs Confirmation |
| Transaction | TBD — current runtime implementation chưa tồn tại. |
| Side effects | Candidate INSERT vào quiz_attempts; chưa runtime-verified. |

## Sources

- [API catalog](../../../../../docs/lists/list_api.md) — API #29 contract, schema QuizAttempt và business code.
- [AC API index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — AC-16 actor, precondition và postcondition.
- [AC-16 activity diagram](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — create-attempt branch, trạng thái IN_PROGRESS và nhánh lỗi exhausted/expired.
- [DB table design](../../diagrams/DB_UNICA_TABLES.md) và [DB ERD](../../diagrams/DB_UNICA_ERD.drawio) — candidate quiz_attempts fields/relations; design-only.
- [Checked-in DB DDL](../../../../../infra/postgres/study-server/DB.sql) — candidate physical DDL; không xác nhận live schema.
- [Current Study router](../../../app/api/v1.py), [modules](../../../app/modules/) và [tests](../../../tests/) — kiểm tra current wiring.
- [API guidelines](../../../../../contracts/api-guidelines/README.md) — ApiEnvelope/error response conventions.
- [API #28 open questions](../28_quizzes_detail/OPEN_QUESTIONS.md) — eligibility ownership and AC-16 branch ambiguity already identified.

## Tables read

- quizzes — candidate lookup for quiz existence or eligibility; exact query and predicate are not defined.
- No user lookup is specified; authenticated Student identity is required for the candidate quiz_attempts.user_id value, but claim mapping is SOURCE_REQUIRED.

## Tables write

- quiz_attempts — candidate INSERT for the new attempt.
- No quiz_answers INSERT is specified for attempt creation.

## Mục chú ý

- API catalog is APPROVED_DESIGN_CONTRACT, not runtime evidence. It specifies Student Bearer JWT, path quiz_id:int64!, ApiEnvelope<QuizAttempt>, and HTTP/business codes 201, 401, 403, 404, 422, 409 and 500.
- AC-16 activity diagram labels the create flow as INSERT Attempt = IN_PROGRESS.
- AC-16 puts the eligibility decision after reading quiz/rules/questions, but does not identify whether API #28 or API #29 owns that check.
- The catalog lists both 403 DESIGN_ACCESS_DENIED and 409 DESIGN_STATE_CONFLICT for API #29. AC-16 says exhausted/expired attempts lead to 403/409 without assigning each condition to a code.
- DB_UNICA_TABLES.md describes quiz_attempts.quiz_id and user_id as required references; checked-in DB.sql declares nullable foreign keys. Live metadata is not verified.
- Logical QuizAttempt requires answers:QuizAnswer[]. AC-16 does not define whether the create response includes an empty answers array or another initial representation.

## Assumptions

- No unverified eligibility, attempt-count, expiry, identity-claim, transaction or response-nullability rule is treated as settled.
- Candidate persistence fields are documented as design evidence only.

## Conflicts

- SOURCE_REQUIRED: Student entitlement, quiz-open predicate, attempt limit, expiry and ownership of the AC-16 eligibility check are undefined.
- DISCREPANCY: AC-16 groups exhausted/expired conditions under 403/409, while API #29 catalog lists both codes without mapping the conditions.
- DISCREPANCY / DESIGN_ONLY: DB table design marks quiz_id and user_id required, while checked-in DDL permits NULL references.
- SOURCE_REQUIRED: QuizAttempt.answers is required in the logical response schema, but the initial response value is not specified.

## Security note

- Do not accept user_id from the request; API catalog defines only quiz_id in the path and Student identity comes from Bearer authentication.
- The exact JWT claim used to populate candidate quiz_attempts.user_id is not part of API #29's contract and remains SOURCE_REQUIRED.
- Do not expose quiz answer keys or internal database details in this response.

## Performance note

- The contract has no pagination or latency/cache requirement.
- No query plan, concurrency policy or attempt deduplication rule is defined.


## Phụ thuộc AC-35 — quiz tombstone proposal

- AC-16 yêu cầu quiz đang mở trước khi tạo attempt; AC-35 #90 yêu cầu soft-delete khi quiz đã có attempt.
- Đề xuất DERIVED: không tạo attempt mới cho quiz đã tombstone; status value, điều kiện quiz-open cụ thể và ánh xạ lỗi 403/404/409/422 chưa được chốt.
- Không thay catalog hoặc tự coi DELETED là enum đã duyệt.
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
