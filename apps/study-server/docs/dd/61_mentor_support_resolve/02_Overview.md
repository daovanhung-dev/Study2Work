---
title: "Overview"
order: 2
dd_id: "61"
api_name: "Đóng yêu cầu hỗ trợ"
source_sheet: "Overview"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | 61 |
| Module | MENTOR / TEACHING & SUPPORT |
| Method | PATCH |
| Endpoint | `/api/v1/mentor/support/{request_id}/resolve` |
| Purpose | Mentor đánh dấu yêu cầu hỗ trợ đã được xử lý theo nhánh YES của AC-24. |
| Consumer/Actor | Mentor |
| Authentication | Bearer JWT; shared guard yêu cầu role `MENTOR`, numeric JWT `sub`. |
| Authorization | Request thuộc course có `courses.mentor_id = JWT sub`. Đây là fallback `DERIVED` đang dùng nhất quán ở API #58–#60. |
| Basis | Route, path, response và error codes theo catalog; hiệu ứng status theo AC-24; mapping physical/state/timestamp theo nguồn local và quyết định `DERIVED`. |
| Status | Draft — Needs Confirmation |
| Transaction | Khóa request, cập nhật trạng thái, dựng full thread response, validate envelope rồi caller commit một lần. |
| Side effects | `support_requests.status = RESOLVED`; lần đầu set `resolved_at` bằng DB `CURRENT_TIMESTAMP`; không ghi message. |

## Sources

- [API catalog và reusable schemas](../../../../../docs/lists/list_api.md).
- [AC/API index, AC-24](../../diagrams/AC_UNICA/00_AC_API_INDEX.md).
- [AC-24 flow diagram](../../diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio).
- [Local support migration 008](../../../../../infra/postgres/study-server/migrations/008_support_requests.sql) và [Study DB.sql](../../../../../infra/postgres/study-server/DB.sql).
- [API #58 — danh sách support requests](../58_mentor_support_requests/02_Overview.md).
- [API #59 — request/thread](../59_mentor_support_request_detail/02_Overview.md).
- [API #60 — gửi reply](../60_mentor_support_reply/02_Overview.md).
- [Current Study router](../../../../../apps/study-server/app/api/v1.py).
- [Current DB helper](../../../../../apps/study-server/app/core/database.py).
- [Current response helper](../../../../../apps/study-server/app/core/responses.py).
- [API Guidelines](../../../../../contracts/api-guidelines/README.md).
- [Study API DD workflow](../../../../../.agents/server-study/workflows/README.md).

## Tables read

- `support_requests`: `id`, `course_id`, `student_id`, `status`, `created_at`, `resolved_at`.
- `courses`: `id`, `mentor_id`; owner predicate dùng numeric Mentor JWT `sub`.
- `users`: student public fields cho SupportRequest.
- `support_messages`, `support_message_uploads`, `uploads`, `users`: thread và attachment projection theo API #59.

## Tables write

- Local source mapping: `support_requests.status` và `support_requests.resolved_at`.
- Transition `OPEN`, `IN_PROGRESS`, hoặc `WAITING_LEARNER` → `RESOLVED`; `RESOLVED` giữ nguyên timestamp; `CANCELLED` bị từ chối 422. Đây là lựa chọn `DERIVED` dựa trên trạng thái có trong migration 008 và nhánh YES AC-24.
- Không ghi `resolution_code`, `cancelled_at`, `support_messages` hoặc attachment links.
- Migration/DDL chỉ là checked-in source; không chứng minh schema đã áp dụng ở live database.

## Mục chú ý

- AC-24: sau reply #60, câu trả lời YES gọi #61; câu trả lời NO giữ request `OPEN` và không gọi #61.
- Mapping khóa BIGINT, `course_id`, và direct course owner dùng đúng local fallback hiện có trong #58–#60; không dùng V1-PILOT UUID `support_tickets`.
- Response là một `SupportRequest`, reuse model và projection chung từ #58/#59; messages được đọc theo `created_at ASC, id ASC`, attachment metadata theo resolver hiện tại.
- Status set, idempotency, timestamp source và hành vi 422 cho `CANCELLED` là `DERIVED`, chưa phải business approval.
- `error_response` hiện trả `data: null`; lỗi validation dùng `meta.fieldErrors`.

## Assumptions

| ID | Quyết định triển khai | Cơ sở | Trạng thái |
|---|---|---|---|
| A-61-01 | Dùng local BIGINT `support_requests.id`, FK `course_id`, numeric user IDs. | Migration 008 và các API #58–#60 hiện tại. | DERIVED local fallback; live schema chưa xác minh |
| A-61-02 | Mentor scope là `courses.mentor_id = numeric JWT sub`. | Shared Mentor guard và #58–#60. | DERIVED local fallback |
| A-61-03 | Ba trạng thái active chuyển sang `RESOLVED`; `RESOLVED` lặp lại là success; `CANCELLED` trả 422. | Local status check và AC-24 YES/NO. | DERIVED |
| A-61-04 | Gán `resolved_at = CURRENT_TIMESTAMP` một lần và giữ nguyên khi retry. | Local nullable timestamp column và idempotent update. | DERIVED |
| A-61-05 | Request không tồn tại trả 404; request tồn tại ngoài owner scope trả 403. | Catalog errors và API #59/#60. | DERIVED from current local convention |

## Discrepancies

| Nguồn A | Nguồn B | Khác biệt | Cách xử lý |
|---|---|---|---|
| Catalog yêu cầu numeric int64 SupportRequest ID; local migration 008/API #58–#60 dùng BIGINT. | V1-PILOT `support_tickets.id` là UUID. | Hai physical models không tương thích. | Theo nguồn local đang chạy trong source; không cast UUID; live schema vẫn chưa xác minh. |
| AC-24 chỉ nói đổi status. | Migration có ba active states, `RESOLVED`, `CANCELLED`, và `resolved_at`. | Pre-state, retry và timestamp không được diagram định nghĩa. | Dùng ma trận DERIVED trong Data Mapping; giữ Draft status. |

## Security note

- Shared guard kiểm tra Bearer JWT và role Mentor trước DB access.
- Chỉ cho phép thao tác theo `courses.mentor_id`; request không phải bằng chứng ownership.
- Phân loại missing 404 trước owner mismatch 403 theo API #59/#60.

## Performance note

- Request row được khóa trong transaction; response thread đọc bằng query owner-scoped dùng chung với #59.
- Không thêm pagination, notification, audit field hoặc message mutation vào #61.

## Trạng thái liên quan

- [Plan và ma trận nguồn](./PLAN_RESULT.md).
- [Open Questions](./OPEN_QUESTIONS.md).
- [Verification report](./VERIFICATION_REPORT.md).
- [AC-24 macro-review #58–#61](./PLAN_RESULT.md#macro-review-ac-24-58-61).
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
