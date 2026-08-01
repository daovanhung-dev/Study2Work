# Review S2W-STUDY-API-137 — POST suspend learner

- DD nguồn: `docs/DD/Study2Work_DD_API/11_Admin_quan_ly_hoc_vien_va_ho_tro_ngoai_le/S2W-STUDY-API-137_POST_admin_learners_learner_id_suspend.xlsx`
- Endpoint: `POST /api/v1/admin/learners/{learner_id}/suspend`
- Kết luận: **CẦN SỬA — chưa chốt service sở hữu trạng thái tài khoản**

## Các điểm cần sửa

| ID | Mức độ | Vị trí DD | Nhận xét và căn cứ BD | Cách sửa |
|---|---|---|---|---|
| 137-01 | P0 | `3.Data mapping!A12:H20`, DB Update sheets | DD cập nhật local `study.users`, trong khi kiến trúc hệ thống giao lifecycle identity/account cho Platform Identity và Study chỉ giữ projection (`System_Architecture.md:61-75`, `201-301`). Hai BD đang xung đột nên chưa thể VERIFIED. | Chốt owner/host: gọi command Platform Identity rồi đồng bộ projection qua event/outbox, hoặc phê duyệt ngoại lệ sửa kiến trúc trước khi viết SQL. |
| 137-02 | P0 | `1.Request!A22:J24` | `category` không có enum, `until` không có timezone/auto-unsuspend/job semantics; không rõ suspend đã suspend thì trả gì. | Chốt category enum, max duration, permanent vs timed, scheduler/event và idempotent state transition. |
| 137-03 | P1 | `2.Response!A16:H21` | `suspended_at`, `suspended_by`, `restrictions`, `audit_id`, `notification_created` không phải cột `users`; Boolean lại khai báo String. | Map từ identity result + audit/outbox; dùng Boolean/Array enum và chỉ rõ restrictions gồm học, nộp bài, link cộng đồng như `BD-11:148-155`. |
| 137-04 | P0 | `3.Data mapping!A15:H15` | Audit/notification và thay đổi trạng thái cross-service chưa có consistency/failure model. BD bắt buộc reason, actor và audit (`BD-11:139-155`, `170-180`). | Dùng saga/outbox phù hợp; audit before/after; notification sau khi trạng thái authoritative thành công; định nghĩa retry/compensation. |
| 137-05 | P0 | `2.Response!A9:E11` | Envelope cũ trái chuẩn `/api/v1` (`System_Architecture.md:632-700`). | Viết lại success/error theo chuẩn và businessCode cho invalid transition. |

## Điều kiện duyệt lại

- Có quyết định kiến trúc về account owner và sequence cross-service.
- Có test timed/permanent suspend, retry, audit và thực thi đủ restrictions.
