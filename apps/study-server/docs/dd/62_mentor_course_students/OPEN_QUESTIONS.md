# OPEN_QUESTIONS — Study API #62

Trạng thái: `Draft — Needs Confirmation`. Giữ nguyên contract trực tiếp; mọi khuyến nghị dưới đây là DERIVED và chưa được duyệt.

<a id="q-62-01-response-resource"></a>

| ID | Câu hỏi cần xác nhận | Bằng chứng và ảnh hưởng | Khuyến nghị đơn giản | Mức độ |
|---|---|---|---|---|
| Q-62-01 | Item của response là Course hay học viên/người nhận? | Catalog khai báo `Page<Course>`; endpoint `/students` và AC-25 yêu cầu learner ghi danh. Không thể map roster row thành Course. | Sửa contract sang `Page<UserSummary>` để dùng schema có sẵn gồm id/full_name/avatar_url; cần owner phê duyệt. | BLOCKING — contract |
| Q-62-02 | Có query page/size không; default/max/order là gì? | PageMeta bắt buộc nhưng request chỉ có course_id; client không thể yêu cầu trang tiếp theo. | Nếu cần phân trang, thêm page/size sau khi cập nhật catalog. | BLOCKING — pagination |
| Q-62-03 | Schema canonical là legacy BIGINT `enrollments` hay V1-PILOT UUID `course_enrollments`? | Khác ID, relation và identity/profile; live schema chưa được xác minh. | Chọn schema trước khi viết SQL runtime. | BLOCKING — persistence |
| Q-62-04 | “Active” gồm những trạng thái nào; có gửi cho learner đã COMPLETED không? | Diagram nói active; legacy chỉ có VARCHAR default ACTIVE; pilot enum là ENROLLED/IN_PROGRESS/COMPLETED. | Duyệt predicate theo schema được chọn; không trộn hai bộ trạng thái. | BLOCKING — eligibility |
| Q-62-05 | Một learner có thể xuất hiện nhiều lần; tổng đếm theo learner hay enrollment? | Legacy thiếu unique course/user; pilot unique theo learner/course version nhưng một course có thể có nhiều version. | Danh sách người nhận nên unique theo learner; xác nhận grain của total. | BLOCKING — semantics người nhận |
| Q-62-06 | Quyền Mentor dựa trên ownership, assignment hay cả hai; JWT claim nào map vào key? | AC-25 yêu cầu quyền với course; legacy có mentor_id, pilot có owner_subject_id; guard hiện tại chỉ Student. | Duyệt một scope rule dùng chung cho các API AC-25. | BLOCKING — authorization |
| Q-62-07 | Có ẩn learner account/profile bị khóa, xóa hoặc private không? | Legacy users có status; pilot learner_profiles có deleted_at/profile_visibility; diagram không nói. | Chỉ trả projection tối thiểu đã được phép. | BLOCKING — privacy |
| Q-62-08 | #63 encode `recipients:string!` thế nào; dùng user ID hay enrollment ID? | Catalog chỉ định string opaque; ID khác giữa schema candidates. | Chọn encoding tường minh và thống nhất với key #62 trả. | BLOCKING — integration |
| Q-62-09 | Course thiếu, ngoài quyền hoặc roster rỗng có behavior nào? | Catalog có 403/404; diagram chưa chốt thứ tự privacy hoặc empty behavior. | Thiếu→404, ngoài scope→403, roster rỗng→200 empty page là proposal cần xác nhận. | NEEDS CONFIRMATION |
| Q-62-10 | Error envelope dùng `data:null` hay `{}` khi API được wired? | Guideline yêu cầu null; helper hiện mặc định `{}`; path chưa allowlist. | Đồng bộ helper và middleware khi triển khai route. | BLOCKING — future wiring |

## Ranh giới đã giữ

- #62 chỉ đọc; #63 tạo và phát; #64 theo dõi delivery status.
- Không thêm query/response field, table, enum, error code hoặc encoding người nhận.
- `Page<UserSummary>` và `status='ACTIVE'` vẫn là đề xuất DERIVED.


## Macro-review AC-25 sau DD #64

- Macro-review #62–#64 cùng API #18 đã hoàn tất ở mức tài liệu với trạng thái `VERIFIED_WITH_OPEN_QUESTIONS`; xem [API #64 verification report](../64_mentor_notifications_status/VERIFICATION_REPORT.md).
- Các câu hỏi Q-62-01/02/03/04/05/06/08 còn chặn contract roster, pagination, schema, eligibility, ID và quyền Mentor; không tự chọn phương án trong review nhóm.
