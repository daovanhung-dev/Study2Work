# Câu hỏi còn mở — API #73

Trạng thái tài liệu: Draft — Needs Confirmation. Các điểm dưới đây ảnh hưởng trực tiếp đến implementation hoặc nhất quán nhóm AC-32.

1. **Category filter:** Course-category relation nằm ở table/column nào? Legacy `courses` không có `category_id`; API #73 hiện dùng fallback 422 trước DB theo API #06. Cần schema/source được duyệt để triển khai filter thay fallback.
2. **Admin authorization:** Shared JWT guard kiểm tra role `ADMIN`; AC-32 có yêu cầu course-management permission riêng không, và scope/numeric Admin identity lấy từ đâu?
3. **CourseStatus:** Các giá trị hợp lệ và casing là gì? #76 ghi draft/published/suspended; legacy/API #06 dùng `DRAFT`/`PUBLISHED`.
4. **Pagination:** Runtime dùng page mặc định 1, size cố định 20 và page 1-based theo precedent #06/#68; owner có chấp nhận các lựa chọn `DERIVED` này không?
5. **Sort:** Runtime dùng default `courses.id ASC` vì catalog không có sort; owner có chấp nhận thứ tự này không?
6. **Orphan mentor:** `courses.mentor_id` nullable nhưng `Course.mentor` bắt buộc. API #06 trả 500 nếu thiếu mentor; Admin có cần nhìn thấy course mồ côi để sửa thay vì fail toàn trang không?
7. **Optional category response:** Catalog có `Course.category?`, nhưng shared runtime Course model chưa khai báo field đó. Có cần cập nhật reusable schema sau khi relation source-backed?
8. **Null behavior:** Runtime shared Course serializes description, thumbnail and mentor avatar as null when source values are NULL; confirm this for the Admin projection.
9. **Schema/live DB:** Chọn legacy BIGINT hay V1-PILOT UUID/versioned model? Live schema chưa xác minh và hai model không tương đương.
10. **Error envelope/integration:** Đã cập nhật `DESIGN_CONTRACT_PATHS`; shared `error_response` emits `data:null`. Không còn implementation gap tại thời điểm này.
11. **AC-32 macro-review:** Đã rà #73–#77 sau khi #77 có DD; category/counters, wrapper singleton của #74–#76, dedicated Admin permission, enum/status casing, soft-delete visibility/persistence và route-template middleware cho #74–#77 còn mở.

## Ranh giới proposal

- Page default/size/order, exact-match semantics, all-status default và empty-page 200 được gắn `DERIVED`.
- Không tự tạo bảng/cột, enum hoặc permission source. Category 422 hiện tại là fallback `DERIVED`, cần owner/schema xác nhận trước khi coi là behavior chuẩn.
- Các proposal không thay đổi catalog, diagram, schema hoặc runtime.
## Rà nhóm AC-32 #73–#77 — 2026-10-24

- #73 giữ vai trò list/filter; `Page<Course>` là direct response, còn default/page size/order/all-status visibility là proposal.
- Sau #77 soft-delete, #73 nên ẩn deleted course; physical marker và predicate chưa được chọn nên đây vẫn là câu hỏi.
- Category filter chưa có relation source-backed; counters được nhắc trong flow detail nhưng không có field trong Course contract.
- Admin course-management guard chưa có source; CourseStatus casing và legacy BIGINT/V1-PILOT UUID model chưa được chốt; error path/envelope còn discrepancy.
