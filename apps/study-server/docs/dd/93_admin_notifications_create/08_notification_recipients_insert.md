---
title: "Recipient association insert mapping"
order: 8
dd_id: "93"
api_name: "Tạo/phát notification"
source_sheet: "additional logical mutation mapping"
format: markdown
status: "Draft — Needs Confirmation"
---

# Recipient association — logical INSERT mapping

## Mapping metadata

| Property | Value |
|---|---|
| Physical table | SOURCE_REQUIRED — compatible relation not found |
| Logical entity | Notification-to-recipient association |
| Operation | INSERT proposal; not executable |
| Data Mapping step | [Step 2](./05_Data_Mapping.md#step-2-resolve-audience) and [Step 3](./05_Data_Mapping.md#step-3-create-notification) |

## Logical input mapping

| No | Logical value | Source | Physical column | Type/constraint | Status |
|---:|---|---|---|---|---|
| 1 | Notification reference | Created logical Notification ID | SOURCE_REQUIRED | SOURCE_REQUIRED | ID relationship unknown |
| 2 | Recipient reference | recipients[] or segment expansion | SOURCE_REQUIRED | SOURCE_REQUIRED | No approved table/key |
| 3 | Segment reference | Request segment | SOURCE_REQUIRED | SOURCE_REQUIRED | Enum/storage unknown |

## Candidate evidence

- Legacy notifications.user_id stores one nullable recipient per row; it does not define a campaign association table.
- V1-PILOT learner notifications use UUID and are not the Admin campaign relation.
- AC-36 requires Notification + recipients but names no tables, keys, uniqueness, or partial-write behavior.
- Do not invent physical table/column names, SQL, or constraints.
- Duplicate handling, expansion snapshot, atomicity, and rollback are SOURCE_REQUIRED.
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
