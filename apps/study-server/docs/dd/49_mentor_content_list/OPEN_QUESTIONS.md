# Open Questions — API #49 Lấy cây nội dung course

**Trạng thái DD:** Draft — Needs Confirmation  
**Endpoint:** `GET /api/v1/mentor/courses/{course_id}/content`

## Q-49-01 — Response shape của “cây”

**Implementation decision:** `Content[]` phẳng, `parent_id` nối node, không tạo nested `children[]` hoặc pagination. Catalog và AC-22 node đã được đồng bộ. Đây là quyết định code cần API/business owner xác nhận.

## Q-49-02 — Persistence của Content

**Implementation decision:** legacy BIGINT `contents` table trong `DB.sql` và migration `006_contents.sql`, gồm payload JSONB, parent cùng course, order và `deleted_at`. Migration chưa được xác minh/apply trên DB live. UUID V1-PILOT `content_blocks` không được dùng.

## Q-49-03 — Content schema và lifecycle

Còn cần xác nhận:

- Tập giá trị hợp lệ của `ContentType` và `ContentStatus`.
- Payload schema cho từng content type.
- Status transition, publish/readiness semantics và có trả draft cùng published không.
- Có cần audit/version history hoặc version selection. Bảng `contents` hiện chỉ lưu một row trạng thái, không có version history.
- Quy tắc khi node đang hoạt động có parent đã soft-delete.

API #49 hiện lưu/đọc type và status dạng open string, JSON object, trả mọi status, và trả 500 nếu parent node không có trong active result. Đây là current implementation behavior.

## Q-49-04 — Mentor identity and assigned-course access

Current source dùng Study JWT guard, numeric principal và direct predicate `courses.mentor_id = principal_id`. Cần product/security owner xác nhận liệu direct owner là đủ hay Mentor được phân công cũng cần truy cập; API hiện chưa kiểm tra assignment relation.

## Q-49-05 — 404 and empty result semantics

**Implementation decision:** malformed/out-of-range signed-int64 path và missing course trả 404; existing course with no active Content trả 200 với `data: []`; wrong role/owner trả 403. Đây là implementation resolution, chưa phải approval business.

## Q-49-06 — Versioning boundary với API #50–#53

Cần xác nhận #49 đọc revision nào, #51 revision update được lưu ở đâu, #52 publish version nào, và cách phân biệt draft/published khi Mentor tải lại cây. API #49 hiện trả mọi `status` từ `contents` và không chọn version.

## Q-49-07 — Soft-deleted node và active children

API #49 loại các row có `deleted_at`. Nếu node active trỏ tới parent đã soft-delete, parent reference thiếu trong kết quả và API trả 500 để không phát cây không nhất quán. Cần quyết định #53 có chặn xóa parent còn child, cascade soft-delete, hay cho phép ẩn subtree.
