---
title: "Định nghĩa table"
order: 7
dd_id: "69"
api_name: "Lấy chi tiết user"
source_sheet: "table"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Table mapping

N/A — READ-ONLY API. API #69 không INSERT, UPDATE hoặc DELETE.

## Candidate read source — legacy users

| Logical field | Relation | Column | Mapping | Basis/status |
|---|---|---|---|---|
| User ID | Legacy users | id | UserProfile.id | BIGSERIAL candidate; live schema unverified. |
| Full name | Legacy users | full_name | UserProfile.full_name | Candidate; API #4/#14 projection precedent. |
| Email | Legacy users | email | UserProfile.email | PII; Admin-only. |
| Role | Legacy users | role | UserProfile.role | VARCHAR candidate; enum members unspecified. |
| Avatar | Legacy users | avatar_url | UserProfile.avatar_url | Nullable; runtime giữ JSON null theo API #04 model. |
| Biography | No legacy users column | N/A | Omitted | Optional contract field; không có source trong current profile queries/model. |
| Phone | Legacy users | phone | UserProfile.phone | Nullable PII; runtime giữ JSON null theo API #04 model. |
| Status | Legacy users | status | UserProfile.status | VARCHAR candidate; enum members/deletion policy unresolved. |
| Created time | Legacy users | created_at | UserProfile.created_at | Timestamp candidate; live schema unknown. |
| Updated time | Legacy users | updated_at | UserProfile.updated_at | Timestamp candidate; live schema unknown. |
| Credential | Legacy users | password_hash | Excluded | Never select or return. |

## Alternate V1-PILOT source boundary

V1-PILOT identity_projections, learner_profiles, service_roles, service_permissions and service_role_assignments use UUID-oriented relations. They do not establish one live users row with email, phone, Admin role and int64 ID. Do not join or substitute those relations without an approved contract/schema mapping.

No table, column, index, enum, audit record or role policy is created by this DD.

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
