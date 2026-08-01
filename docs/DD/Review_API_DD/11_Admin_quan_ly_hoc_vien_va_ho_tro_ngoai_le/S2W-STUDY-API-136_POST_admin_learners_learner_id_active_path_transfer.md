# Review S2W-STUDY-API-136 — POST transfer active path

- DD nguồn: `docs/DD/Study2Work_DD_API/11_Admin_quan_ly_hoc_vien_va_ho_tro_ngoai_le/S2W-STUDY-API-136_POST_admin_learners_learner_id_active_path_transfer.xlsx`
- Endpoint: `POST /api/v1/admin/learners/{learner_id}/active-path/transfer`
- Kết luận: **CẦN SỬA — có nguy cơ tạo trạng thái lộ trình không nhất quán**

## Các điểm cần sửa

| ID | Mức độ | Vị trí DD | Nhận xét và căn cứ BD | Cách sửa |
|---|---|---|---|---|
| 136-01 | P0 | `3.Data mapping!A12:H20`, DB Update sheets | DD update `users` bằng `current_enrollment_id/target_path_id/progress_policy`; dữ liệu thật nằm ở `learning_path_enrollments`, và `users.user_id` không tồn tại. | Trong một transaction: khóa enrollment hiện tại, validate target, kết thúc enrollment cũ, tạo/activate enrollment mới và ghi audit. |
| 136-02 | P0 | `3.Data mapping!A13:H15` | Invariant chỉ một ACTIVE được BD yêu cầu (`BD-11:170-180`) và được DB bảo vệ bằng partial unique index (`schema_seed.sql:405-408`), nhưng DD không chỉ cách xử lý race/unique violation. | Nêu lock order, isolation/version, map unique violation thành 409/businessCode và rollback toàn bộ. |
| 136-03 | P1 | `1.Request!A22:J25` | `progress_policy=KEEP_HISTORY` mơ hồ vì BD luôn yêu cầu giữ lịch sử; chưa rõ có mang credit/progress sang lộ trình mới hay không, cách map course trùng và submission ra sao. | Tách “history retention” khỏi “credit transfer”; định nghĩa effect matrix được Product phê duyệt. |
| 136-04 | P1 | `2.Response!A16:H20` | `new_enrollment`, `active_count`, `learner_notified` sai kiểu (`String`) và sai nguồn (`users`). | Trả object enrollment, integer activeCount, Boolean learnerNotified và auditLogId từ nguồn thật. |
| 136-05 | P0 | `2.Response!A9:E11`, `3.Data mapping!A15:H15` | Envelope cũ, pagination giả và idempotency chỉ là câu template. | Chuẩn hóa contract; quy định replay behavior và outbox notification sau commit. |

## Điều kiện duyệt lại

- Có test race hai transfer và invariant activeCount ≤ 1.
- Policy chuyển credit/progress, rollback, audit và notification được chốt rõ.
