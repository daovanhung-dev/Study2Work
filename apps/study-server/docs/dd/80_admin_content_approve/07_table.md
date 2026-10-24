---
title: "Định nghĩa table"
order: 7
dd_id: "80"
api_name: "Phê duyệt nội dung"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | SOURCE_REQUIRED — chưa chọn |
| Logical table | Content review status và approval audit |
| Operation | UPDATE + APPEND — logical effects only |
| Data Mapping step | Step 5–6; see [Step 3](./05_Data_Mapping.md#3-insertupdate-thong-tin) |

> Đây là logical mutation/gap register, chưa phải physical DB specification. Legacy DDL không có Content review/audit table được chọn. V1-PILOT content_review_decisions dùng UUID revision identity và không được map trực tiếp sang contract Content ID int64.

## Update mapping

**Áp dụng khi**

- AC-33 approve branch được thực hiện và status transition cụ thể đã được chủ sở hữu contract xác nhận.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---|---|
| 1 | SOURCE_REQUIRED | Content review/publication status | ContentStatus | TBD | N/A | TBD | N/A | APPROVED/PUBLISHED theo diagram; exact target chưa chốt | AC-33 node n9 | Step 5 | Logical field only; physical table/column, revision key và transition chưa được xác nhận. |

## Insert mapping

**Áp dụng khi**

- AC-33 approve branch ghi audit; physical append target và schema cần được duyệt.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---|---|
| 1 | SOURCE_REQUIRED | Approval audit/decision record | SOURCE_REQUIRED | TBD | N/A | TBD | N/A | Ghi audit sau approve theo AC-33 | AC-33 node n9 | Step 6 | Không tự thêm reviewer, comment, reason code, timestamp, version hoặc row-version column. |

## Delete mapping

**Áp dụng khi**

- N/A — API #80 không khai báo delete.

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---:|---|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | No DELETE operation. |
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
