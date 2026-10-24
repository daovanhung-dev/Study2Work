# Open Questions — Study API #55 Lấy bài làm và rubric Mentor

**Trạng thái DD:** Draft — Needs Confirmation
**Endpoint:** `GET /api/v1/mentor/submissions/{submission_id}`

Các đề xuất `DERIVED` dưới đây là hướng thiết kế đơn giản để tiến hành; chúng không thay đổi catalog hoặc chứng minh runtime. Các gap ảnh hưởng response, schema hay authorization vẫn cần owner xác nhận trước khi implementation.

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
- API #34 upload chưa có relation được duyệt để tra asset metadata; API #35/#36 có cùng gap.

**Đề xuất đơn giản (DERIVED)**

- Không biến `file_url` thành asset giả và không ép `files: []` cho bản ghi thật.
- Chốt association/metadata resolver dùng chung cho #35, #36, #54 và #55 trước khi triển khai mapping.

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
- Current JWT helper dùng `sub` numeric user ID và `roles`; shared request guard hiện chỉ cho Student.
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

- Với candidate logic, row thiếu `assignment_id`, assignment/course hoặc `user_id` không được map thành `Submission`; dùng 500 integrity error đến khi owner chốt quy tắc.

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

- API #55 trả score/feedback hiện lưu nếu contract field có giá trị, nhưng chưa quy định null/omit; không tự suy ra publish/visibility transition.
- Đồng bộ đơn vị/range/precision `score`, `max_score` và #56 body trước implementation.

**Cần xác nhận**

1. #56 `score:int32` là tổng điểm theo rubric hay điểm normalized; giới hạn nào áp dụng so với `max_score`?
2. SubmissionStatus có những member/transition nào?
3. API #36 chỉ trả score/feedback sau khi hành động publish nào?

**Ảnh hưởng:** API #55 projection, tính đúng điểm và dữ liệu Student thấy.

## Q-55-07 — Malformed `submission_id`

**Bằng chứng**

- Catalog yêu cầu `submission_id:int64!` nhưng error set không có 400/422.
- API #55 chưa có route; behavior parse path hiện tại chưa tồn tại.

**Đề xuất đơn giản (DERIVED)**

- Int64 hợp lệ không tìm thấy row → 404. Path không parse được/overflow cần được map sang một trong các status catalog hoặc cập nhật catalog; không thêm 422 ngầm.

**Ảnh hưởng:** Router validation và exact error set.

## Q-55-08 — Error envelope và middleware path

**Bằng chứng**

- API Guidelines yêu cầu `data:null` trên lỗi.
- Current `error_response()` dùng `{}` khi `data=None`.
- Middleware `DESIGN_CONTRACT_PATHS` hiện không có API #55.

**Đề xuất đơn giản (DERIVED)**

- Giữ expected catalog code và guideline envelope trong DD; khi wiring, tích hợp path vào mapping middleware và quyết định cập nhật helper hay guideline để thống nhất `data`.

**Ảnh hưởng:** Client error parsing và implementation contract.

## Q-55-09 — API #54 không có collection response cho bước chọn

**Bằng chứng**

- AC-23 nối #54 đọc danh sách → chọn một submission → gọi #55 bằng `submission_id`.
- API #54 catalog response hiện là `ApiEnvelope<Submission>` đơn lẻ dù tên endpoint là danh sách; DD #54 đã ghi cardinality question.
- API #55 chỉ nhận `submission_id` trên path và không có query/body để thay thế bước chọn.

**Đề xuất đơn giản (DERIVED)**

- Nếu UI cần chọn từ danh sách, owner cần cập nhật catalog/schema API #54 sang collection response trong một contract change được duyệt.
- Tới khi contract owner chốt thay đổi đó, DD #54/#55 giữ nguyên contract catalog hiện tại và tiếp tục ghi nhận mismatch; không tự đổi response shape.
- Vì #54 có `page` query, owner nên chốt `Page<Submission>` cùng size/default/order/meta hoặc bỏ pagination contract đồng bộ; không giả định một quy ước trong DD #55.

**Ảnh hưởng:** AC-23 không thể chạy end-to-end nếu #54 không trả danh sách có ID để mở #55.

## Trạng thái

Giữ `Draft — Needs Confirmation`. Contract method/path/auth/path type/success/error đã khóa theo catalog; handoff collection từ #54, rubric, asset mapping, Mentor access, schema/nullability, grade/status semantics và error serialization chưa đủ nguồn để coi DD là implementation-ready.


Macro-review AC-23 #54–#57 đã hoàn tất ở mức tài liệu. Các mismatch và gap trong nhóm vẫn giữ mở; không có contract nào được tự thay đổi.