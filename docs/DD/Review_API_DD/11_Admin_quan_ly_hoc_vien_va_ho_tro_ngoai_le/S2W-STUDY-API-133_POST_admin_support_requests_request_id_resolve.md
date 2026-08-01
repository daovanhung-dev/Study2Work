# Review S2W-STUDY-API-133 — POST resolve support request

- DD nguồn: `docs/DD/Study2Work_DD_API/11_Admin_quan_ly_hoc_vien_va_ho_tro_ngoai_le/S2W-STUDY-API-133_POST_admin_support_requests_request_id_resolve.xlsx`
- Endpoint: `POST /api/v1/admin/support-requests/{request_id}/resolve`
- Kết luận: **CẦN SỬA — sai contract SEQ-12 và chưa đủ an toàn giao dịch**

## Các điểm cần sửa

| ID | Mức độ | Vị trí DD | Nhận xét và căn cứ BD | Cách sửa |
|---|---|---|---|---|
| 133-01 | P0 | `1.Request!A21:J26` | Contract lệch trực tiếp SEQ-12: DD dùng `APPROVE|REJECT`, action Object `RESET|CANCEL|TRANSFER`, `reason`, `learner_message`; BD quy định `APPROVED`, `SWITCH_LEARNING_PATH`, `targetLearningPathId`, `adminReason`, `notifyLearner` (`SEQ-12:76-87`). | Đồng bộ tên/enum/required với SEQ-12 hoặc lập quyết định thay đổi BD có phê duyệt; action phải là enum string. |
| 133-02 | P0 | `2.Response!A15:H23` | Response `request_status/resulting_states/audit_id/notification_created` không khớp response chuẩn `requestId`, `status`, `appliedAction`, `auditLogId` tại `SEQ-12:90-105`; nhiều kiểu Boolean/Object bị để String. | Viết response đúng sequence, kiểu cụ thể và envelope chuẩn camelCase. |
| 133-03 | P0 | `3.Data mapping!A12:H20`, DB sheets | Mapping coi `decision`, `action`, `target_path_id`, `learner_message` là cột update của `support_requests`, nhưng schema chỉ có `admin_decision`, `target_learning_path_id`, `resolved_at` (`schema_seed.sql:662-682`). Chưa có SQL thực hiện reset/cancel/switch. | Thiết kế transaction thật: khóa request/enrollment, validate trạng thái, cập nhật đúng bảng, đảm bảo một ACTIVE, ghi audit before/after và outbox notification. |
| 133-04 | P0 | `1.Request!A11:D11`, `3.Data mapping!A15:H15` | Mutation rủi ro và retryable chỉ ghi chung “Idempotency-Key” nhưng không có storage key/request hash/replay behavior; concurrent resolve có thể áp dụng hai lần. Kiến trúc yêu cầu transaction/outbox (`System_Architecture.md:601-628`). | Bắt buộc idempotency contract; optimistic version/row lock; map request đã resolve và unique ACTIVE thành businessCode/409 ổn định. |
| 133-05 | P1 | `4.Error!A9:H15` | Error chưa phân biệt decision/action không hợp lệ theo type, request đã đóng, target path không published, target trùng current hay action thất bại từng phần. | Bổ sung state-specific errors và rollback semantics; notification chỉ phát sau commit. |

## Điều kiện duyệt lại

- Contract được đối chiếu từng field với SEQ-12.
- Có integration test double-submit/concurrent resolve và chứng minh enrollment + request + audit nhất quán.
