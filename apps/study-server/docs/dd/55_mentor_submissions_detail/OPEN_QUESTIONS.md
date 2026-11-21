# Open Questions — Study API #55 Lấy bài làm và rubric Mentor

**Trạng thái DD:** Draft — Needs Confirmation
**Endpoint:** `GET /api/v1/mentor/submissions/{submission_id}`

Các fallback `DERIVED` dưới đây được dùng trong source local để tiến hành theo catalog; chúng không xác nhận schema live hoặc business policy. Các gap ảnh hưởng response, schema hay authorization vẫn cần owner xác nhận.

## Q-55-01 — Rubric trong flow nhưng không có trong Submission response

**Bằng chứng**

- AC-23 node #55 yêu cầu backend đọc `Submission + files + rubric`.
- Catalog khai báo response `ApiEnvelope<Submission>`; reusable `Submission` không có field rubric.
- API #56 nhận `rubric items:string!` nhưng không định nghĩa cấu trúc chuỗi/rubric items.
- Legacy `assignments`/`assignment_submissions` không có rubric field hoặc relation được mô tả.

**Đề xuất đơn giản (DERIVED)**

- Giữ response API #55 đúng reusable `Submission`; không thêm rubric vào `data` hoặc `meta`.
- Cập nhật catalog/schema và diagram cùng lúc nếu rubric phải được trả từ API #55; định nghĩa wire shape trước khi implementation.

**Cần xác nhận**

1. AC-23 có yêu cầu API #55 trả rubric cho client hay rubric chỉ là dữ liệu nội bộ để xử lý bước chấm?
2. Nếu trả, rubric nằm ở field/type nào và liên kết với Assignment/Submission bằng khóa nào?

**Ảnh hưởng:** API response, client grade UI, Query Matrix và tương thích API #56.

## Q-55-02 — Nguồn và cấu trúc `files: UploadAsset[]`

**Bằng chứng**

- Reusable `Submission.files` là array `UploadAsset[]` với id, name, url, content_type, size_bytes, status.
- Legacy `assignment_submissions` chỉ có một nullable `file_url`.
- API #34 exposes uploads metadata. APIs #54 and #55 use a DERIVED exact URL/owner/purpose/course lookup, but API #35/#36 do not confirm that `file_url` stores this URL.

**Đề xuất đơn giản (DERIVED)**

- Reuse the API #54 DERIVED constrained lookup; return `files: []` only when no matching metadata row exists, without fabricating assets.
- Confirm API #35 file reference persistence and whether #55 should reuse this DERIVED lookup or a future approved association.

**Cần xác nhận**

1. Một submission được gắn một hay nhiều upload asset?
2. Asset ID/metadata/URL policy được lưu và tra từ đâu; có filter theo owner, course, purpose hoặc status không?

**Ảnh hưởng:** Response đầy đủ, storage access control và tương thích các API submission.

## Q-55-03 — Không tương thích giữa rubric V1-PILOT và assignment submission

**Bằng chứng**

- `infra/postgres/02_study_db.sql` định nghĩa `rubrics.assessment_id UUID` → `assessments.id` và `rubric_criteria.rubric_id UUID`.
- Legacy `assignment_submissions`/`assignments` dùng BIGINT; không có relation đến `assessments` hoặc `rubrics`.
- Hai bộ DDL là artifacts khác model; live metadata chưa được kiểm tra.

**Đề xuất đơn giản (DERIVED)**

- Không join chéo UUID assessment sang BIGINT assignment bằng ID hoặc quy đổi tự suy đoán.
- Chỉ dùng rubric model sau khi domain owner định nghĩa relation assignment/rubric trong schema và API contract.

**Ảnh hưởng:** Không thể tạo query rubric có thể lập trình từ nguồn hiện tại.

## Q-55-04 — Mentor identity, assignment scope và 403/404

**Bằng chứng**

- AC-23 precondition yêu cầu Mentor có quyền chấm submission của course.
- Current JWT helper dùng `sub` numeric user ID và `roles`; shared request guard accepts an explicit MENTOR role; #55 now uses it, while direct-owner rule remains DERIVED.
- Legacy DB có `courses.mentor_id`; không có assignment relation cho Mentor được phân công.
- Catalog có cả 403 và 404; API #36 cũng giữ câu hỏi về access/masking.

**Đề xuất đơn giản (DERIVED)**

- Tái dùng decoder/claim parser hiện tại, yêu cầu role `MENTOR`, lấy numeric `sub` làm principal.
- So sánh `courses.mentor_id` với principal như direct-owner candidate; bản ghi không tồn tại → 404, owner khác → 403.

**Cần xác nhận**

1. Course được phân công có được chấm không và quan hệ nào thể hiện assignment?
2. Submission tồn tại ngoài scope trả 403 hay được mask thành 404?
3. Mentor role/ID có cùng claim shape và `users.id` numeric trong target schema không?

