# Câu hỏi còn mở — API #73

Trạng thái tài liệu: Draft — Needs Confirmation. Các điểm dưới đây ảnh hưởng trực tiếp đến implementation hoặc nhất quán nhóm AC-32.

1. **Category filter:** Course-category relation nằm ở table/column nào? Legacy `courses` không có `category_id`; API #06 hiện từ chối filter này. Cần schema/source được duyệt để Q1 và Q2 dùng cùng predicate.
2. **Admin authorization:** JWT Admin claim, course-management permission, scope và numeric Admin identity lấy từ đâu? Study hiện chỉ có Student guard.
3. **CourseStatus:** Các giá trị hợp lệ và casing là gì? #76 ghi draft/published/suspended; legacy/API #06 dùng `DRAFT`/`PUBLISHED`.
4. **Pagination:** Catalog có `page` nhưng không có `size`; có chấp nhận page mặc định 1, size cố định 20 và page 1-based không? API #06 và proposal #68 là precedent, chưa phải approval cho #73.
5. **Sort:** Catalog không có sort. Có chấp nhận default `courses.id ASC` để ổn định pagination không?
6. **Orphan mentor:** `courses.mentor_id` nullable nhưng `Course.mentor` bắt buộc. API #06 trả 500 nếu thiếu mentor; Admin có cần nhìn thấy course mồ côi để sửa thay vì fail toàn trang không?
7. **Optional category response:** `Course.category?` có thể omit toàn bộ cho tới khi relation source-backed, hay cần sửa reusable schema/DB model?
8. **Null behavior:** Description, thumbnail và mentor avatar hiện được API #06 serialize thành null khi source NULL; xác nhận behavior này cho Admin Course projection.
9. **Schema/live DB:** Chọn legacy BIGINT hay V1-PILOT UUID/versioned model? Live schema chưa xác minh và hai model không tương đương.
10. **Error envelope/integration:** Khi wire route, cập nhật `DESIGN_CONTRACT_PATHS` cho `/api/v1/admin/courses`; chuẩn hóa error `data:null` theo guideline hay giữ helper hiện tại `{}`?
11. **AC-32 macro-review:** Đã rà #73–#77 sau khi #77 có DD; category/counters, wrapper singleton của #74–#76, Admin guard, enum/status casing, soft-delete visibility/persistence và error middleware còn mở.

## Ranh giới proposal

- Page default/size/order, exact-match semantics, all-status default và empty-page 200 được gắn `DERIVED`.
- Không tự tạo bảng/cột, enum, permission source hoặc category behavior.
- Các proposal không thay đổi catalog, diagram, schema hoặc runtime.
## Rà nhóm AC-32 #73–#77 — 2026-10-24

- #73 giữ vai trò list/filter; `Page<Course>` là direct response, còn default/page size/order/all-status visibility là proposal.
- Sau #77 soft-delete, #73 nên ẩn deleted course; physical marker và predicate chưa được chọn nên đây vẫn là câu hỏi.
- Category filter chưa có relation source-backed; counters được nhắc trong flow detail nhưng không có field trong Course contract.
- Admin course-management guard chưa có source; CourseStatus casing và legacy BIGINT/V1-PILOT UUID model chưa được chốt; error path/envelope còn discrepancy.
