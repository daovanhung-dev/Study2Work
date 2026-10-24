---
title: "Định nghĩa table"
order: 7
dd_id: "70"
api_name: "Cập nhật thông tin/role Conditional"
source_sheet: "table"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Table mapping

| Table/Relation | Loại | Vai trò | Trạng thái |
|---|---|---|---|
| Legacy `users` | UPDATE/RETURNING candidate | Cập nhật profile và role; trả safe UserProfile projection | DERIVED CANDIDATE; live schema chưa verify. |
| V1-PILOT identity/profile/role relations | Không dùng trong candidate | Schema UUID khác legacy int64 user model | Không map/join khi chưa có contract identity mapping. |

Không migration hoặc DDL nào được tạo bởi DD này.

## Candidate read/write source — legacy users

Candidate cột theo `infra/postgres/study-server/DB.sql` và API #14 precedent:

| Logical field | Relation | Column | Operation | Mapping/status |
|---|---|---|---|---|
| User ID | Legacy users | id | WHERE/RETURNING | BIGINT candidate; match `user_id` chỉ là DERIVED. |
| Full name | Legacy users | full_name | UPDATE/RETURNING | Body candidate; API #14 precedent; validation reuse needs approval. |
| Phone | Legacy users | phone | UPDATE/RETURNING | Nullable PII candidate; null/omit semantics open. |
| Avatar URL | Legacy users | avatar_url | UPDATE/RETURNING | Candidate; exact URI/null behavior open. |
| Role | Legacy users | role | UPDATE/RETURNING | Inferred from #70 intent; enum/policy/transition SOURCE_REQUIRED. |
| Updated time | Legacy users | updated_at | UPDATE/RETURNING | Candidate server timestamp; API #14 precedent. |
| Email | Legacy users | email | RETURNING only | Preserve; not writable in candidate body; PII. |
| Status | Legacy users | status | RETURNING only | Preserve; API #71 owns status mutation. |
| Created time | Legacy users | created_at | RETURNING only | Candidate response mapping; live type/timezone unverified. |
| Biography | No legacy users column | N/A | No mapping | UserProfile.bio optional; source gap, no fabricated persistence. |
| Credential | Legacy users | password_hash | EXCLUDED | Never select, return or update. |

## Candidate UPDATE mapping

| Parameter/source | Target column | Operation | Evidence |
|---|---|---|---|
| `:user_id` | `users.id` | WHERE | Path type direct; relation mapping derived. |
| `:full_name` | `users.full_name` | UPDATE | Derived from user/profile intent and API #14. |
| `:phone` | `users.phone` | UPDATE | Derived from API #14; null/omission open. |
| `:avatar_url` | `users.avatar_url` | UPDATE | Derived from API #14; URI/null semantics open. |
| `:role` | `users.role` | UPDATE | Derived from API title/AC-31; exact role values/policy open. |
| Server timestamp | `users.updated_at` | UPDATE | Derived from API #14 precedent. |
| Returned safe fields | id/full_name/email/role/avatar_url/phone/status/created_at/updated_at | RETURNING | Candidate UserProfile projection; excludes password_hash; bio unavailable. |

## Alternate V1-PILOT source boundary

V1-PILOT uses UUID `identity_projections`, `learner_profiles`, `service_roles`, `service_permissions` and `service_role_assignments`. These relations do not prove a mapping to the legacy BIGINT users row or the `UserProfile` email/role fields. Do not JOIN or substitute them without an approved schema and identity contract.

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
