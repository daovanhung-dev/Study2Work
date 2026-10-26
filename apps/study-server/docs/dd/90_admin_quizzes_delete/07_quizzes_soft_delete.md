---
title: "Table — quizzes soft delete"
order: 7
dd_id: "90"
api_name: "Xóa quiz"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
status: "Draft — Needs Confirmation"
---

# Định nghĩa table — `quizzes` UPDATE (soft-delete)

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | Legacy candidate `quizzes` |
| Logical table | Quiz |
| Operation | UPDATE |
| Data Mapping step | [Step 4A — soft delete](./05_Data_Mapping.md#step-4a-soft-delete) |
| Basis | AC-35 yêu cầu soft-delete khi có attempts; marker/value runtime là DERIVED và chưa được xác nhận. |

## Update mapping

**Áp dụng khi**

- Q2 tìm thấy attempt hoặc answer trỏ tới question/choice của quiz, và Quiz chưa là tombstone `DELETED`.
- Giữ nguyên các question/choice/attempt/answer rows.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|
| 1 | `id` | Quiz ID | BIGSERIAL | N/A | N/A | Yes | Yes | `quiz_id` từ path, chỉ định record | Request path | Step 2 / Step 4A | Candidate legacy PK; live schema chưa xác minh. |
| 2 | `status` | Quiz status | VARCHAR | 20 | N/A | Nullable; DDL default DRAFT | No | `DELETED` | Runtime source; value DERIVED | Step 4A | Cột có trong DDL; allowed values không canonical. |
| 3 | `updated_at` | Last updated time | TIMESTAMP | N/A | N/A | Yes | No | DB timestamp lần đầu soft-delete; giữ nguyên khi DELETE lặp lại | Runtime source; semantics DERIVED | Step 4A | DDL có cột; timezone/clock policy và map sang `deleted_at` cần xác nhận. |

## Điều kiện UPDATE

- `quizzes.id = :quiz_id`.
- Chỉ chạy khi Q2 thấy attempt hoặc linked answer history.
- Không cập nhật course/title/questions/choices hoặc `created_at`.
- Nếu status đã `DELETED`, runtime không ghi lại timestamp; giữ source row nguyên trạng theo policy idempotency DERIVED.
- Không thay đổi status nếu tombstone state chưa được owner phê duyệt.

## Gap

- Legacy `quizzes` không có `deleted_at`; `status='DELETED'` là giá trị DERIVED, chưa được định nghĩa trong enum.
- `DeleteResult.deleted_at` map từ `updated_at` trong runtime; tombstone semantics và future immutability cần được duyệt.
- Nếu physical schema được chọn không có status/timestamp tương ứng, cần schema decision ngoài phạm vi DD này.

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
