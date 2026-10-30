---
title: "Định nghĩa table"
order: 7
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
dd_id: "43"
api_name: "Lấy notification list"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | notifications — candidate read source |
| Logical table | Notification / người nhận thông báo |
| Operation | `SELECT` candidate only; no mutation |
| Data Mapping step | 3–5 |
| Evidence | AC-20, DB guide, ERD và checked-in DDL; live schema chưa xác minh |

## Update mapping

**Áp dụng khi**

- N/A — READ-ONLY API; không có UPDATE.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting `content` | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---:|---|
| — | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | API #43 không mutate data. |

## Insert mapping

**Áp dụng khi**

- N/A — READ-ONLY API; không có INSERT.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting `content` | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---:|---|
| — | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | API #43 không tạo notification. |

## Delete mapping

**Áp dụng khi**

- N/A — READ-ONLY API; không có DELETE.

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---|
| — | N/A | N/A | N/A | N/A | API #43 không xóa notification. |

## Candidate read projection

> DDL/ERD là design evidence trong repository, không xác nhận live schema. Các dòng này không phải SQL đã chạy hoặc mapping đã được duyệt.

| No | Table | Column | DDL `type` | Constraint | Data Mapping use | Evidence `status` |
|---:|---|---|---|---|---|---|
| 1 | notifications AS n | id | `BIGSERIAL` | Primary key | Notification ID trong item | Direct candidate |
| 2 | notifications AS n | `user_id` | `BIGINT` | Nullable FK → users.id | Candidate principal filter | DERIVED; NULL/broadcast behavior unresolved |
| 3 | notifications AS n | `sender_id` | `BIGINT` | Nullable FK → users.id | Không dùng trong API #43 projection | Direct schema fact |
| 4 | notifications AS n | `title` | `VARCHAR(200)` | NOT NULL | Notification `title` | Direct candidate |
| 5 | notifications AS n | `content` | `TEXT` | NOT NULL | Notification `content` | Direct candidate |
| 6 | notifications AS n | `type` | `VARCHAR(30)` | Nullable | Không map sang `channels` hoặc `status` | Direct schema fact; response mapping unsupported |
| 7 | notifications AS n | `is_read` | `BOOLEAN` | Default FALSE | Predicate khi `unread_only`=true | Direct candidate; không map sang `read_at`/`status` |
| 8 | notifications AS n | `created_at` | `TIMESTAMP` | NOT NULL | Page order và response candidate | Timezone semantics SOURCE_REQUIRED |

## Physical source gaps

| Contract/logical item | Physical source | Status | Impact |
|---|---|---|---|
| `NotificationRecipient` | Không có table trong DB guide, ERD hoặc DDL | SOURCE_REQUIRED | Chưa biểu diễn được delivery/read state theo từng recipient cho broadcast. |
| Notification.channels[] | Không có cột `channels` hoặc enum definition | SOURCE_REQUIRED | Không map từ `type` nếu chưa có quyết định. |
| Notification.status | Không có cột `status` hoặc enum definition | SOURCE_REQUIRED | Không suy từ `type`/`is_read`. |
| Notification.read_at | Không có cột timestamp; chỉ có `is_read` | SOURCE_REQUIRED | Boolean không xác định thời điểm đọc. |
| Notification.scheduled_at | Không có cột | SOURCE_REQUIRED | Không thể trả physical timestamp. |

## Query boundary

- Q1/Q2 chỉ đọc candidate table notifications.
- Predicate n.user_id = `principal_id` là DERIVED để cô lập dữ liệu theo `Student`.
- `unread_only`=true chỉ dùng `n.is_read = FALSE` làm filter candidate.
- Page size 20 và order `created_at` DESC, id DESC là DERIVED; không tạo index hoặc schema mới.
- `NotificationRecipient` không được giả lập thành physical table.
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
