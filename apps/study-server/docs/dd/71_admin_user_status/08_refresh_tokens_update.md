---
title: "Định nghĩa refresh_tokens update"
order: 8
dd_id: "71"
api_name: "Khóa/mở khóa user Conditional"
source_sheet: "3. Data mapping — refresh_tokens"
status: "Draft — Needs Confirmation"
---

# Định nghĩa bảng refresh_tokens update

## Table mapping

| Table/Relation | Loại | Vai trò | Trạng thái |
|---|---|---|---|
| Legacy `refresh_tokens` | Conditional UPDATE | Thu hồi refresh credentials còn hiệu lực khi account chuyển sang SUSPENDED | Checked-in DDL/API #3 candidate; bulk user revoke là DERIVED. |

## SQL mapping

~~~sql
UPDATE refresh_tokens
SET revoked_at = CURRENT_TIMESTAMP
WHERE user_id = :user_id
  AND revoked_at IS NULL
  AND expires_at > CURRENT_TIMESTAMP
~~~

| Logical field | Column | Operation | Value/source | Runtime rule |
|---|---|---|---|---|
| Owner user ID | `user_id` | WHERE | Path user ID | BIGINT FK candidate tới `users.id`; bind parameter. |
| Revocation time | `revoked_at` | UPDATE | `CURRENT_TIMESTAMP` | Chỉ set cho token chưa revoke và chưa hết hạn, khi target status là SUSPENDED. |
| Expiration | `expires_at` | WHERE | Stored time | Chỉ token đang hiệu lực; API #3 refresh cũng yêu cầu expires_at > current time. |
| Token hash | `token_hash` | Excluded | N/A | Không đọc, log hoặc trả token hash. |
| Token ID | `id` | Not selected | N/A | Bulk mutation không cần response row IDs. |

Q2 chạy trong cùng transaction với `users.status` update. Nếu Q2 lỗi, rollback status update. Khi mở khóa, không khôi phục token rows; user cần đăng nhập lại. Access JWT đã cấp là stateless theo current guard và có thể còn dùng tới expiry. Không có migration hoặc live DB claim.