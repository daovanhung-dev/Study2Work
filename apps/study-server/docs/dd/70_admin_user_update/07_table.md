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
| Legacy `users` | UPDATE/RETURNING runtime target candidate | Cập nhật profile và role; trả safe UserProfile projection | Runtime local; live schema/deployment chưa verify. |
| V1-PILOT identity/profile/role relations | Không dùng | Schema UUID khác legacy int64 user model | Không map/join khi chưa có contract identity mapping. |

Không migration hoặc DDL nào được tạo bởi DD này.

## Runtime read/write source — legacy users candidate

Candidate cột theo `infra/postgres/study-server/DB.sql` và API #14 precedent:

| Logical field | Relation | Column | Operation | Mapping/status |
|---|---|---|---|---|
| User ID | Legacy users | id | WHERE/RETURNING | BIGINT candidate; match `user_id` chỉ là DERIVED. |
| Full name | Legacy users | full_name | UPDATE/RETURNING | Runtime fallback; API #14 trim/nonblank/max 150 rules. |
| Phone | Legacy users | phone | UPDATE/RETURNING | Runtime fallback; nullable, trim/blank-to-null, max 20. |
| Avatar URL | Legacy users | avatar_url | UPDATE/RETURNING | Runtime fallback; nullable trim/blank-to-null; URL syntax not checked. |
| Role | Legacy users | role | UPDATE/RETURNING | Runtime allowlist `STUDENT`/`MENTOR`/`ADMIN`; DERIVED. |
| Updated time | Legacy users | updated_at | UPDATE/RETURNING | `CURRENT_TIMESTAMP`; API #14 precedent. |
| Email | Legacy users | email | RETURNING only | Preserve; not writable in candidate body; PII. |
| Status | Legacy users | status | RETURNING only | Preserve; API #71 owns status mutation. |
| Created time | Legacy users | created_at | RETURNING only | Response mapping; live type/timezone unverified. |
| Biography | No legacy users column | N/A | No mapping | UserProfile.bio optional; source gap, no fabricated persistence. |
| Credential | Legacy users | password_hash | EXCLUDED | Never select, return or update. |

## Runtime UPDATE mapping

| Parameter/source | Target column | Operation | Evidence |
|---|---|---|---|
| `:user_id` | `users.id` | WHERE | Path type direct; relation mapping derived. |
| `:full_name` | `users.full_name` | UPDATE | Runtime fallback; normalized by API #14 rules. |
| `:phone` | `users.phone` | UPDATE | Runtime fallback; null clears the column. |
| `:avatar_url` | `users.avatar_url` | UPDATE | Runtime fallback; null clears the column. |
| `:role` | `users.role` | UPDATE | Runtime allowlist from current Study role labels; transition policy open. |
| Server timestamp | `users.updated_at` | UPDATE | `CURRENT_TIMESTAMP`; API #14 precedent. |
| Returned safe fields | id/full_name/email/role/avatar_url/phone/status/created_at/updated_at | RETURNING | Runtime UserProfile projection; excludes password_hash; bio unavailable. |

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
