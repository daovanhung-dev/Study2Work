# Open Questions — API #50 Tạo nội dung mới

**Trạng thái DD:** Draft — Needs Confirmation
**Endpoint:** `POST /api/v1/mentor/content`

Các câu hỏi này chặn implementation-ready persistence/access mapping. Không tự tạo physical table, enum member, payload field, business code hoặc HTTP status để lấp gap.

## Q-50-01 — Nguồn persistence của generic Content là gì?

**Bằng chứng**

- Catalog yêu cầu `ApiEnvelope<Content>` với BIGINT `id`, `course_id`, `parent_id?` và `order`.
- AC-22 diagram chỉ ghi logical `INSERT Content`.
- Legacy `DB.sql` không có generic Content table. V1-PILOT `content_blocks` dùng UUID `id` và `lesson_id`, không tương thích trực tiếp với catalog model.

**Cần xác nhận**

1. Bảng/model và migration nào lưu Content theo API contract?
2. Field/column mapping, foreign key tới course, ID strategy, transaction boundary và RETURNING projection là gì?
3. Có schema đã deploy nào tương ứng không? DDL hiện có không chứng minh live schema.

**Ảnh hưởng:** Chặn physical INSERT, source mapping và executable response projection.

## Q-50-02 — Enum `ContentType`/`ContentStatus` và payload schema là gì?

**Bằng chứng**

- Catalog chỉ đặt type `ContentType`, `ContentStatus`, `payload:object`; không liệt kê enum members hoặc cấu trúc theo subtype.
- AC-33 dùng trạng thái `PENDING_REVIEW` trong moderation queue.

**Cần xác nhận**

1. Allowed `content_type` values và mapping sang payload schema?
2. Validation bắt buộc/optional trong payload, kích thước tối đa, URI/asset reference rules?
3. `PENDING_REVIEW` có phải trạng thái khởi tạo chính thức của POST không, và enum status đầy đủ gồm gì?

**Ảnh hưởng:** Chặn validation 422 chi tiết và kiểm chứng nội dung response.

## Q-50-03 — Quy tắc quyền quản lý course và principal binding là gì?

**Bằng chứng**

- Catalog xác định Bearer JWT và role Mentor.
- AC-22 yêu cầu Mentor có quyền quản lý course.
- Legacy `courses.mentor_id` là direct-owner candidate; route chưa có identity binding và course assignment query.

**Cần xác nhận**

1. JWT claim nào map tới Mentor/course owner?
2. Mentor được assign/co-manage course có quyền tạo không?
3. Course tồn tại nhưng không được phép có luôn trả 403 không?

**Ảnh hưởng:** Chặn executable authorization query; 403 code có trong catalog.

## Q-50-04 — Parent, order và ID được gán thế nào?

**Bằng chứng**

- Request chỉ nhận `course_id`, `content_type`, `title`, `payload`.
- Response Content có `parent_id?` và `order`.

**Đề xuất cần xác nhận**

- Vì không có parent input, coi nội dung mới là root (`parent_id=null`).
- Cấp `order` kế tiếp trong các root cùng course; cần xác định base value, sort/tie-breaker, concurrency/locking và behavior sau xóa.
- ID do persistence layer sinh nhưng kiểu/key source cần khớp catalog BIGINT.

**Ảnh hưởng:** Chặn INSERT defaults và response fields `id`, `parent_id`, `order`.

## Q-50-05 — Course không tồn tại hoặc body có lỗi được map thế nào?

**Bằng chứng**

- Catalog API #50 có 401/403/422/500, không có 404.
- `course_id` là body field required; enum/payload schema chưa có.

**Cần xác nhận**

- `course_id` không tồn tại là 422 hay 403 trong contract hiện tại?
- Unknown enum member và payload subtype mismatch có luôn dùng 422 `DESIGN_VALIDATION_ERROR` không?
- Giá trị `title` rỗng/whitespace và int64 boundary được xác định ra sao?

**Ảnh hưởng:** Chặn error branch/source matrix chi tiết; không thêm code/status.

## Q-50-06 — Middleware và cross-API lifecycle có cần cập nhật khi wire route?

**Bằng chứng**

- API #50 hiện chưa có route. Middleware generic path allowlist hiện chưa chứa path này.
- AC-22 có #49–#53; AC-33 có approve/reject và audit behavior.

**Cần xác nhận khi implementation**

- Thêm route vào contract allowlist để validation/internal errors phát đúng `DESIGN_*` code.
- Chốt consistency giữa create→pending review, update #51, publish #52 và delete #53 trong macro-review AC-22.
- Xác định audit/review metadata ở schema/API nào; không tự thêm cột trong #50.

**Ảnh hưởng:** Contract business codes và lifecycle consistency sau khi API được nối.

## Q-50-07 — Content PENDING_REVIEW có thể bị Mentor xóa không?

API #50 đề xuất tạo Content ở PENDING_REVIEW. API #53 đề xuất soft-delete Content không PUBLISHED khi không còn direct child; điều này có thể rút Content khỏi AC-33 queue nhưng diagram không mô tả withdrawal/audit. Cần xác nhận quyền xóa pending item và cách queue giữ review history.
