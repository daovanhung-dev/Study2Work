# OPEN_QUESTIONS — Study API #62

Trạng thái: `Draft — Needs Confirmation`. API #62 đã được wire theo fallback local; các lựa chọn DERIVED chưa phải product/schema approval.

| ID | Câu hỏi còn mở | Current implementation | Vì sao cần xác nhận |
|---|---|---|---|
| Q-62-01 | Có chấp thuận `ApiEnvelope<UserSummary[]>` không phân trang thay cho `Page<Course>` ban đầu? | Đồng bộ catalog/AC-25 diagram và runtime với recipient roster; request vẫn chỉ có `course_id`. | Đây là contract change cần API/product owner duyệt. |
| Q-62-02 | Runtime database có dùng legacy BIGINT `courses/enrollments/users` không? | Code dùng các bảng trong `infra/postgres/study-server/DB.sql`; không dùng V1-PILOT UUID. | Checked-in DDL và local tests không xác minh live schema/migration. |
| Q-62-03 | Eligibility active enrollment có chỉ là `status='ACTIVE'` không? | Exact legacy predicate `ACTIVE`; lọc `users.role='STUDENT'`; không lọc `users.status`. | Legacy status là VARCHAR và không có full lifecycle enum; AC-25 không định nghĩa account-status/privacy filtering. |
| Q-62-04 | Mentor được phân công nhưng không phải `courses.mentor_id` owner có được đọc roster không? | Chỉ direct owner theo pattern hiện hành API #46/#49/#54. | Legacy schema được chọn không có assignment relation cho API này. |
| Q-62-05 | API #63 phải encode `recipients:string!` bằng JSON, CSV hay định dạng khác? | #62 trả `UserSummary.id` numeric và không serialize cho API #63. | #63 request catalog chưa định nghĩa ID encoding; cần thống nhất giữa hai API. |

## Đã xử lý bằng fallback

- `Page<Course>` không biểu diễn roster trong AC-25; không tạo Course giả.
- PageMeta không thể điều hướng trang vì request không có page/size; không tự đặt page size.
- Legacy và V1-PILOT không được trộn schema, ID hoặc enrollment status.
- Course thiếu trả 404; owner mismatch trả 403; roster rỗng trả 200 `data: []`.
- Fallback giữ trạng thái `DERIVED — Draft — Needs Confirmation` cho đến khi owner phê duyệt.
