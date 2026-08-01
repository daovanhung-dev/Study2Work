# Review S2W-STUDY-API-155 — DELETE revoke user role

- DD nguồn: `docs/DD/Study2Work_DD_API/13_Vai_tro_phan_quyen_va_audit/S2W-STUDY-API-155_DELETE_admin_users_user_id_roles_role_code.xlsx`
- Endpoint: `DELETE /api/v1/admin/users/{user_id}/roles/{role_code}`
- Kết luận: **CẦN SỬA — soft-delete/HTTP contract mâu thuẫn schema**

## Các điểm cần sửa

| ID | Mức độ | Vị trí DD | Nhận xét và căn cứ BD | Cách sửa |
|---|---|---|---|---|
| 155-01 | P0 | `3.Data mapping!A12:H20`, DB Update sheets | DD dùng `user_roles.role_code` và “SOFT_DELETE”, nhưng bảng chỉ có `role_id`, không có deleted/status/revoked columns (`schema_seed.sql:311-317`). | JOIN roles.code để tìm role_id rồi hard delete nếu policy cho phép, hoặc bổ sung assignment lifecycle schema trước khi dùng soft delete. |
| 155-02 | P0 | `2.Response!A9:E11`, `A15:H23` | DD ghi HTTP 204 nhưng đồng thời thiết kế body `{data.revoked, effective_permissions, audit_id}` và sample; HTTP 204 không có response body. | Chọn 204 không body, hoặc 200 với envelope chuẩn; sửa toàn bộ sheet nhất quán. |
| 155-03 | P0 | `Overview!A19:B20`, `3.Data mapping!A13:H15` | Thiếu safeguard thu hồi role cuối cùng, tự thu hồi làm lockout, thu hồi role cao hơn actor và approval. BD yêu cầu Super Admin/risk control và audit (`BD-13:125-140`, `174-198`, `213-223`). | Lập revoke matrix/last-admin protection; bắt buộc reason và audit before/after trong cùng transaction/outbox. |
| 155-04 | P1 | `1.Request!A23:J23` | DELETE có JSON body `reason`; một số proxy/client không bảo đảm body và contract chưa nêu content semantics/idempotency. | Dùng endpoint action POST revoke hoặc header/query/body contract được OpenAPI/toolchain kiểm chứng; nêu already-revoked behavior. |
| 155-05 | P0 | `3.Data mapping!A15:H15` | Idempotency/concurrency chỉ là template, còn unique assignment có thể biến mất giữa read/delete. | Delete theo composite key trong transaction, kiểm affected rows và trả businessCode ổn định cho replay. |

## Điều kiện duyệt lại

- Chọn rõ hard/soft revoke và 200-vs-204.
- Có test last-admin/self-revoke/concurrency và audit không thể bỏ qua.
