---
title: "Định nghĩa table"
order: 7
dd_id: "93"
api_name: "Tạo/phát notification"
source_sheet: "table"
format: markdown
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | notifications — legacy candidate only |
| Logical table | Admin Notification; grain unresolved |
| Operation | INSERT proposal; not executable |
| Data Mapping step | [Step 3](./05_Data_Mapping.md#step-3-create-notification) |

## Candidate legacy columns

These rows describe checked-in legacy schema only; it is not an approved API #93 target.

| No | Physical column | Type/constraint | Candidate source | Status/remarks |
|---:|---|---|---|---|
| 1 | id | BIGSERIAL PRIMARY KEY | Selected store | SOURCE_REQUIRED; allocator not verified |
| 2 | user_id | BIGINT NULL FK users.id | One recipient candidate | Does not define campaign relation |
| 3 | sender_id | BIGINT NULL FK users.id | Admin principal candidate | Principal mapping unknown |
| 4 | title | VARCHAR(200) NOT NULL | Request title | Candidate; DDL length not approved validation |
| 5 | content | TEXT NOT NULL | Request content | Candidate; target not approved |
| 6 | type | VARCHAR(30) NULL | None | Do not map NotificationChannel |
| 7 | is_read | BOOLEAN DEFAULT FALSE | None | Not NotificationStatus or read_at |
| 8 | created_at | TIMESTAMP NOT NULL | Persistence clock | DDL has no default; source unknown |

## Insert mapping

**Áp dụng khi**

- Only if an owner later selects this legacy model; this DD does not authorize it.

| No | Candidate field | Logical value | Setting/source | Step | Remarks |
|---:|---|---|---|---|---|
| 1 | title | Notification title | Request title | 3 | Candidate only |
| 2 | content | Notification content | Request content | 3 | Candidate only |
| 3 | user_id | Recipient | Request ID if one row per recipient is approved | 2, 3 | Grain unresolved |
| 4 | sender_id | Admin sender | Principal if mapping approved | 0, 3 | SOURCE_REQUIRED |
| 5 | id | Notification ID | Selected store generation | 3 | SOURCE_REQUIRED |
| 6 | type | Channel/type | No approved mapping | 3 | Do not infer |
| 7 | is_read | Read state | No approved Admin mapping | 3 | Do not infer |
| 8 | created_at | Creation time | No approved source | 3 | SOURCE_REQUIRED |

## Update mapping

N/A — API #93 does not declare UPDATE.

## Delete mapping

N/A — API #93 does not declare DELETE.

## Physical mapping boundary

- Legacy schema is a checked-in candidate, not verified live schema or approved campaign target.
- V1-PILOT UUID learner notification schema is a different model.
- No executable INSERT or physical target is approved.
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