**Ảnh hưởng:** Kiểm soát truy cập, nguy cơ lộ sự tồn tại và dữ liệu giữa course.

## Q-55-05 — FK nullable và schema target

**Bằng chứng**

- DB table guide/ERD mô tả `assignment_id` và `user_id` là FK bắt buộc.
- Legacy `infra/postgres/study-server/DB.sql` cho phép NULL ở cả hai; `assignments.course_id` cũng nullable.
- `infra/postgres/02_study_db.sql` là V1-PILOT UUID model khác; live schema chưa xác minh.

**Đề xuất đơn giản (DERIVED)**

- Với candidate logic, row thiếu `assignment_id`, assignment/course hoặc `user_id` không được map thành `Submission`; current source uses 500 integrity error as a DERIVED fallback until the owner confirms the rule.

**Cần xác nhận**

1. DDL/schema nào là target của API #55?
2. Có cần sửa nullability/migrate legacy records trước khi triển khai không?

**Ảnh hưởng:** Query joins, response bắt buộc và availability của API.

## Q-55-06 — Grade/status và hiển thị cho Student

**Bằng chứng**

- `Submission.score` là optional `decimal-string`; candidate column `score NUMERIC(6,2)`.
- `Assignment.max_score` là `decimal-string`; API #56 nhận `score:int32`.
- AC-17 nêu trạng thái `SUBMITTED`, AC-23 #56 chuyển sang `GRADED`; đầy đủ `SubmissionStatus` chưa có.
- AC-23 nói Student có thể nhận kết quả; API #36 chưa chốt thời điểm hiển thị score/feedback.

**Đề xuất đơn giản (DERIVED)**

- API #55 returns stored score/feedback through the reusable Submission shape and omits null optional fields in current source; contract null/omit and Student visibility remain open.
- Đồng bộ đơn vị/range/precision `score`, `max_score` và #56 body trước implementation.

**Cần xác nhận**

1. #56 `score:int32` là tổng điểm theo rubric hay điểm normalized; giới hạn nào áp dụng so với `max_score`?
2. SubmissionStatus có những member/transition nào?
3. API #36 chỉ trả score/feedback sau khi hành động publish nào?

**Ảnh hưởng:** API #55 projection, tính đúng điểm và dữ liệu Student thấy.

## Q-55-07 — Malformed `submission_id`

**Bằng chứng**

- Catalog yêu cầu `submission_id:int64!` nhưng error set không có 400/422.
- API #55 parses a raw path string and maps malformed/overflow values to 404 following the existing API #48 pattern.

**Đề xuất đơn giản (DERIVED)**

- Int64 hợp lệ không tìm thấy row → 404. Malformed/overflow → 404 `DESIGN_RESOURCE_NOT_FOUND` as a DERIVED fallback; no 422 branch is added.

**Ảnh hưởng:** Router validation và exact error set.

## Q-55-08 — Error envelope và middleware path

**Bằng chứng**

- API Guidelines yêu cầu `data:null` trên lỗi.
- Current `error_response()` serializes `data=None` as JSON null.
- Middleware `DESIGN_CONTRACT_PATHS` now includes the API #55 FastAPI route template.

**Đề xuất đơn giản (DERIVED)**

- Keep the catalog code and guideline envelope; current `error_response()` emits `data:null`, and API #55 returns its responses through that helper. No helper change is needed for this endpoint.

**Ảnh hưởng:** Client error parsing và implementation contract.

## Q-55-09 — API #54 collection fallback and client compatibility

**Bằng chứng**

- AC-23 nối #54 đọc danh sách → chọn một submission → gọi #55 bằng `submission_id`.
- API #54 implementation and updated catalog/diagram now use `ApiEnvelope<Page<Submission>>` as a DERIVED fallback for the AC-23 list/select flow.
- API #55 accepts the selected `submission_id` on the path and has no query/body that replaces the list selection.

**Đề xuất đơn giản (DERIVED)**

- Contract owner should confirm the DERIVED collection change and client compatibility. Current #54 fallback uses page 1, fixed size 20 and `submitted_at DESC, id DESC` order.
- API #55 now reuses the API #54 constrained API #34 `uploads` match unless the API #35 producer contract specifies another asset key.

**Ảnh hưởng:** API #55 can consume IDs from the current page, but final contract approval and API #35 file-reference compatibility remain open.

## Trạng thái

Giữ `Draft — Needs Confirmation`. API #55 runtime implements the catalog Submission shape with DERIVED direct-owner/path/integrity/file fallbacks. Rubric mapping, assigned-Mentor policy, live schema/nullability, grade/status semantics and API #35 file-reference compatibility remain unresolved.


Macro-review AC-23 #54–#57 was refreshed after #54/#55 local implementation. The collection/file/owner/path fallbacks remain DERIVED and await owner confirmation; rubric and grade/status gaps remain.
