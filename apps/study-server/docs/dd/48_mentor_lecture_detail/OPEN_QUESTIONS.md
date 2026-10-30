# Open Questions — API #48 Tải lecture của Mentor

**Trạng thái DD:** Draft — Needs Confirmation
**Endpoint:** GET /api/v1/mentor/lectures/{lecture_id}

Các quyết định dưới đây chưa có nguồn đủ để chuyển candidate thành implementation contract. Giữ nguyên catalog; không tạo field, bảng, enum hoặc business code để lấp chỗ trống.

## Q-48-01 — Migration assets trên môi trường chạy

**Bằng chứng**

- Lecture yêu cầu assets:UploadAsset[]; UploadAsset có id, name, url, content_type, size_bytes, status.
- Local API #47 parses `asset_refs` as an ordered JSON array of unique signed-int64 IDs and resolves them against API #34's `uploads` metadata.
- API #47 writes each validated ID and zero-based position to `lesson_uploads`; API #48 reads that relation and returns ordered metadata from `uploads`.
- `migrations/004_uploads.sql` and `migrations/005_lesson_uploads.sql` exist in the checkout. The live database has not been inspected.
- Legacy `resources` and V1-PILOT `file_objects` are not used for the UploadAsset projection.

**Cần xác nhận**

1. Has migration 005 been applied to every database environment that will run APIs #47/#48?
2. Is the local ordered `lesson_uploads` relation accepted as the business association contract?
3. Does the API owner confirm that a lecture without linked assets returns `assets: []`?

**Ảnh hưởng:** Local success mapping is implemented and tested; deployment and business confirmation remain open, so keep the DD Draft.

## Q-48-02 — Course ownership, phân công và Mentor identity

**Bằng chứng**

- AC-21 cho phép Mentor sở hữu hoặc được phân công course.
- #46/#47/#48 currently compare legacy `courses.mentor_id` with a numeric JWT subject through the shared Mentor guard.
- No assignment relation was found in inspected legacy artifacts; V1-PILOT uses a separate identity/schema model.

**Cần xác nhận**

1. Relation nào biểu diễn course được phân công cho Mentor?
2. JWT subject của Mentor là numeric users.id hay UUID subject?
3. Có dùng cùng một authorization helper/predicate cho #46, #47 và #48 không?

**Ảnh hưởng:** Query ownership, 403 behavior và việc AC-21 hỗ trợ course được phân công.

## Q-48-03 — Schema đích và quan hệ Lecture/Course

**Bằng chứng**

- Legacy DB.sql and migrations 004/005 use BIGINT courses/lessons/uploads; `lessons.course_id` is nullable while DB table guide describes it as required.
- V1-PILOT dùng UUID lessons theo chapter/course_version, không có cùng projection course_id/name/sort_order/status.
- Live schema chưa được xác minh.

**Cần xác nhận**

1. Does the target environment use the checked-in legacy BIGINT schema or V1-PILOT UUID schema?
2. Is migration 005 deployed, and is a missing parent course correctly treated as an integrity error?

**Ảnh hưởng:** Query, identifier type, parent authorization và projection course_id bắt buộc.

## Q-48-04 — Content nullable và cách serialize

**Bằng chứng**

- Lecture.content là optional string.
- Legacy lessons.content là TEXT NULL.
- API #47 gửi content:int64! và đã ghi discrepancy/decimal-string candidate.

**Cần xác nhận**

1. Does the API owner confirm returning JSON `null` when `lessons.content` is SQL NULL?
2. Is the existing #47 content-as-decimal-string behavior semantically correct for AC-21?

**Ảnh hưởng:** Tính ổn định response và mapping create → reload.

## Q-48-05 — LessonStatus values

**Bằng chứng**

- Legacy lessons.status có default DRAFT; catalog không liệt kê member của LessonStatus.
- Current API #47 implementation explicitly inserts `PUBLISHED`; API #48 returns the stored value without a status filter.
- AC-21 gọi #48 ngay sau #47; API #9 public curriculum lọc PUBLISHED nhưng khác role/workflow.

**Cần xác nhận**

1. What are the approved LessonStatus members?
2. Are stored statuses outside the current #47 `PUBLISHED` value allowed in Mentor detail responses?

**Ảnh hưởng:** Runtime returns the stored status as a string; the catalog enum remains unspecified.

## Q-48-06 — Path parse failure

**Bằng chứng**

- lecture_id:int64! là path parameter bắt buộc.
- Catalog #48 chỉ liệt kê 401/403/404/500; không khai báo 422.

**Cần xác nhận**

1. Does the API owner confirm that malformed or out-of-range path values map to the existing 404 code?
2. Should the catalog instead declare a validation response for those values?

**Ảnh hưởng:** Không thể thêm 422 vào DD nếu chưa sửa contract nguồn.

## Q-48-07 — Error envelope

**Bằng chứng**

- API Guidelines yêu cầu data:null ở error response.
- `app/core/responses.py` defaults error `data` to JSON null.
- API #48 uses the shared error helper and returns that shape in its local implementation.

**Cần xác nhận**

1. Does the API owner confirm the shared helper's `data: null` error envelope for this endpoint?
2. No helper change is currently required; revisit only if the contract owner requests another shape.

**Ảnh hưởng:** Expected contract và current helper representation khác nhau.

## Quyết định cần có trước khi DD chuyển Final

Ưu tiên xác nhận live legacy schema/migration 005, assigned-course and identity rules, content semantics, enum members, and malformed path mapping. Local source behavior and tests do not prove deployed DB compatibility or business approval. Keep status Draft — Needs Confirmation.
