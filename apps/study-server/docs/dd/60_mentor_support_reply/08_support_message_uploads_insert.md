---
title: "Định nghĩa table — SupportMessageUpload INSERT"
order: 8
dd_id: "60"
api_name: "Gửi phản hồi"
source_sheet: "table"
status: "Draft — Needs Confirmation"
---

# SupportMessageUpload INSERT mapping

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | support_message_uploads — API #58 checked-in legacy BIGINT fallback; live schema chưa xác minh |
| Logical table | Ordered SupportMessage-to-UploadAsset relation |
| Operation | INSERT khi attachment_refs không rỗng |
| Data Mapping step | [6.1](./05_Data_Mapping.md) |

## Update mapping

**Áp dụng khi**

- N/A — API #60 không UPDATE attachment links.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | API #60 không UPDATE links. |

## Insert mapping

**Áp dụng khi**

- Insert one row per validated UploadAsset, in the request array order.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|
| 1 | message_id | Support message ID | BIGINT | N/A | N/A | Yes | PK/FK | M1 returned message ID | INSERT support_messages | 6.1 | Composite primary key with upload_id. |
| 2 | upload_id | UploadAsset ID | BIGINT | N/A | N/A | Yes | PK/FK | Validated attachment_refs item | Request + Q2 | 6.1 | FK uploads.id; owner/course/purpose/status validated first. |
| 3 | asset_position | Zero-based position | BIGINT | N/A | N/A | Yes | Unique with message_id | Array ordinality - 1 | JSON array order | 6.1 | Must be nonnegative and unique per message. |

## Delete mapping

**Áp dụng khi**

- N/A — API #60 không DELETE attachment links.

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
