---
title: "Định nghĩa table"
order: 7
dd_id: "71"
api_name: "Khóa/mở khóa user Conditional"
source_sheet: "table"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Table mapping

| Table/Relation | Loại | Vai trò | Trạng thái |
|---|---|---|---|
| Legacy `users` | UPDATE/RETURNING candidate | Cập nhật account status và trả UserProfile safe projection | DERIVED CANDIDATE; live schema chưa verify. |
| Legacy `refresh_tokens` | Conditional UPDATE candidate | Đặt `revoked_at` cho refresh-token rows đang hiệu lực khi khóa nếu policy yêu cầu | DERIVED CANDIDATE; không revoke access JWT. |
| V1-PILOT `identity_projections` | Không dùng làm target candidate | Có UUID subject và account_status enum | DDL model khác; không map ngầm sang legacy BIGINT users. |

Không migration, DDL hoặc index nào được tạo bởi DD này.

## Candidate status source — legacy users

| Logical field | Relation | Column | Operation | Mapping/status |
|---|---|---|---|---|
| User ID | Legacy users | id | WHERE/RETURNING | BIGSERIAL candidate; map với `user_id` là DERIVED. |
| Account status | Legacy users | status | UPDATE/RETURNING | VARCHAR(20), default ACTIVE trong DDL; legal values chưa được constraint. |
| Updated time | Legacy users | updated_at | UPDATE/RETURNING | Candidate server timestamp; cần xác nhận behavior #71. |
| Safe profile | Legacy users | full_name/email/role/avatar_url/phone/created_at | RETURNING | UserProfile candidate; không lấy `password_hash`. |
| Biography | No legacy users column | N/A | No mapping | UserProfile.bio optional; source gap. |

V1-PILOT có enum `account_status` gồm ACTIVE, SUSPENDED, DELETION_PENDING, ANONYMIZED và lưu trên UUID identity projection. Chỉ ACTIVE/SUSPENDED được nêu như candidate cho operation khóa/mở khóa; không coi enum này là legacy users schema hoặc contract UserStatus.

## Candidate refresh-token mapping

| Logical field | Relation | Column | Operation | Mapping/status |
|---|---|---|---|---|
| User ID | Legacy refresh_tokens | user_id | WHERE | BIGINT FK candidate tới `users.id`. |
| Revoked time | Legacy refresh_tokens | revoked_at | Conditional UPDATE | Chỉ revoke rows chưa revoke và chưa hết hạn khi target status là SUSPENDED nếu policy được duyệt. |
| Token hash | Legacy refresh_tokens | token_hash | EXCLUDED | Không đọc/trả token hash; API #3 lưu hash và revoke bằng row ID. |
| Expiry | Legacy refresh_tokens | expires_at | Optional selection/filter | Candidate query có thể chỉ xét chưa hết hạn; policy “active session” cần xác nhận. |

Current API #3 revokes one refresh-token row by token ID. Bulk revoke by user is a proposal for #71. Refresh-token revocation alone does not invalidate existing stateless access JWTs.

## Alternate V1-PILOT source boundary

V1-PILOT `identity_projections` dùng UUID và `account_status`; legacy Study `users` dùng BIGINT và VARCHAR `status`. Không JOIN, thay thế hoặc gộp hai mô hình khi chưa có identity mapping/schema contract được duyệt.

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
