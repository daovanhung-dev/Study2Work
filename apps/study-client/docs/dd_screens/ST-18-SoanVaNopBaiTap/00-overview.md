# ST-18 — Soạn và nộp bài tập · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `ST-18` |
| Module | Student |
| Route | `/student/assignments/:assignmentId/submit` — Study Client route; deployed runtime chưa xác minh |
| Actor/role | Student Bearer; #34 and #35 validate Student role |
| DD status | Eligibility/duplicate-recovery/visual gaps open; **Implementation:** PARTIAL · **Runtime:** NOT VERIFIED. #33–#35 and client callers exist. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.2 / 2026-11-20 |
| Nguồn đối chiếu | [ST-18.md](../../screen_stitch/03_student/ST-18_soan-va-nop-bai-tap/ST-18.md), [ST-18_PLAN.md](../../screen_stitch/03_student/ST-18_soan-va-nop-bai-tap/ST-18_PLAN.md), [ST-18_markers.json](../../screen_stitch/03_student/ST-18_soan-va-nop-bai-tap/ST-18_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Soạn nội dung, file đính kèm, kiểm tra tiến độ upload/nộp một lần.
- In-scope: GET #33 → POST #34 cho từng file khi cần → thu asset reference → POST #35 → nhận submission_id. Tách trạng thái upload thành công khỏi submission thành công; F06 chưa chốt giữ draft/nội dung qua lỗi.
- Out-of-scope: Không áp dụng giới hạn file không có trong API; live runtime chưa xác minh.

### Current implementation — 2026-11-20

- ST-18 loads assignment #33 reactively, validates its response, and supports retry. It permits text and at most one uploaded asset: #34 receives `file`, `purpose=SUBMISSION`, and `course_id`; #35 receives `content` and `upload_id`.
- #34 checks ACTIVE enrollment when `course_id` is supplied; ST-18 supplies it. #35 checks Student, assignment existence, ACTIVE enrollment, deadline and ownership/course/purpose of the selected upload, then creates a new `SUBMITTED` row and returns `data.id`. The client requires `DESIGN_RESOURCE_CREATED`, matching assignment ID and `SUBMITTED` status before navigating to ST-19 using that ID. It suppresses repeat after an ambiguous outcome or accepted submission; after a page reload the ambiguity/idempotency state cannot be recovered. #34 confirmation also requires `DESIGN_RESOURCE_CREATED` and `UPLOADED` status.
- Upload and submission are separate. The form locks fields while submitting and retains a successful upload if #35 returns a definitive error. It does not expose the upload URL.
- #33 itself does not enforce assignment ownership/enrollment/status. #34 accepts any size/MIME in application source and returns a public-base URL. The DD's many-file/checklist/loaded screen content and visual alignment remain incomplete. Runtime/tests were not verified.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-17 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Soạn nội dung, file đính kèm, kiểm tra tiến độ upload/nộp một lần. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #33, #34, #35
- Liên kết màn hình dự kiến: [ST-19](../ST-19-BaiDaNopVaPhanHoi/00-overview.md), [ST-17](../ST-17-ChiTietBaiTap/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | editing/uploading/submitting/failed/submitted |
| Current source | Study Client ST-18 | `loading / editing / uploading / submitting / error / ambiguous / receipt link`; deployed runtime NOT VERIFIED |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [ST-18 source screen.png](../../screen_stitch/03_student/ST-18_soan-va-nop-bai-tap/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/03_student/ST-18_soan-va-nop-bai-tap/screen_annotated.png))
- Luồng: GET #33 → POST #34 cho từng file khi cần → thu asset reference → POST #35 → nhận submission_id. Tách trạng thái upload thành công khỏi submission thành công; F06 chưa chốt giữ draft/nội dung qua lỗi.
- Priority: P1; Gate/source status: **DD BLOCKED; IMPLEMENTATION PARTIAL; RUNTIME NOT VERIFIED:** current callers use source-backed #33/#34/#35 fields; #35 validates enrollment/deadline and accepts one upload ID. #33 lacks access predicates, #34 has no app size/MIME limit and returns a public URL, and #35 has no idempotency/reload reconciliation; API response `data.id` differs from inventory's `submission_id`. Multiple-file/checklist/loaded-screen content, DD states and visual alignment remain incomplete; schemas and live storage are unverified.

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.
- 2026-11-20 — Ghi nhận luồng #33/#34/#35 hiện hành, route/response validation, ambiguity guard và các policy gaps.

## Trạng thái và ranh giới bằng chứng

# ST-18 — Soạn và nộp bài tập

> Các đoạn “hiện trạng/current behavior” bên dưới được giữ từ source DD cũ để truy vết; trạng thái source hiện tại là phần **Current implementation — 2026-11-20** ở trên.

> **Trạng thái nguồn hiện tại:** DD BLOCKED; IMPLEMENTATION PARTIAL; RUNTIME NOT VERIFIED. API #33/#34/#35 và Study Client callers exist; access and idempotency gaps remain.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

### A.1. Định danh

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID / tên | ST-18 — Soạn và nộp bài tập (Page) |
| Mục tiêu | Student chuẩn bị thông tin/file và gửi bài tập cho assignment. |
| Actor | Student theo inventory và AC-17; route hiện là đề xuất. API #34 cũng cho phép Mentor với purpose khác, nhưng ST-18 chỉ mô tả actor Student. |
| Route thiết kế | /student/assignments/:assignmentId/submit; chưa có Study Web router/source. |
| Màn hình liên quan | ST-17 — Chi tiết bài tập; ST-19 — Bài đã nộp và phản hồi. |
| API dự kiến | #33 đọc Assignment/rule; #34 upload từng file nếu cần; #35 tạo submission. #36 thuộc màn hình ST-19 theo inventory. |
| Elements / events | 60 elements ST18-EL-01…ST18-EL-60; 13 events ST18-EV-01…ST18-EV-13. |
| Trạng thái | DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED. |

### A.2. Điều kiện vào, dữ liệu và rời màn hình

- ST-17 có thể chuyển assignmentId qua route path. Inventory ST-18 yêu cầu GET #33, trong khi AC-17 đã GET #33 ở bước đọc đề bài trước đó; source không quy định cache, refetch hoặc owner của request. Đây là DISCREPANCY; DD không tự chọn.
- API #33 catalog: GET /api/v1/assignments/{assignment_id}, Student Bearer, chỉ path assignment_id:int64; response ApiEnvelope<Assignment> với id, course_id, title, description?, due_at?, max_score; status 200/401/403/404/500. Không có Student route/module/test hiện hành; DD Draft — Needs Confirmation.
- AC-17 tiền điều kiện là Student được phép nộp và assignment còn hạn. Nhánh quá hạn/không quyền ghi 403/409; #33 catalog không có 409. Access predicate, boundary/timezone, rule trả qua #33 và #35 enforcement còn mở.
- API #34 catalog/source hiện hành: POST /api/v1/uploads, Bearer, multipart file + purpose + optional course_id; Student dùng purpose=SUBMISSION. Response 201 ApiEnvelope<UploadAsset> gồm id, name, url, content_type, size_bytes, status. API #34 hiện nhận file nào cũng được về bytes/MIME; không có application size cap. Student course_id là optional; chỉ khi có thì route kiểm tra enrollment ACTIVE. Vì vậy text “Tối đa 50MB” và định dạng PDF/DOCX/ZIP/PNG/WEBP trong ảnh là design claim, chưa phải giới hạn server.
- API #34 lưu object lên S3-compatible storage theo key UUID phía server, sau đó insert uploads metadata và commit. URL trả về ghép từ configured public base URL. Lỗi storage trả 503; lỗi DB rollback + best-effort delete object rồi trả 500. Test source tồn tại nhưng không chạy trong phiên này; migration, live DB, credentials, URL reachability và production behavior chưa xác minh.
- API #35 catalog: POST /api/v1/assignments/{assignment_id}/submissions; Student Bearer; body bắt buộc text:string và file refs:string; response 201 ApiEnvelope<Submission>; errors 401/403/404/409/422/500. Catalog không chỉ rõ media type hay wire key của file refs. API DD chỉ là Draft — Needs Confirmation; route/module/test không tồn tại trong source hiện tại.
- API #35 logical response dự thảo có data.id, assignment_id, user_id, content?, files:UploadAsset[], status, submitted_at, score?, feedback?. Inventory gọi ID trả về là submission_id, tạo discrepancy với data.id; assignment_submissions.file_url trong DDL chỉ có một URL và không có association table submission-upload được thấy, khác với logical files[].
- Screenshot hiện tại là loaded form Student. code.html là Guest/unavailable fallback, dùng hash link `#/student/assignments/detail` thay cho route thiết kế có `assignmentId`; không có form, API request hay screen-specific interaction logic. File HTML vẫn có script cấu hình Tailwind và tải Tailwind/Google Fonts từ xa. Tên, URL, số điểm/checklist, timestamps, progress và files trên PNG đều là nội dung sample.
- Study Web hiện có docs/assets và ignored `dist/index.html` chỉ có route `/`; editable source/package/Student route không có. PNG 826px cho thấy layout hai cột dày; HTML dùng max-width 1440px và remote fonts/CDN, khác target Study Web (max-width khoảng 1120px, không remote font, controls tối thiểu 44px và reflow dưới 768px). Đây là design discrepancy; chưa có runtime hành vi ST-18 được xác minh.

### A.3. Expected behavior và current behavior

**Expected behavior:** ST-18 nhận Assignment context, cho Student nhập nội dung/chọn file, gọi #34 cho từng file cần upload, rồi #35 để tạo submission. Upload thành công không đồng nghĩa submission đã thành công. Sau response thành công, luồng chuyển tới ST-19 và GET #36 theo submission ID trong inventory. AC-17 đặt GET #36 sau #35 trước node “Đã nộp”, trong khi inventory gán #36 cho ST-19; owner cần chốt screen/call boundary. F06 không chốt việc giữ nội dung/draft khi lỗi; retention là câu hỏi mở.

**Current behavior:** Chỉ API #34 có route/module/provider hiện hành. API #33, #35 và #36 Student routes/modules/tests không có. Study Web ST-18 route không có. screen.png mô phỏng loaded state; code.html chỉ hiển thị fallback. Không có submission nào được tạo bởi các asset này.

### A.4. API contract, source và giới hạn

| API | Contract/source hiện có | Giới hạn |
|---|---|---|
| #33 GET assignment | Catalog 200/401/403/404/500; Student Bearer; response Assignment có id, course_id, title, description?, due_at?, max_score. | Catalog/DD only; access/deadline/submission-rule/nullability/serialization/path errors open; route/module/test NOT_FOUND. |
| #34 POST upload | Route/module/provider/source tests exist; Student purpose SUBMISSION; optional course_id; 201 UploadAsset; source errors 401/403/422/503/500. | No app size/MIME restrictions; optional course_id skips enrollment check when absent; public-base URL; test/live provider/schema not verified. |
| #35 POST submission | Catalog 201 ApiEnvelope<Submission>; body text and file refs strings; errors 401/403/404/409/422/500. | DD-only; wire key, encoding, access/deadline, insert/update, idempotency and storage mapping open; route/module/test NOT_FOUND. |
| #36 GET receipt | AC-17/catalog successor for submission detail; inventory assigns it to ST-19. | Current Student route/module/test NOT_FOUND; do not call silently from ST-18. |

### A.5. Bảo mật và dữ liệu

- Countdown chỉ là display. Không dùng local time để authorize hoặc deny submission.
- API #34 checks role/purpose; nếu Student gửi course_id thì source checks ACTIVE enrollment. Nếu bỏ field thì source không chạy enrollment query; không tự kết luận omission là an toàn hoặc đúng cho ST-18.
- API #34 trả public-base URL. Quyền xem/download file, signed URL và dữ liệu nhạy cảm của bài nộp cần được xác nhận trước khi bật preview/share.
- Không gửi user ID do client nhập; actor identity đến từ Bearer principal.
- Source DDL/migration và fake-session test không chứng minh live schema, FK, S3 access policy hoặc deployment.
