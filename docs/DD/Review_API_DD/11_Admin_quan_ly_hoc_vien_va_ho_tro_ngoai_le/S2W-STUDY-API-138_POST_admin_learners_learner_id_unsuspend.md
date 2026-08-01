# Review S2W-STUDY-API-138 — POST unsuspend learner

- DD nguồn: `docs/DD/Study2Work_DD_API/11_Admin_quan_ly_hoc_vien_va_ho_tro_ngoai_le/S2W-STUDY-API-138_POST_admin_learners_learner_id_unsuspend.xlsx`
- Endpoint: `POST /api/v1/admin/learners/{learner_id}/unsuspend`
- Kết luận: **CẦN SỬA — chưa chốt service sở hữu trạng thái tài khoản**

## Các điểm cần sửa

| ID | Mức độ | Vị trí DD | Nhận xét và căn cứ BD | Cách sửa |
|---|---|---|---|---|
| 138-01 | P0 | `3.Data mapping!A12:H20`, DB Update sheets | Giống suspend, DD update local `users` nhưng Platform Identity là owner lifecycle account theo `System_Architecture.md:61-75`, `201-301`. Điều kiện còn dùng `users.user_id` thay vì `id`. | Chốt authoritative owner và sequence command/event; local table chỉ cập nhật projection nếu kiến trúc hiện hành được giữ. |
| 138-02 | P0 | `3.Data mapping!A13:H17`, `4.Error!A13:H15` | Không nêu state transition: chỉ `SUSPENDED` mới được mở hay API idempotent khi ACTIVE; không xử lý timed suspension, security hold hoặc permission cấp cao. | Lập state/role matrix và businessCode cụ thể; bảo vệ không tự mở các hold thuộc Security/Platform. |
| 138-03 | P1 | `2.Response!A16:H20` | `reopened_at`, `reopened_by`, `audit_id`, `notification_created` không có trong `users`; Boolean bị khai báo String. | Trả dữ liệu từ identity/audit/outbox, dùng kiểu đúng và thống nhất thuật ngữ `unsuspendedAt/By`. |
| 138-04 | P0 | `3.Data mapping!A15:H15` | Chưa có consistency model khi account authoritative đã mở nhưng projection/audit/notification lỗi. BD bắt buộc reason và actor (`BD-11:155`, `170-180`). | Dùng outbox/event retry, correlation, audit before/after và định nghĩa trạng thái tạm thời/khả năng phục hồi. |
| 138-05 | P0 | `2.Response!A9:E11` | Envelope cũ và pagination giả trái `System_Architecture.md:632-700`. | Chuyển sang envelope chuẩn, bỏ pagination và thêm traceId. |

## Điều kiện duyệt lại

- Có quyết định owner và transition matrix được Security/API Owner duyệt.
- Có test duplicate/retry, sync projection, audit và notification.
