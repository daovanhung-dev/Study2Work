# Review S2W-STUDY-API-156 — GET audit logs

- DD nguồn: `docs/DD/Study2Work_DD_API/13_Vai_tro_phan_quyen_va_audit/S2W-STUDY-API-156_GET_admin_audit_logs.xlsx`
- Endpoint: `GET /api/v1/admin/audit-logs`
- Kết luận: **CẦN SỬA — lệch SEQ-14 và SQL không hợp lệ**

## Các điểm cần sửa

| ID | Mức độ | Vị trí DD | Nhận xét và căn cứ BD | Cách sửa |
|---|---|---|---|---|
| 156-01 | P0 | `1.Request!A21:J30` | SEQ-14 quy định `actorId,targetType,targetId,action,from,to,page,pageSize` và action là string (`SEQ-14:43-59`). DD dùng snake_case, thêm actor_role/channel nhưng khai báo `action` là Object. | Đồng bộ camelCase; action/role/channel là enum string; nếu mở rộng filter phải document/version. |
| 156-02 | P0 | `3.Data mapping!A12:H20` | Query lọc `audit_logs.from/to` (không tồn tại) thay vì `created_at`; `ORDER BY desc` sai cú pháp. SELECT các alias `audit_id,actor,role,occurred_at,target` như cột dù schema có `id,actor_id,actor_role,created_at,target_type,target_id` (`schema_seed.sql:691-732`). | Viết SELECT alias/JOIN đúng và `created_at >= :from AND created_at < :to ORDER BY created_at DESC,id DESC`; index/pagination ổn định. |
| 156-03 | P0 | `1.Request!A10:D10`, `4.Error!A11:H11` | DD yêu cầu `study.rbac.manage`, trong khi SEQ-14 yêu cầu `audit.read` (`SEQ-14:33-38`). | Tách audit-read khỏi RBAC mutation; giới hạn scope toàn cục cho Super Admin và theo nghiệp vụ cho Admin phù hợp. |
| 156-04 | P0 | `2.Response!A15:H25` | Contract lệch item chính xác của SEQ-14 (`id,actorId,actorRole,action,targetType,targetId,beforeValue,afterValue,reason,createdAt`) tại `SEQ-14:62-97`; `action` sai kiểu Object. | Dùng item sequence hoặc cập nhật BD có phê duyệt; map cột đúng và redaction trước/after. |
| 156-05 | P0 | `2.Response!A9:E11`, sample success/error | Envelope cũ trái cả chuẩn hệ thống (`System_Architecture.md:632-700`) và error mẫu `RBAC_PERMISSION_DENIED` của SEQ-14 (`100-114`). | Dùng success/businessCode/message/data/meta.pagination/traceId và errors[]. |
| 156-06 | P1 | `3.Data mapping!A16:H16` | Chưa có policy loại password, OTP, token/raw PII khỏi before/after; BD cấm dữ liệu nhạy cảm trong audit (`BD-13:213-223`, `SEQ-14:117-120`). | Lập redaction allowlist theo target type và test dữ liệu nhạy cảm. |

## Điều kiện duyệt lại

- Request/response/error khớp SEQ-14 và SQL chạy được.
- Có permission `audit.read`, stable pagination, redaction và negative tests.
