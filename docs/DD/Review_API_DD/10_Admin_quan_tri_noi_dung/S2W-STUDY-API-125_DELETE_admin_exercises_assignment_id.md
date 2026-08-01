# Review API DD — S2W-STUDY-API-125

- DD source: `docs/DD/Study2Work_DD_API/10_Admin_quan_tri_noi_dung/S2W-STUDY-API-125_DELETE_admin_exercises_assignment_id.xlsx`
- Method + endpoint: `DELETE /api/v1/admin/exercises/{assignment_id}`
- Kết luận: **CẦN SỬA**

## Findings

| Severity | Sheet + cell | Mô tả cụ thể | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P1 | `00.Hướng dẫn!A4:B4`, `Cover!B19` | Nguồn 44 file/không schema đã stale. | SQL `:1-31`; canonical `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Cập nhật inventory/precedence. |
| P0 | `2.Response!D9:D11`, `2.Response!A33` | Envelope/error cũ trái canonical. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Dùng canonical response nếu có body. |
| P0 | `2.Response!B9:E9`, `2.Response!A22` | Chọn `204` nhưng vẫn định nghĩa body `deleted_or_archived/submission_count/audit_id` và pagination mẫu. | Chính DD `2.Response!E9`; canonical meta `docs/BD/base/0. Study2Work_System_Architecture.md:693-700` | Chọn `200`+body hoặc `204` no-body; bỏ pagination. |
| P1 | `3.Data mapping!A20`, `00.Hướng dẫn!A13:B18` | SOFT_DELETE còn `<mapping>`/generic predicate dù checklist đã tick. | `docs/BD/base/0. Study2Work_System_Architecture.md:601-628,738-752` | Viết archive/delete guard, lock và audit cụ thể. |
| P0 | `5.DB_Update_Main!B8:I10` | DD dùng `status/deleted_at/updated_*`; exercises chỉ có `publish_status`, không có soft-delete metadata. | SQL `:486-500` | Archive qua `publish_status='ARCHIVED'` hoặc bổ sung migration; không dùng cột ảo. |
| P0 | `3.Data mapping!D12:D14` | Hard delete exercise sẽ cascade toàn bộ `exercise_submissions`, phá lịch sử bài nộp — trái mục tiêu API. | SQL `:508-529`; bảo toàn lịch sử archived BD-10 `:181` | Nếu có submission/đã publish thì chỉ archive/version; hard delete chỉ DRAFT unused với guard. |
| P1 | `1.Request!D22:E22`, `6.DB_Update_Related!A12:I12` | Reason bắt buộc là đúng nhưng chưa có audit before/after, submission count lock/snapshot và notification impact. | BD-10 `:163-167,182-193`; audit SQL `:691-719` | Count/lock relevant state, audit atomic, notify affected learners khi cần; không cascade submission. |

## Checklist duyệt lại

- [ ] Source/envelope/status-body consistency đã sửa.
- [ ] Không còn pagination.
- [ ] Archive dùng `publish_status`/migration thật.
- [ ] Hard-delete chỉ DRAFT unused.
- [ ] Submission history không bị cascade.
- [ ] Reason/audit/lock atomic.
- [ ] Impact/notification policy rõ.
- [ ] Test zero/many submissions, retry và concurrent submit/delete.
