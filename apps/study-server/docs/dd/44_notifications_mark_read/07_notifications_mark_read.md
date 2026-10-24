---
title: "Định nghĩa `notifications` `UPDATE`"
order: 7
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
dd_id: "44"
api_name: "Đánh dấu một thông báo đã đọc"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table — `notifications` `UPDATE`

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | `notifications` |
| Logical table | `Notification` và read state của direct recipient |
| Operation | Candidate `UPDATE`; design-only |
| Data Mapping step | 3 |
| Evidence | AC-20 nhánh ONE, DB guide/ERD và checked-in DDL; live schema chưa xác minh |

## Update mapping

**Áp dụng khi**

- AC-20 chọn nhánh ONE và API #44 nhận đúng notification ID cùng `Student` principal.
- Đây là candidate mapping vào cột hiện có; AC diagram yêu cầu `NotificationRecipient`.`read_at` nhưng schema không có recipient table/read timestamp.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting `content` | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---:|---|
| 1 | `is_read` | Cờ đã đọc | `BOOLEAN` | N/A | N/A | DDL nullability unspecified; set non-null `TRUE` |  | `TRUE` | Candidate mapping từ AC-20 action tới column hiện có | 3 | `DERIVED` fallback; không lưu `read_at`. |

### Điều kiện update

| No | Column | Operator | Value source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---|
| 1 | id | = | Path `notification_id` | 3 | Chỉ nhắm đúng notification được yêu cầu. |
| 2 | `user_id` | = | Principal ID trong `Student` `JWT` | 3 | Owner gate `DERIVED`; row broadcast NULL không match. |

## Insert mapping

**Áp dụng khi**

- N/A — API #44 chỉ đánh dấu notification đã đọc; API tạo/gửi notification nằm ngoài scope.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting `content` | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---:|---|
| — | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | Không có INSERT. |

## Delete mapping

**Áp dụng khi**

- N/A — API #44 không xóa notification.

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---|
| — | N/A | N/A | N/A | N/A | Không có DELETE. |

## Candidate `RETURNING` projection

| No | Column | DDL type | Purpose | Evidence `status` |
|---:|---|---|---|---|
| 1 | id | `BIGSERIAL` | `Notification` response ID | Direct candidate |
| 2 | `title` | `VARCHAR(200)` | `Notification` `title` | Direct candidate |
| 3 | `content` | TEXT | `Notification` `content` | Direct candidate |
| 4 | `created_at` | `TIMESTAMP` | `Notification` creation time | Source direct; timezone unresolved |

## Physical source gaps

| Contract/logical item | Physical source | Status | Impact |
|---|---|---|---|
| `NotificationRecipient` | No table in DB guide, ERD or checked-in DDL | `SOURCE_REQUIRED` | Cannot store per-recipient read state for broadcast/segment `notifications`. |
| `read_at` | No timestamp column; only `notifications`.`is_read` boolean | DISCREPANCY / `SOURCE_REQUIRED` | Candidate boolean update does not satisfy the diagram's timestamp action. |
| `Notification`.`channels` | No physical field/enum; table has type | `SOURCE_REQUIRED` | Do not map type without approved rule. |
| `Notification`.`status` | No physical field/enum | `SOURCE_REQUIRED` | Do not infer `status` from `is_read`. |
| `Notification`.`scheduled_at` | No physical field | `SOURCE_REQUIRED` | Cannot return physical scheduled timestamp. |

## Candidate mapping boundary

- Checked-in DDL and ERD are design artifacts; live database schema was not inspected.
- Direct row ownership through nullable `notifications`.`user_id` is a `DERIVED` candidate.
- `is_read`=`TRUE` is state-idempotent but differs from `NotificationRecipient`.`read_at`.
- Required response `channels`/`status`, optional timestamps and `page` semantics remain unresolved.
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
