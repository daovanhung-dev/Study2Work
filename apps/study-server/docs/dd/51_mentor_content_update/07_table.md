---
title: "Định nghĩa table"
order: 7
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
dd_id: "51"
api_name: "Cập nhật nội dung Mentor"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table — Logical Content/version update, physical mapping SOURCE_REQUIRED

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table/model | `SOURCE_REQUIRED`; không có generic Content/version relation tương thích trong DDL hiện có. |
| Logical entity | `Content` và revision/version state theo catalog + AC-22. |
| Operation | Logical UPDATE Content + version. |
| Data Mapping step | 4–8 |
| Evidence | API #51 row; AC-22 PUT node `UPDATE Content + version`; AC-33 reads content/version/author. |
| Runtime | Route/module/test chưa tìm thấy (`UNWIRED` / `NOT_FOUND`). |

## Update/version mapping

| Logical value/field | Value source | Proposed action | Evidence/status |
|---|---|---|---|
| `id` | Path `content_id` | Chọn và giữ nguyên Content identity | Path DIRECT; physical column SOURCE_REQUIRED |
| `course_id` | Current Content | Preserve; dùng để authorization | DERIVED immutable-scope rule; physical mapping SOURCE_REQUIRED |
| `content_type` | Proposed body | Ghi vào revision mới | DERIVED; enum/type-change policy SOURCE_REQUIRED |
| `title` | Proposed body | Ghi vào revision mới | DERIVED; schema/normalization SOURCE_REQUIRED |
| `payload` | Proposed body | Ghi object thay thế vào revision mới | DERIVED; subtype schema/storage SOURCE_REQUIRED |
| `status` | Review lifecycle | New revision candidate `PENDING_REVIEW` | DERIVED from AC-22 + AC-33; transition/storage SOURCE_REQUIRED |
| `parent_id` | Current Content | Preserve | DERIVED proposal; parent schema SOURCE_REQUIRED |
| `order` | Current Content | Preserve | DERIVED proposal; ordering schema SOURCE_REQUIRED |
| Previous revision | Existing Content/version | Retain as historical snapshot | DERIVED proposal; version persistence SOURCE_REQUIRED |
| New revision | Proposed complete body | Advance current logical version | AC-22 logical version effect DIRECT; revision representation SOURCE_REQUIRED |
| `version_no`/`row_version` | Not in API contract | No concrete field or numeric rule assigned | SOURCE_REQUIRED; do not equate pilot `row_version` with content revision |
| `updated_by`/timestamps/audit | Not in contract | No column/value assigned | SOURCE_REQUIRED |

## SQL mapping

Chưa duyệt câu SQL `UPDATE` hoặc `INSERT` version vật lý. Chưa xác định relation/cột, cách chọn current version, thời hạn giữ version cũ, uniqueness, khóa dòng, kiểu ID và projection trả về. Không dùng V1-PILOT `content_blocks`/`row_version` thay cho catalog Content.

## Transaction proposal

Vì AC-22 ghép update Content với thay đổi version, đề xuất xử lý nguyên tử: revision Content và version cùng commit hoặc cùng rollback. Đây là `DERIVED` cho tới khi chọn được persistence model và transaction owner.

## Cross-API lifecycle

- API #50 creates Content; its proposed initial state is `PENDING_REVIEW`.
- API #51 proposes a new `PENDING_REVIEW` revision while retaining the previous published revision until review/publish completes.
- API #52 publishes/unpublishes; API #53 deletes. Admin AC-33 approves/rejects and reads version/author metadata.
- The exact compatibility between Admin approval `APPROVED/PUBLISHED` and Mentor publish #52 remains for AC-22 macro-review after #52/#53 DDs exist.

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
