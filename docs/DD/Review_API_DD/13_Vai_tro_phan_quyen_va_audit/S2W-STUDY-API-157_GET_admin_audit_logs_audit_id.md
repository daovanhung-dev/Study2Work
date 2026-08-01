# Review S2W-STUDY-API-157 — GET audit-log detail

- DD nguồn: `docs/DD/Study2Work_DD_API/13_Vai_tro_phan_quyen_va_audit/S2W-STUDY-API-157_GET_admin_audit_logs_audit_id.xlsx`
- Endpoint: `GET /api/v1/admin/audit-logs/{audit_id}`
- Kết luận: **CẦN SỬA — mapping không khớp audit schema**

## Các điểm cần sửa

| ID | Mức độ | Vị trí DD | Nhận xét và căn cứ BD | Cách sửa |
|---|---|---|---|---|
| 157-01 | P0 | `3.Data mapping!A12:H20` | Điều kiện dùng `audit_logs.audit_id`, nhưng PK là `id`; SELECT `actor,role,timestamp,target,before,after,correlation_id` như cột không tồn tại (`schema_seed.sql:691-732`). | Query `audit_logs.id`; alias/map từ actor_id/actor_role/created_at/target_type+id/before_value/after_value; bỏ correlationId hoặc bổ sung migration. |
| 157-02 | P1 | `2.Response!A16:H24` | `timestamp` chỉ là String, `action` là Object, actor/target là String mơ hồ; thiếu target type/id và audit id trong data. | Dùng schema item nhất quán API-156/SEQ-14, date-time và enum string; actor/target object tối thiểu nếu join. |
| 157-03 | P0 | `1.Request!A10:D10`, `4.Error!A11:H11` | Permission `study.rbac.manage` quá rộng/sai mục đích; SEQ-14 yêu cầu `audit.read` (`SEQ-14:33-38`). | Dùng audit.read và scope theo target; 404/403 policy chống enumeration. |
| 157-04 | P0 | `2.Response!A9:E11`, sample success | Envelope cũ và pagination giả cho singleton trái `System_Architecture.md:632-700`. | Chuyển sang envelope chuẩn camelCase và bỏ pagination. |
| 157-05 | P0 | `Overview!A12`, `3.Data mapping!A16:H16` | Câu “không trả dữ liệu nhạy cảm” chưa đủ: detail chứa full before/after, có nguy cơ lộ password/token/PII; BD cấm điều này (`BD-13:213-223`, `SEQ-14:117-120`). | Redact/minimize theo target/action; field allowlist và size limit; kiểm thử secret/PII. |

## Điều kiện duyệt lại

- Query/map đúng schema và response thống nhất API-156.
- Có audit.read scope, redaction và test 404/403/secret leakage.
