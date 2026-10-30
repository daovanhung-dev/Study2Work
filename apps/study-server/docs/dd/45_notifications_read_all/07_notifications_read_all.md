---
title: "Định nghĩa notifications UPDATE"
order: 7
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "07_notifications_read_all"
format: markdown
dd_id: "45"
api_name: "Đánh dấu tất cả đã đọc"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table — `notifications` `UPDATE`

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | `notifications` — legacy Study schema candidate |
| Logical table | Notification và read state của direct recipient |
| Operation | Candidate `UPDATE`; design-only |
| Data Mapping step | 2 |
| Evidence | AC-20, DB guide/ERD, `infra/postgres/study-server/DB.sql`; live schema chưa xác minh |

## Update mapping

**Áp dụng khi**

- AC-20 chọn nhánh ALL và Student hiện tại có các notification unread thuộc direct recipient.
- Candidate schema đặt `user_id` trực tiếp trên notification row và dùng boolean `is_read`.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---:|---|
| 1 | `is_read` | Cờ đã đọc | `BOOLEAN` | N/A | N/A | DDL nullability unspecified | N/A | `TRUE` | API action “đánh dấu đã đọc” | 2 | DERIVED fallback; không lưu timestamp. |

### Điều kiện update

| No | Column | Operator | Value source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---|
| 1 | `user_id` | `=` | Principal ID trong Student JWT | 2 | Chỉ phạm vi direct recipient; `user_id IS NULL` bị loại. |
| 2 | `is_read` | `=` | Hằng `FALSE` | 2 | Chỉ chuyển các row đang unread; NULL không match. |

## Insert mapping

**Áp dụng khi**

- N/A — API #45 không tạo notification; tạo/gửi notification thuộc API khác.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---:|---|
| — | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | Không có INSERT. |

## Delete mapping

**Áp dụng khi**

- N/A — API #45 không xóa notification.

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---|
| — | N/A | N/A | N/A | N/A | Không có DELETE. |

## Candidate `RETURNING` projection

| No | Column | Legacy DDL type | Purpose | Evidence status |
|---:|---|---|---|---|
| 1 | `id` | `BIGSERIAL` | Notification response ID | Direct legacy candidate; pilot DDL uses UUID. |
| 2 | `title` | `VARCHAR(200)` | Notification title | Direct legacy candidate. |
| 3 | `content` | `TEXT` | Notification content | Direct legacy candidate; pilot DDL calls this `body`. |
| 4 | `created_at` | `TIMESTAMP` | Notification creation time | Direct column; timezone unresolved. |

## Physical source gaps and schema alternatives

| Contract/logical item | Candidate source | Status | Impact |
|---|---|---|---|
| `NotificationRecipient` | No table in legacy DB guide/ERD/DDL | SOURCE_REQUIRED | Broadcast/segment notifications have no per-Student read state. |
| `read_at` | Missing in legacy DDL; present on pilot `notifications` | DISCREPANCY / SOURCE_REQUIRED | Pilot `learner_id` and notification ID are UUID, unlike current principal/catalog int64. |
| `Notification.channels` | Legacy `type` is not an approved mapping; pilot delivery table has per-channel rows | SOURCE_REQUIRED | Do not map `type` or join a different schema model without decision. |
| `Notification.status` | No legacy status; pilot has per-delivery `notification_status` | SOURCE_REQUIRED | Delivery status semantics may differ from notification/read status. |
| `Notification.scheduled_at` | No physical column in the DDLs examined | SOURCE_REQUIRED | Cannot return scheduled timestamp. |
| Body/Page semantics | API catalog only declares `body{}` and `Page<Notification>` | DERIVED / OPEN_QUESTION | Empty-object validation and full changed-row Page need confirmation. |

## Candidate mapping boundary

- This is a physical candidate aligned with AC-20's API IDs and current numeric Student principal; it is not a live-schema claim.
- Candidate SQL updates `is_read=TRUE` only where `user_id` equals the principal and `is_read=FALSE`.
- It does not update the alternative V1-PILOT DDL or synthesize `read_at`.
- `RETURNING` fields only cover part of the Notification response schema; the DD remains Draft.
---
## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `table`
- Dimension: `A1:BA35`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `19`
- Số vùng merge: `5`

<details>
<summary>Danh sách vùng merge</summary>

- `W34:BA34`
- `W14:BA14`
- `W15:BA15`
- `W19:BA19`
- `W32:BA32`

</details>

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 2 | `A2` | № |  |
| 2 | `B2` | Tên table |  |
| 3 | `B3` | SB |  |
| 3 | `S3` | Độ dài |  |
| 3 | `T3` | Dấu phẩy thập phân |  |
| 3 | `U3` | Bắt buộc |  |
| 3 | `V3` | Main key |  |
| 3 | `W3` | Nội dung setting |  |
| 4 | `B4` | № |  |
| 4 | `C4` | Item ID |  |
| 4 | `I4` | Item name |  |
| 4 | `O4` | Kiểu |  |
| 5 | `A5` | 1 |  |
| 5 | `B5` | table id |  |
| 5 | `I5` | table name |  |
| 6 | `B6` | Update |  |
| 6 | `I6` | Trường hợp số record get được từ xử lý 3. của sheet [３．Data mapping]  > 0 |  |
| 21 | `B21` | Insert |  |
| 21 | `I21` | Trường hợp số record get được từ xử lý 3. của sheet [３．Data mapping]  = 0 |  |

</details>
