---
title: "Định nghĩa table"
order: 7
dd_id: "60"
api_name: "Gửi phản hồi"
source_sheet: "table"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | `support_messages` (V1-PILOT candidate; chưa được duyệt/live) |
| Logical table | SupportMessage |
| Operation | Candidate M1: INSERT |
| Data Mapping step | [5.1](./05_Data_Mapping.md) |

## Update mapping

**Áp dụng khi**

- N/A — API #60 không UPDATE; #61 là API đổi SupportRequest status.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | Không có UPDATE tại API #60. |

## Insert mapping

**Áp dụng khi**

- Candidate V1-PILOT mapping để trình bày physical gaps; không phải schema runtime đã duyệt.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|
| 1 | id | Message ID | uuid | N/A | N/A | Yes | PK | SOURCE_REQUIRED | Generator chưa có default | 5.1 | API contract yêu cầu int64; pilot UUID mismatch. |
| 2 | created_at | Record creation time | timestamptz | N/A | N/A | Yes | No | Omit column; pilot DB default now() | V1-PILOT DDL | 5.1 | Candidate metadata; live schema chưa xác nhận. |
| 3 | ticket_id | Support request ID | uuid | N/A | N/A | Yes | FK | SOURCE_REQUIRED | request_id int64 không map trực tiếp | 5.1 | Pilot FK tới support_tickets.id. |
| 4 | author_subject_id | Mentor subject ID | uuid | N/A | N/A | Yes | No | SOURCE_REQUIRED | JWT subject mapping chưa rõ | 5.1 | Không tin ID do client gửi; không có body field này. |
| 5 | author_type | Author type | varchar(16) | 16 | N/A | Yes | No | `STAFF` candidate | DERIVED từ Mentor action | 5.1 | Pilot cho phép LEARNER/STAFF; mapping cần confirm. |
| 6 | body | Message body | text | N/A | N/A | Yes | No | `message` request field | Catalog + pilot candidate | 5.1 | Reject blank/whitespace là DERIVED; length không đặt. |
| 7 | attachment_file_ids | Attached file IDs | uuid[] | N/A | N/A | Yes | No | Resolve refs sang UUIDs | API #34 resolver SOURCE_REQUIRED | 5.1 | Catalog proposes UploadAsset int64 refs; pilot UUID[] mismatch. |
| 8 | is_internal | Internal-message flag | boolean | N/A | N/A | Yes | No | `false` candidate | V1-PILOT default false | 5.1 | Learner-visible reply interpretation DERIVED. |
| 9 | sent_at | Message time | timestamptz | N/A | N/A | Yes | No | Server-generated time | Generator/clock SOURCE_REQUIRED | 5.1 | Pilot no default; timezone/clock rule unresolved. |

## Delete mapping

**Áp dụng khi**

- N/A — API #60 không DELETE; support message immutability candidate không được dùng để suy diễn delete flow.

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
