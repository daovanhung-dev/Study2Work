# Review S2W-STUDY-API-154 — POST assign user role

- DD nguồn: `docs/DD/Study2Work_DD_API/13_Vai_tro_phan_quyen_va_audit/S2W-STUDY-API-154_POST_admin_users_user_id_roles.xlsx`
- Endpoint: `POST /api/v1/admin/users/{user_id}/roles`
- Kết luận: **CẦN SỬA — insert mapping và kiểm soát privilege escalation chưa đúng**

## Các điểm cần sửa

| ID | Mức độ | Vị trí DD | Nhận xét và căn cứ BD | Cách sửa |
|---|---|---|---|---|
| 154-01 | P0 | `1.Request!A22:J24`, DB Insert sheets | `user_roles` cần `user_id`, `role_id`, `assigned_at`; DD lại insert `role_code`, `reason`, `expires_at`, các cột không tồn tại (`schema_seed.sql:311-317`). | Resolve active `roles.code → roles.id`; insert đúng cột. Lưu reason ở audit; nếu cần expiry phải bổ sung migration/policy. |
| 154-02 | P0 | `3.Data mapping!A12:H20` | Điều kiện đọc/khóa `user_roles.user_id` không kiểm role code tồn tại/active; không nêu xử lý unique `(user_id,role_id)` hay retry. | Validate user/role/scope, row lock hoặc unique mapping, idempotency key; map already-assigned ổn định. |
| 154-03 | P0 | `Overview!A19:B20`, `3.Data mapping!A13:H15` | BD chỉ Super Admin quản lý quyền cao nhất và mọi cấp role Admin/Support/Moderator phải audit (`BD-13:125-140`, `174-198`, `213-223`). DD không có rule chống self-escalation, grant role cao hơn actor, hay role cuối cùng giữ hệ thống. | Lập grant matrix, step-up/approval cho high-risk, self/last-admin safeguards; audit actorRole, target, before/after, reason. |
| 154-04 | P1 | `2.Response!A16:H18` | `assigned_role` là String, effective permissions chưa có nguồn; audit ID bị gán nguồn user_roles. | Trả role object từ roles, effective permissions chỉ khi model có thật, auditLogId từ audit log. |
| 154-05 | P0 | `2.Response!A9:E11`, `3.Data mapping!A15:H15` | Envelope cũ/pagination giả và idempotency chỉ là câu template; mutation quyền có thể lặp. | Dùng envelope chuẩn; định nghĩa key/request hash/replay TTL và transaction/outbox/audit consistency. |

## Điều kiện duyệt lại

- Insert chạy đúng DDL hoặc migration expiry được phê duyệt.
- Có test self-escalation, higher-role grant, duplicate/concurrent grant và audit exactly once.
