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
| Purpose | Đánh dấu SupportRequest đã được xử lý sau khi Mentor gửi reply trong AC-24. |
| Consumer/Actor | Mentor |
| Authentication | Bearer JWT |
| Authorization | Role Mentor; chỉ được resolve request trong phạm vi phụ trách. Cách ánh xạ principal và assignment chưa có runtime source. |
| Basis | Catalog và nhánh YES của AC-24 là DIRECT; xử lý idempotent, timestamp và state guard là DERIVED. |
| Status | Draft — Needs Confirmation |
| Transaction | Đề xuất đọc/check, đổi status, reload response trong một transaction do use case sở hữu. |
| Side effects | Logical UPDATE SupportRequest.status = RESOLVED; không thêm hoặc sửa SupportMessage. |

## Sources

- [API catalog và reusable schemas](../../../../../docs/lists/list_api.md).
- [AC/API index, AC-24](../../diagrams/AC_UNICA/00_AC_API_INDEX.md).
- [AC-24 flow diagram](../../diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio).
- [API #58 — danh sách support requests](../58_mentor_support_requests/02_Overview.md).
- [API #59 — request/thread](../59_mentor_support_request_detail/02_Overview.md).
- [API #60 — gửi reply](../60_mentor_support_reply/02_Overview.md).
- [V1-PILOT Study DDL](../../../../../infra/postgres/02_study_db.sql).
- [Current Study router](../../../../../apps/study-server/app/api/v1.py).
- [Current DB helper](../../../../../apps/study-server/app/core/database.py).
- [Current response helper](../../../../../apps/study-server/app/core/responses.py).
- [API Guidelines](../../../../../contracts/api-guidelines/README.md).
- [Study API DD workflow](../../../../../.agents/server-study/workflows/README.md).

## Tables read

- Chưa có SupportRequest table được chọn làm nguồn runtime.
- V1-PILOT `support_tickets` là physical candidate có `id`, `status`, `assigned_to_subject_id`, `resolved_at`, `updated_at`, `row_version`; ID UUID không khớp contract int64.
- `support_messages` chỉ được tham chiếu để giữ ranh giới với API #60; #61 không ghi bảng này.

## Tables write

- Logical target theo AC-24: SupportRequest, cập nhật `status = RESOLVED`.
- Candidate physical table: V1-PILOT `support_tickets`; không được khẳng định là live/approved.
- `resolved_at` theo server time là đề xuất DERIVED từ field optional trong contract và cột candidate.
- Không ghi `resolution_code`, `cancelled_at` hoặc message rows.

## Mục chú ý

- API #61 chỉ được gọi ở nhánh YES sau khi #60 đã thêm reply; nhánh NO không gọi #61 và giữ request ở `OPEN` theo sơ đồ.
- Đề xuất đơn giản: `OPEN` → `RESOLVED`; gọi lặp khi đã `RESOLVED` trả thành công mà không ghi đè `resolved_at`; trạng thái khác trả 422. Đây là DERIVED proposal, cần xác nhận cùng SupportStatus enum.
- `request_id:int64` và SupportRequest contract không khớp UUID trong V1-PILOT. Không cast hoặc tạo SQL vật lý giả định.
- Response vẫn là một `SupportRequest`, dùng cùng projection với #59/#60. Các trường student, course và messages/assets vẫn `SOURCE_REQUIRED` cho đến khi model/resolver được duyệt.
- Error `data:null` theo API Guidelines khác current helper mặc định `{}`; support route hiện chưa wired.

## Assumptions

| ID | Đề xuất | Cơ sở | Trạng thái |
|---|---|---|---|
| A-61-01 | Lần đầu chỉ cho transition từ `OPEN` sang `RESOLVED`. | AC-24 ghi nhánh NO giữ `OPEN` và nhánh YES resolve. | DERIVED — cần xác nhận |
| A-61-02 | Gọi lại khi trạng thái đã `RESOLVED` là idempotent thành công; giữ nguyên thời điểm resolved đầu tiên. | Retry của PATCH không nên làm lỗi sau khi lần đầu đã thành công. | DERIVED — cần xác nhận |
| A-61-03 | Khi chuyển trạng thái, gán `resolved_at` bằng thời gian server. | Hợp lý với field `resolved_at` trong contract và cột cùng tên ở pilot DDL. | DERIVED — cần xác nhận |
| A-61-04 | Trạng thái khác `OPEN`/`RESOLVED` bị từ chối bằng 422. | Contract có 422; không coi enum pilot là API enum đã duyệt. | DERIVED — cần xác nhận |

## Conflicts

| Nguồn A | Nguồn B | Xung đột | Ảnh hưởng |
|---|---|---|---|
| Catalog yêu cầu `request_id:int64` và SupportRequest `id:int64`. | V1-PILOT `support_tickets.id` là UUID. | Không có ánh xạ khóa đã duyệt. | Chưa thể chốt predicate UPDATE. |
| AC-24 chỉ nêu đổi status. | SupportRequest có `resolved_at?`; pilot có cột `resolved_at`. | Thời điểm ghi và nguồn thời gian chưa được AC phê duyệt. | Giữ timestamp như proposal, không coi là DIRECT. |
| API Guidelines dùng error `data:null`. | Current helper mặc định `{}` khi không truyền data. | Expected/current serialization khác nhau. | Future wiring cần quyết định/cập nhật thống nhất. |

## Security note

- Kiểm tra Bearer và role Mentor trước khi thay đổi dữ liệu.
- Chỉ Mentor có quyền với request trong scope được phép resolve; không lấy path ID làm bằng chứng ownership.
- Predicate assignment và thứ tự phân biệt 403/404 còn cần chính sách xác nhận.

## Performance note

- Response là một SupportRequest/thread; #59/#60 chưa có giới hạn hoặc resolver được duyệt cho messages/assets.
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
