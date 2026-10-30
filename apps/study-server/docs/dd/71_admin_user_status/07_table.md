---
title: "Định nghĩa users update"
order: 7
dd_id: "71"
api_name: "Khóa/mở khóa user Conditional"
source_sheet: "table — users"
status: "Draft — Needs Confirmation"
---

# Định nghĩa bảng users update

## Table mapping

| Table/Relation | Loại | Vai trò | Trạng thái |
|---|---|---|---|
| Legacy `users` | SELECT FOR UPDATE / UPDATE RETURNING | Khóa và đổi account status; trả safe UserProfile | Checked-in DDL candidate; live schema chưa verify. |
| V1-PILOT `identity_projections` | Không dùng | UUID account status model khác legacy users | Không JOIN hoặc mutate. |

## User status query and mutation

~~~sql
SELECT status
FROM users
WHERE id = :user_id
FOR UPDATE
~~~

~~~sql
UPDATE users
SET status = :status,
    updated_at = CURRENT_TIMESTAMP
WHERE id = :user_id
RETURNING id, full_name, email, role, avatar_url, phone, status, created_at, updated_at
~~~

## Column mapping

| Logical field | Column | Operation | Value/source | Runtime rule |
|---|---|---|---|---|
| User identity | `id` | WHERE/RETURNING | Path `user_id` | BIGSERIAL candidate; bound int64. |
| Current account status | `status` | SELECT FOR UPDATE | Stored value | Only ACTIVE/SUSPENDED may transition through #71; other state returns 422 DERIVED. |
| Target account status | `status` | UPDATE/RETURNING | Body `status` | ACTIVE or SUSPENDED only; request allowlist DERIVED. |
| Modification time | `updated_at` | UPDATE/RETURNING | `CURRENT_TIMESTAMP` | Set on each accepted request, including same-state request; DERIVED. |
| User name | `full_name` | RETURNING | Stored value | Required safe UserProfile field; not changed. |
| Email | `email` | RETURNING | Stored value | Required safe UserProfile field; not changed. |
| Role | `role` | RETURNING | Stored value | Required safe UserProfile field; not changed. |
| Avatar | `avatar_url` | RETURNING | Stored value | Nullable; preserve null. |
| Phone | `phone` | RETURNING | Stored value | Nullable; preserve null. |
| Creation time | `created_at` | RETURNING | Stored value | Required UserProfile field. |
| Password hash | `password_hash` | Excluded | N/A | Never selected or returned. |
| Biography | No legacy `users` column | Excluded | N/A | No fabricated `bio`; API #04 UserProfile model omits it. |

No migration, DDL change or index is introduced. BIGINT schema and live deployment are unverified.

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
