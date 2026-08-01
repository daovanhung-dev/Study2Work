# Review S2W-STUDY-API-141 — GET learner audit

- DD nguồn: `docs/DD/Study2Work_DD_API/11_Admin_quan_ly_hoc_vien_va_ho_tro_ngoai_le/S2W-STUDY-API-141_GET_admin_learners_learner_id_audit.xlsx`
- Endpoint: `GET /api/v1/admin/learners/{learner_id}/audit`
- Kết luận: **CẦN SỬA — query audit hiện không chạy được**

## Các điểm cần sửa

| ID | Mức độ | Vị trí DD | Nhận xét và căn cứ BD | Cách sửa |
|---|---|---|---|---|
| 141-01 | P0 | `1.Request!A22:J26` | `action_type` khai báo Object cho query, trong khi audit action là enum/string; query dùng snake_case trái convention camelCase. | Dùng `action` enum/repeated key nếu nhiều giá trị; `from/to/page/pageSize` theo chuẩn. |
| 141-02 | P0 | `3.Data mapping!A12:H20` | DD lọc `audit_logs.user_id`, `action_type`, `from`, `to`, nhưng schema có `actor_id`, `action`, `target_type/target_id`, `support_request_id`, `created_at` (`schema_seed.sql:691-732`). | Xác định learner là target nào; lọc target/support request đúng và dùng `created_at >= :from AND < :to`; viết SQL thực thi được. |
| 141-03 | P0 | `1.Request!A10:D10`, `4.Error!A11:H11` | Permission dùng `study.admin.manage`; SEQ-14 yêu cầu `audit.read` (`SEQ-14:33-38`) và BD chỉ cho người có quyền phù hợp xem (`BD-13:200-209`). | Dùng permission read riêng, scope theo learner; không trao audit read chỉ vì có quyền admin mutation. |
| 141-04 | P1 | `2.Response!A15:H20` | `data` là Array nhưng chỉ có field `data.audit` kiểu String; không hề khai báo actor/action/target/before/after/reason tối thiểu theo `BD-13:187-198`. | Định nghĩa từng audit item và redaction/minimization; map đúng cột. |
| 141-05 | P0 | `2.Response!A9:E11` | Envelope/pagination cũ trái `System_Architecture.md:632-721`. | Dùng envelope chuẩn, `meta.pagination` và traceId. |

## Điều kiện duyệt lại

- Có định nghĩa learner-target và SQL/filter đúng schema.
- Có permission `audit.read`, redaction policy và test chống lộ secret/PII.
