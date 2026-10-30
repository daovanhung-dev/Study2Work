---
title: "Định nghĩa table"
order: 7
dd_id: "72"
api_name: "Xóa user theo policy AC-31"
source_sheet: "table"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Table mapping

| Table/Relation | Loại | Vai trò | Trạng thái |
|---|---|---|---|
| Legacy `users` | UPDATE target candidate | BIGINT user, existing `status` and `updated_at` fields | Checked-in DDL only; live schema chưa xác minh. |
| Legacy user-linked relations | Preserved references | Courses, enrollments, progress, submissions, discussions, notifications, payments, refresh tokens | Không delete/cascade; relation policy chưa được duyệt. |
| V1-PILOT identity/profile | Không dùng làm target | UUID account lifecycle | Không có approved mapping sang API `user_id:int64`. |

## Mapping fields

| Logical field/operation | Physical relation | Column | Operation | Mapping/status |
|---|---|---|---|---|
| Target ID | Legacy `users` | `id` | WHERE | Bind `:user_id`; primary-key candidate. |
| Soft-delete marker | Legacy `users` | `status` | UPDATE | Set literal `DELETED`; value DERIVED, VARCHAR(20) in checked-in legacy DDL. |
| Mutation timestamp | Legacy `users` | `updated_at` | UPDATE/RETURNING | Set `CURRENT_TIMESTAMP`; return under alias `deleted_at` for this response. |
| DeleteResult.status | Response constant | N/A | Response | Literal `deleted` from catalog; not a DB column. |
| DeleteResult.deleted_at | Response alias | `users.updated_at` | RETURNING | Timestamp of this mutation only; not persisted separately as deletion time. |

## Mutation mapping

- Statement: one bound `UPDATE users`.
- WHERE: `id = :user_id`.
- WHERE: `status IS DISTINCT FROM 'DELETED'`.
- Updated field: `status = 'DELETED'`.
- Updated field: `updated_at = CURRENT_TIMESTAMP`.
- Returned field: `id`.
- Returned field: `updated_at AS deleted_at`.
- Transaction: validate RETURNING projection, then commit; rollback query/mapping/commit failures.
- No migration, new column, physical DELETE, anonymization, dependent-row mutation or cascade is included.

Legacy FK declarations are evidence of local relationships only; soft-delete retains the user row so this mutation does not violate those references. Live FK/schema state remains unverified.

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
