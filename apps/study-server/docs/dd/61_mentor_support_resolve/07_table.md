---
title: "Định nghĩa table"
order: 7
dd_id: "61"
api_name: "Đóng yêu cầu hỗ trợ"
source_sheet: "table"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | `support_tickets` (V1-PILOT candidate; chưa được duyệt/live) |
| Logical table | SupportRequest |
| Operation | Candidate M1: UPDATE |
| Data Mapping step | [5.1–5.3](./05_Data_Mapping.md) |

> Legacy Study DB.sql/ERD không có SupportRequest table. V1-PILOT ID là UUID, còn API contract yêu cầu int64; mapping dưới đây chỉ mô tả candidate DDL để làm lộ gap, không phải SQL triển khai.

## Update mapping

**Áp dụng khi**

- Candidate trạng thái hiện tại là `OPEN` và Mentor có quyền trên request.
- Request đang `RESOLVED` thì theo DERIVED proposal không chạy UPDATE, trả success và giữ `resolved_at` ban đầu.
- State khác `OPEN`/`RESOLVED` không UPDATE; 422 là DERIVED proposal, enum API cần được xác nhận.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|
| 1 | `id` | Support request ID | uuid | N/A | N/A | Yes | PK | Candidate match với logical `request_id` | V1-PILOT DDL | 4.1 | API contract là int64; không cast UUID; WHERE predicate chưa thể chốt. |
| 2 | `assigned_to_subject_id` | Mentor được gán | uuid? | N/A | N/A | No | No | Candidate đối chiếu với Mentor principal | V1-PILOT DDL | 2.2 | Cột nullable; JWT subject mapping và authorization policy chưa được duyệt. |
| 3 | `status` | Request status | varchar(24) | 24 | N/A | Yes | No | `RESOLVED` khi status hiện tại là `OPEN` | AC-24 + V1-PILOT candidate | 5.1–5.2 | Giá trị RESOLVED có trong diagram/DDL; allowed transition API chưa được duyệt. |
| 4 | `resolved_at` | Resolution time | timestamptz? | N/A | N/A | No | No | Server/database current timestamp khi chuyển OPEN → RESOLVED | V1-PILOT candidate + DERIVED | 5.2 | Sơ đồ không nêu timestamp; set time/null/omit policy cần xác nhận. |
| 5 | `updated_at` | Record update time | timestamptz | N/A | N/A | Yes | No | Auto-set bởi candidate trigger `s2w_touch_entity()` | V1-PILOT DDL | 5.2 | Trigger body đặt `now()`; không phải API field. |
| 6 | `row_version` | Record version | bigint | N/A | N/A | Yes | No | Auto-increment bởi candidate trigger | V1-PILOT DDL | 5.2 | Trigger tăng OLD.row_version + 1; live schema chưa xác nhận. |

## Insert mapping

**Áp dụng khi**

- N/A — API #61 không INSERT. API #60 sở hữu logical `INSERT SupportMessage`.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | Không tạo message ở API #61. |

## Delete mapping

**Áp dụng khi**

- N/A — API #61 không DELETE hoặc soft-delete request.

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---:|---|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | API #61 chỉ resolve status theo AC-24. |
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
