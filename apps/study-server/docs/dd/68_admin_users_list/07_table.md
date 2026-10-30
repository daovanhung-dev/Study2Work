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

N/A — READ-ONLY API. API #68 chỉ SELECT, không INSERT, UPDATE hoặc DELETE.

## Runtime query source — legacy users candidate

| Logical role | Relation | Column | Mapping | Basis/status |
|---|---|---|---|---|
| User ID | users | id | UserProfile.id | BIGSERIAL candidate; live schema unknown. |
| Full name | users | full_name | UserProfile.full_name | Legacy DDL and API #04 model. |
| Email | users | email | UserProfile.email | PII; ADMIN guard; legacy candidate. |
| Role | users | role | UserProfile.role | VARCHAR(20); runtime model string; no enum whitelist. |
| Avatar | users | avatar_url | UserProfile.avatar_url | Nullable candidate; current API #04 serializes null. |
| Phone | users | phone | UserProfile.phone | Nullable PII candidate; current API #04 serializes null. |
| Status | users | status | UserProfile.status | VARCHAR(20); stored string; exact optional filter. |
| Created time | users | created_at | UserProfile.created_at | Timestamp candidate. |
| Updated time | users | updated_at | UserProfile.updated_at | Timestamp candidate. |
| Credential | users | password_hash | Excluded | SQL does not select; never return. |
| Biography | No legacy users column | N/A | Omitted | Reusable field optional; no current API #04 source. |

No query JOIN, schema change or migration is added. The V1-PILOT UUID identity/profile model is not joined to legacy BIGINT user IDs. Checked-in DDL and fake-session tests do not establish deployed schema.

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
