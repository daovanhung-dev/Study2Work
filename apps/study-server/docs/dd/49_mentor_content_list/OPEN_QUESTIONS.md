# Open Questions — API #49 Lấy cây nội dung course

**Trạng thái DD:** Draft — Needs Confirmation  
**Endpoint:** `GET /api/v1/mentor/courses/{course_id}/content`

Các câu hỏi dưới đây ảnh hưởng trực tiếp tới response/query/authorization. Không tự tạo bảng, enum, payload key hoặc business code để lấp khoảng trống.

## Q-49-01 — “Cây” được biểu diễn thế nào trong response?

**Bằng chứng**

- Tên API và AC-22 diagram mô tả đọc cây sections/lessons/content.
- Catalog chỉ trả `ApiEnvelope<Content>`; reusable Content có `parent_id?` nhưng không có `children[]` hay `Page<Content>`.

**Cần xác nhận**

1. Endpoint trả một root Content, danh sách nodes, hay nested tree?
2. Nếu nested, field con và thứ tự node được khai báo ở contract nào?
3. Course không có nội dung trả object rỗng, collection rỗng, hay 404?

**Ảnh hưởng:** Chặn response shape và success example có thể chạy.

## Q-49-02 — Nguồn persistence của Content

**Bằng chứng**

- Legacy DB guide/ERD có `courses`, `lessons`, `resources` nhưng không có generic Content/sections/parent-content table.
- V1-PILOT DDL có `chapters`, `lessons`, `content_blocks` với UUID và quan hệ course-version; model khác contract BIGINT/`Content.parent_id`.

**Cần xác nhận**

1. API #49 dùng schema nào trong hai mô hình, hay có schema khác?
2. Bảng/column/PK/FK/version/filter đã được duyệt cho tree read là gì?
3. Live schema nào đã được deploy và xác minh?

**Ảnh hưởng:** Q2 query và tất cả Content field mappings hiện `SOURCE_REQUIRED`.

## Q-49-03 — Content schema và lifecycle

**Bằng chứng**

- `ContentType`, `ContentStatus`, `payload:object`, `parent_id?`, `order` có trong reusable schema.
- Catalog không liệt kê enum values, payload members, null/omit policy, sibling order hoặc draft/published visibility.

**Cần xác nhận**

Enum members, payload schema/version, parent semantics, ordering/tie-breaker, visibility filters, and null/empty/omit rules.

**Ảnh hưởng:** Response mapping, validation and future API #50–#53 compatibility.

## Q-49-04 — Mentor identity and assigned-course access

**Bằng chứng**

- AC-22 precondition yêu cầu Mentor có quyền quản lý course.
- Legacy `courses.mentor_id` supports a direct-owner candidate; assignment relation and current Study Mentor token binding are not source-backed.
- V1-PILOT uses `owner_subject_id uuid` and course UUID.

**Cần xác nhận**

1. Mentor principal maps to which identity and key?
2. Is access limited to direct owner, or can assigned Mentors manage the course?
3. Which approved relation/policy evaluates assigned-course access?

**Ảnh hưởng:** Candidate Q1 does not fully implement authorization; 403 branch is not implementation-ready.

## Q-49-05 — 404 and malformed path semantics

**Bằng chứng**

- Catalog declares 404 but does not identify whether it means missing course, missing content root or both.
- No 422 is declared for invalid `course_id`.

**Cần xác nhận**

Define missing-course, missing-tree, empty-course, malformed/overflow path outcomes without changing the declared error set unless contract is updated. Current middleware fallback is HTTP 422 `VALIDATION_ERROR` outside its allowlist; confirm how future #49 route preserves the catalog set.

**Ảnh hưởng:** Error mapping and framework parse behavior.

## Q-49-06 — Versioning boundary with API #50–#53

**Bằng chứng**

- AC-22 has create/update/delete/publish endpoints after this GET.
- Pilot schema makes published course versions immutable and has draft/version fields; AC-22 contract does not state version selection or draft behavior.

**Cần xác nhận**

Which draft/published version #49 returns, how it relates to mutation APIs, and whether each Mentor sees own draft or latest published content.

**Ảnh hưởng:** Tree query predicates and coherent AC-22 behavior.

## Q-49-07 — Cây nội dung lọc soft-deleted node thế nào?

AC-22 yêu cầu reload cây sau DELETE; API #53 đề xuất soft-delete và loại Content đã xóa khỏi active views. Catalog #49 hiện chỉ trả một Content, không khai báo children collection hoặc deleted marker. Cần xác nhận query/tree shape và quy tắc ẩn node đã xóa để nội dung không xuất hiện lại sau reload.
