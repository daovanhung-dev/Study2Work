---
title: "Định nghĩa table — SupportMessage INSERT"
order: 7
dd_id: "60"
api_name: "Gửi phản hồi"
source_sheet: "table"
status: "Draft — Needs Confirmation"
---

# SupportMessage INSERT mapping

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | support_messages — API #58 checked-in legacy BIGINT fallback; live schema chưa xác minh |
| Logical table | SupportMessage |
| Operation | INSERT |
| Data Mapping step | [5.1](./05_Data_Mapping.md) |

## Update mapping

**Áp dụng khi**

- N/A — API #60 không UPDATE; API #61 sở hữu resolve/status mutation.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | API #60 không UPDATE SupportRequest. |

## Insert mapping

**Áp dụng khi**

- Local fallback: insert một support_messages row sau request scope và UploadAsset checks.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|
| 1 | id | Message ID | BIGSERIAL/BIGINT | N/A | N/A | Yes | PK | Omit; database generates | Migration 008 | 5.1 | Contract response int64; local generator only. |
| 2 | request_id | Support request ID | BIGINT | N/A | N/A | Yes | FK | Locked request.id | Path + Q1 | 5.1 | FK support_requests.id. |
| 3 | author_id | Mentor user ID | BIGINT | N/A | N/A | Yes | FK | JWT sub | Shared MENTOR guard | 5.1 | FK users.id; never client supplied. |
| 4 | content | Message content | TEXT | N/A | N/A | Yes | No | Request message, unchanged | Request body | 5.1 | Reject whitespace-only; no length rule. |
| 5 | created_at | Message creation time | TIMESTAMPTZ | N/A | N/A | Yes | No | Omit; CURRENT_TIMESTAMP default | Migration 008 | 5.1 | Returned by INSERT and reloaded in response. |

## Delete mapping

**Áp dụng khi**

- N/A — API #60 không DELETE SupportMessage.

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---:|---|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | API #60 không có DELETE. |

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
