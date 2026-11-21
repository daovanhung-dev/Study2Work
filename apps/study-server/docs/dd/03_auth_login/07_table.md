---
title: "Định nghĩa table"
order: 7
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
---

# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | `users` (SELECT) và `refresh_tokens` (current login INSERT) |
| Logical table | User account và refresh-token session record |
| Operation | Expected catalog: persistence unspecified; current source: SELECT + INSERT |
| Data Mapping step | `3.1` SELECT users; `5.1` phát hành/persist refresh token |

> `infra/postgres/study-server/DB.sql` là DDL artifact trong repo, không xác nhận schema live. Catalog API #03 không quy định persistence.

## Update mapping

**Áp dụng khi**

- `N/A — API #3 không có UPDATE được source xác nhận.`

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---|---|---:|---|---|---|---|
| `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | Không tạo mapping DB giả |

## Insert mapping

**Áp dụng khi**

- Expected theo catalog: chưa đặc tả persistence.
- Current source login: INSERT vào `refresh_tokens` sau khi credential hợp lệ và token được phát hành.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---|---|---:|---|---|---|---|
| 1 | `user_id` | User ID | `BIGINT` | N/A | N/A | Yes | No | `user["id"]` | Current SQL parameter; DDL candidate FK to `users.id` | `5.1` | Runtime schema unverified |
| 2 | `token_hash` | Refresh token hash | `VARCHAR` | 64 | N/A | Yes | No | HMAC-SHA256 hash | Auth utility parameter; DDL candidate UNIQUE | `5.1` | Raw refresh token is not stored in this column |
| 3 | `expires_at` | Refresh token expiry | `TIMESTAMPTZ` | N/A | N/A | Yes | No | Auth utility expiry | Current SQL parameter; DDL candidate NOT NULL | `5.1` | Exact lifetime is config-based |
| 4 | `created_at` | Creation time | `TIMESTAMPTZ` | N/A | N/A | Yes | No | `CURRENT_TIMESTAMP` | Current INSERT expression; DDL candidate has same default | `5.1` | Source writes creation time explicitly |

### Source-only sibling route: POST /auth/refresh

Route refresh hiện được gắn marker API #03 nhưng không có catalog row riêng. Source query thu hồi record cũ bằng `revoked_at` rồi insert token hash mới trong cùng transaction. Đây không phải mutation của POST /auth/login và không được nhập vào contract normative ở đây.

## Delete mapping

**Áp dụng khi**

- `N/A — API #3 không có DELETE được source xác nhận.`

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---:|---|---|---|---|---|
| `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | Không tạo mapping DB giả |

## Read mapping — current login source

`users` được đọc theo email; source lấy `id`, `full_name`, `email`, `password_hash`, `role`, `avatar_url`, `phone`, `status`, `created_at`, `updated_at`. `password_hash` chỉ dùng cho password verification; query profile không trả hash.


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

