# Review S2W-STUDY-API-135 — POST cancel active path

- DD nguồn: `docs/DD/Study2Work_DD_API/11_Admin_quan_ly_hoc_vien_va_ho_tro_ngoai_le/S2W-STUDY-API-135_POST_admin_learners_learner_id_active_path_cancel.xlsx`
- Endpoint: `POST /api/v1/admin/learners/{learner_id}/active-path/cancel`
- Kết luận: **CẦN SỬA — mapping ghi sai aggregate**

## Các điểm cần sửa

| ID | Mức độ | Vị trí DD | Nhận xét và căn cứ BD | Cách sửa |
|---|---|---|---|---|
| 135-01 | P0 | `3.Data mapping!A12:H20`, DB Update sheets | DD khóa/update `users.user_id` và ghi `enrollment_id`, `reason`, `allow_choose_new_path` vào `users`; PK thực là `users.id`, còn trạng thái cần đổi nằm ở `learning_path_enrollments` (`schema_seed.sql:387-408`). | Khóa đúng enrollment thuộc learner và đang ACTIVE; update `status=CANCELLED_BY_ADMIN`, `admin_reason`; không ghi input nghiệp vụ vào `users`. |
| 135-02 | P0 | `Overview!A18:B20`, `3.Data mapping!A13:H15` | BD yêu cầu chỉ dùng ngoại lệ, giữ lịch sử, audit, notification và tùy cấu hình mới được chọn path khác (`BD-11:125-137`, `170-180`). DD không chỉ ra cấu hình/nguồn của `allow_choose_new_path`. | Chốt đây là quyết định request hay policy server; nêu trạng thái onboarding/eligibility sau hủy và lưu ở đâu. |
| 135-03 | P1 | `2.Response!A16:H20` | `learner_eligibility`/`notification_created` là String và các field bị gán nguồn `users`; actual target là enrollment/audit/outbox. | Khai báo enum/object/Boolean đúng, nguồn đúng và response `auditLogId`. |
| 135-04 | P0 | `3.Data mapping!A15:H15` | Chưa có idempotency/concurrency cụ thể; hai request hủy có thể trả kết quả không ổn định. | Dùng row lock/version, idempotency key và businessCode cho already-cancelled/not-active. |
| 135-05 | P0 | `2.Response!A9:E11` | Envelope cũ trái `System_Architecture.md:632-700`; sample còn pagination cho mutation. | Dùng envelope chuẩn; bỏ pagination. |

## Điều kiện duyệt lại

- SQL tác động đúng enrollment và giữ history.
- Có test duplicate/concurrent cancel, audit và notification sau commit.
