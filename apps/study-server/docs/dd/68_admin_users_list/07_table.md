---
title: "Định nghĩa table"
order: 7
dd_id: "68"
api_name: "Lấy danh sách user"
source_sheet: "table"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Table mapping

N/A — READ-ONLY API. API #68 không INSERT, UPDATE hoặc DELETE.

## Candidate read source — legacy users

| Logical role | Relation | Column | Mapping | Basis/status |
|---|---|---|---|---|
| User ID | Legacy users | id | UserProfile.id | BIGSERIAL candidate; live schema unknown. |
| Full name | Legacy users | full_name | UserProfile.full_name | Source candidate and API #4/#14 precedent. |
| Email | Legacy users | email | UserProfile.email | PII; Admin-only. |
| Role | Legacy users | role | UserProfile.role: UserRole and optional filter | VARCHAR(20); enum members not specified. |
| Avatar | Legacy users | avatar_url | UserProfile.avatar_url | Nullable candidate. |
| Phone | Legacy users | phone | UserProfile.phone | Nullable PII candidate. |
| Status | Legacy users | status | UserProfile.status: UserStatus and optional filter | VARCHAR(20); enum members/deletion policy unresolved. |
| Created time | Legacy users | created_at | UserProfile.created_at | Timestamp candidate. |
| Updated time | Legacy users | updated_at | UserProfile.updated_at | Timestamp candidate. |
| Credential | Legacy users | password_hash | Excluded | Never select or return. |
| Biography | No legacy users column | N/A | UserProfile.bio unresolved | SOURCE_REQUIRED. |

## Alternate V1-PILOT source boundary

V1-PILOT defines UUID identity_projections and learner_profiles with service-role assignments. It does not define one legacy-compatible users row containing email, role, phone and int64 ID. Do not join those relations or claim they are live.

No table, column, index, audit record, role enum or status enum is created by this DD.

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
