# ME-04 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `ME-04-EV-001` | `ME04-EV-01` / ME04-EV-01 — Mở route và xác minh course | See source event detail below |
| `ME-04-EV-002` | `ME04-EV-02` / ME04-EV-02 — Chọn module và vị trí bài | See source event detail below |
| `ME-04-EV-003` | `ME04-EV-03` / ME04-EV-03 — Nhập metadata lecture | See source event detail below |
| `ME-04-EV-004` | `ME04-EV-04` / ME04-EV-04 — Chọn/kéo thả và tải file qua #34 | See source event detail below |
| `ME-04-EV-005` | `ME04-EV-05` / ME04-EV-05 — Hiển thị kết quả upload/progress | See source event detail below |
| `ME-04-EV-006` | `ME04-EV-06` / ME04-EV-06 — Thay thế hoặc tải lại media | See source event detail below |
| `ME-04-EV-007` | `ME04-EV-07` / ME04-EV-07 — Gỡ file khỏi form | See source event detail below |
| `ME-04-EV-008` | `ME04-EV-08` / ME04-EV-08 — Nhập URL stream | See source event detail below |
| `ME-04-EV-009` | `ME04-EV-09` / ME04-EV-09 — Chọn editor mode, toolbar và sửa nội dung | See source event detail below |
| `ME-04-EV-010` | `ME04-EV-10` / ME04-EV-10 — Thêm attachment | See source event detail below |
| `ME-04-EV-011` | `ME04-EV-11` / ME04-EV-11 — Xem trước lecture chưa lưu | See source event detail below |
| `ME-04-EV-012` | `ME04-EV-12` / ME04-EV-12 — Chọn loại Video/Paper/Lab | See source event detail below |
| `ME-04-EV-013` | `ME04-EV-13` / ME04-EV-13 — Guest Preview | See source event detail below |
| `ME-04-EV-014` | `ME04-EV-14` / ME04-EV-14 — Prerequisite | See source event detail below |
| `ME-04-EV-015` | `ME04-EV-15` / ME04-EV-15 — Chọn Draft hoặc Publish | See source event detail below |
| `ME-04-EV-016` | `ME04-EV-16` / ME04-EV-16 — Lưu bản nháp | See source event detail below |
| `ME-04-EV-017` | `ME04-EV-17` / ME04-EV-17 — Tạo bài giảng | See source event detail below |
| `ME-04-EV-018` | `ME04-EV-18` / ME04-EV-18 — Điều hướng sang ME-05 | See source event detail below |
| `ME-04-EV-019` | `ME04-EV-19` / ME04-EV-19 — Validation, API/network errors and repeated submit | See source event detail below |
| `ME-04-EV-020` | `ME04-EV-20` / ME04-EV-20 — Hủy và quay về ME-03 | See source event detail below |
| `ME-04-EV-021` | `ME04-EV-21` / ME04-EV-21 — Global nav, search, notification và footer | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: 4. Đặc tả sự kiện

Mọi event mô tả trạng thái mục tiêu dựa trên inventory/backend source; không event nào bên dưới khẳng định current Study Web đã hoạt động.

### ME04-EV-01 — Mở route và xác minh course

- **Kích hoạt:** page enter, reload hoặc deep link; element #06/#07/#08.
- **Input:** URL `courseId`, Mentor Bearer session; current #46 query/page contract.
- **Xử lý:** (1) Parse route ID thành signed int64 theo yêu cầu #34/#47. (2) Không xem course code string trong mockup là ID. (3) Gọi #46 với page/size trong contract để xác minh một `Course.id` thuộc owner hiện tại. (4) Chỉ bind `Course.title/status` từ response; module/order chưa có nguồn. (5) Nếu target page chưa chứa ID, không tự đoán; cần quyết định pagination/deep-link policy.
- **Kết quả/lỗi:** route context loading → ready only after matching row. #46 401 session/auth; 403 access; 422 query; 500 server. Missing/assigned course mapping chưa có status đủ chính xác.
- **Blocker:** AC-21 assigned-course và current direct-owner #46 chưa khớp; #46 không có detail path.

### ME04-EV-02 — Chọn module và vị trí bài

- **Kích hoạt:** change select #14/#16.
- **Input:** lựa chọn module/order từ nguồn server chưa xác định; route course ID.
- **Xử lý:** Không dùng các option `Chương 02`, `Bài số 16/48` như dữ liệu thật. Chỉ lưu value khi có API/schema hợp lệ; giữ `order` int32 và không áp rule không âm/unique/next-order khi chưa duyệt.
- **Kết quả/lỗi:** hiện là static mockup control; chưa có source để populate hoặc validate module/order.
- **Blocker:** module hierarchy và order allocation.

### ME04-EV-03 — Nhập metadata lecture

- **Kích hoạt:** input/change #17/#19/#37.
- **Input:** title text, duration text, editor content; các giá trị hiện tại trên ảnh là mẫu.
- **Xử lý:** giữ local form state. Chỉ title có API field: #47 yêu cầu string, tối đa 200; source không xác định min length hoặc trim. Duration không có field. Editor #47 chỉ nhận signed int64, nên không chuyển text thành số, không ép `Number`, không lưu content giả để vượt validation.
- **Kết quả/lỗi:** UI validation/error rule cho title, duration và content cần quyết định; #47 type/range lỗi trả 422 `DESIGN_VALIDATION_ERROR`.
- **Blocker:** rich-text mapping và metadata fields.

### ME04-EV-04 — Chọn/kéo thả và tải file qua #34

- **Kích hoạt:** chọn file/kéo thả trên #30 hoặc #39; HTML hiện không có file input/drop event.
- **Input:** file binary; `purpose=LECTURE`; `course_id` lấy từ route dưới dạng int64; Authorization Bearer.
- **Request:** `POST /api/v1/uploads`, `multipart/form-data`; parts `file`, `purpose`, `course_id`. Để multipart encoder tạo boundary. Upload từng file độc lập; không tự đặt giới hạn MIME/2 GB từ copy mockup vì source #34 chưa có policy tương ứng.
- **Xử lý server:** MENTOR auth → purpose-role/course validation → direct-owner check → measure byte size → S3-compatible object upload → insert/commit UploadAsset metadata.
- **Response:** 201 `DESIGN_RESOURCE_CREATED`, data `{id,name,url,content_type,size_bytes,status}`. UI phải giữ `id` để gửi #47; không gửi URL thay ID.
- **Lỗi:** 401 auth; 403 purpose/owner; 422 multipart/purpose/course; 503 storage; 500 DB. Metadata failure rollback DB và best-effort delete object. Live S3/provider chưa verify.

### ME04-EV-05 — Hiển thị kết quả upload/progress

- **Kích hoạt:** response #34 success hoặc upload transport progress.
- **Input:** `UploadAsset` response; client-level byte progress nếu implementation chọn hỗ trợ.
- **Xử lý:** thêm asset ID vào danh sách local theo thứ tự; map name/size/type/status từ response. Chỉ hiển thị “hoàn tất” khi #34 trả 201. API response không trả transcoding, duration, thumbnail hay HLS processing state.
- **Kết quả:** uploaded asset ready-for-link local; screen không được nói “transcoded/ready to stream” từ `UPLOADED`.
- **Blocker:** progress/live processing contract và UI retry/partial batch policy.

### ME04-EV-06 — Thay thế hoặc tải lại media

- **Kích hoạt:** #28 hoặc retry sau upload error.
- **Input:** binary mới, current course ID, current Mentor.
- **Xử lý:** API hiện tại chỉ hỗ trợ thêm upload #34. Nó không thay thế file cũ và không có idempotency key. Retry sau ambiguous network có thể tạo asset thứ hai; không blind-retry trước khi có reconciliation rule.
- **Kết quả:** nếu upload mới thành công, có UploadAsset ID mới. Asset cũ vẫn tồn tại đến khi có cleanup contract.

### ME04-EV-07 — Gỡ file khỏi form

- **Kích hoạt:** #29/#41/#43.
- **Input:** UploadAsset ID đã upload hoặc file chưa upload.
- **Xử lý:** chưa upload thì có thể bỏ local selection; đã upload thì UI chỉ có thể bỏ ID khỏi local `asset_refs` draft. Không gọi API xóa vì route không tồn tại.
- **Kết quả/lỗi:** uploaded object/row vẫn tồn tại và có thể không link lecture nếu người dùng bỏ. Thời hạn dọn file/owner policy chưa được quy định.

### ME04-EV-08 — Nhập URL stream

- **Kích hoạt:** input #32.
- **Input:** URL Vimeo/HLS sample.
- **Xử lý:** không có field `video_url` trong #47 và #34 nhận binary, không nhận URL. Không gửi URL trong body ngoài schema strict (extra fields 422), không tự tạo UploadAsset từ URL.
- **Kết quả:** field chưa thể persist; cần quyết định product/API/allowlist/security trước khi bật.

### ME04-EV-09 — Chọn editor mode, toolbar và sửa nội dung

- **Kích hoạt:** #34/#35/#36/#37.
- **Input:** Markdown/WYSIWYG text, snippets, formatting commands.
- **Xử lý:** mockup không có editor state/textarea/contenteditable hay toolbar listeners. Nếu editor được duyệt, cần canonical serialization/content schema. Không biến rich text thành `content:int64` bằng giả định; current #47 sẽ lưu số đó dưới dạng decimal string.
- **Kết quả/lỗi:** nội dung chưa có payload mapping, error state hoặc autosave API.

### ME04-EV-10 — Thêm attachment

- **Kích hoạt:** #39 hoặc drop file vào #30.
- **Input:** binary + course ID.
- **Xử lý:** upload #34 với `purpose=LECTURE`, lấy `id`, giữ `id` trong thứ tự người dùng. Khi tạo lecture gửi `asset_refs` là JSON string, ví dụ `"[34001,34002]"`; mỗi ID duy nhất. #47 trả `assets` theo đúng order input.
- **Ngoại lệ:** `"[]"` hợp lệ. Một ID thiếu hoặc sai owner/purpose/course khiến #47 trả generic 404; toàn bộ create thất bại, uploads trước đó vẫn tồn tại.

### ME04-EV-11 — Xem trước lecture chưa lưu

- **Kích hoạt:** #12 hoặc #27.
- **Input:** current local editor/media state.
- **Xử lý:** chưa có preview endpoint, route, modal hoặc serialization contract được xác nhận. Không điều hướng sang ME-05 vì ME-05 đọc lecture đã lưu.
- **Kết quả:** feature ở trạng thái blocked; không đánh dấu là implemented.

### ME04-EV-12 — Chọn loại Video/Paper/Lab

- **Kích hoạt:** radio #45/#46/#47.
- **Input:** enum mẫu.
- **Xử lý:** #47 không nhận `type`; không map loại thành `content` hoặc file extension. Chờ enum và persistence contract.
- **Kết quả:** hiện là static options, chưa persist.

### ME04-EV-13 — Guest Preview

- **Kích hoạt:** toggle #48.
- **Input:** boolean mẫu.
- **Xử lý:** không có preview/access field hoặc policy trong #47; không suy luận from PUBLISHED status.
- **Kết quả:** chưa thể áp dụng; cần course/lesson visibility decision.

### ME04-EV-14 — Prerequisite

- **Kích hoạt:** toggle #49.
- **Input:** boolean và sample “hoàn tất bài số 15”.
- **Xử lý:** không có prerequisite ID, dependency API, cycle validation hoặc server rule; không lưu như `order`.
- **Kết quả:** chưa persist; cần model/API và validation policy.

### ME04-EV-15 — Chọn Draft hoặc Publish

- **Kích hoạt:** #50/#51.
- **Input:** lifecycle choice.
- **Xử lý:** current #47 ignores no such field and always inserts `PUBLISHED`. UI choice cannot select lifecycle. “Gửi duyệt” also does not match current immediate status.
- **Kết quả:** do not submit until product/API state machine is settled; no silent publish from a Draft click.

### ME04-EV-16 — Lưu bản nháp

- **Kích hoạt:** #57.
- **Input:** current form state and possibly uploaded IDs.
- **Xử lý:** no draft-create endpoint/body or local draft storage contract is present. Do not call #47 because it publishes. Autosave text #11 does not evidence persistence.
- **Kết quả:** unsupported; button must be disabled/removed in implementation until contract approved.

### ME04-EV-17 — Tạo bài giảng

- **Kích hoạt:** #56.
- **Điều kiện:** valid route/course authorization; approved body schema/content mapping; all intended uploads succeeded; no prior request pending.
- **Request source:** `POST /api/v1/mentor/courses/{course_id}/lectures`, Bearer MENTOR, `application/json`, strict body `title`, `content:int64`, `asset_refs:string`, `order:int32`.
- **Xử lý:** #47 validates path/body/asset refs → checks direct owner → resolves all assets under same Mentor/LECTURE/course → inserts `lessons` as PUBLISHED and ordered `lesson_uploads` links in one transaction → commits.
- **Success:** 201 `DESIGN_RESOURCE_CREATED`, map `data.id`, course/title/content string/assets/order/status; hand off `lectureId` to ME-05. Success response is source behavior, not proof browser route is wired.
- **Errors:** 401 expired/missing auth; 403 owner mismatch; 404 course/assets not found (asset error is intentionally generic); 422 body/path validation; 500 safe internal error. #47 DB rollback does not roll back successful #34 uploads.
- **Retry/idempotency:** no idempotency key/source duplicate prevention identified; if network outcome is ambiguous, blind resubmit may create another lesson. Required duplicate-submit resolution is a blocker.

### ME04-EV-18 — Điều hướng sang ME-05

- **Kích hoạt:** #47 201 with `data.id`.
- **Input:** `lectureId`, course context if ME-05 needs a return link.
- **Xử lý:** proposed route `/mentor/lectures/:lectureId`; ME-05 requests #48 and renders its response. Use returned persisted values rather than local mock values.
- **Lỗi:** #48 401/403/404/500 handled by ME-05 states. Navigation/return-state remains proposed because Study Web router is absent.

### ME04-EV-19 — Validation, API/network errors and repeated submit

- **Kích hoạt:** #34/#47 validation response, transport error, or repeated click.
- **Xử lý:** before request, prevent only duplicate concurrent click in client; this is not a server idempotency guarantee. For #34 show per-file failure for 401/403/422/503/500. For #47 retain local form on failure; render supplied `errors[]` against fields when present and a safe summary for 401/403/404/500. Do not expose DB/S3 internals. #34 success already committed remains an unlinked asset after #47 failure.
- **Network ambiguity:** no API operation-status lookup or idempotency key is found for #34/#47. Do not claim safe automatic retry; need a retry/reconciliation decision.

### ME04-EV-20 — Hủy và quay về ME-03

- **Kích hoạt:** #58 or breadcrumb #06.
- **Input:** `courseId`, current local dirty state, uploaded asset IDs.
- **Xử lý:** target ME-03 with the same course context. Unsaved prompt, browser back policy, persistence of draft and cleanup of already-uploaded files have no approved behavior. Do not imply Cancel reverses API #34.
- **Kết quả:** navigation remains proposed; any committed uploads remain until separate cleanup policy exists.

### ME04-EV-21 — Global nav, search, notification và footer

- **Kích hoạt:** #01–#05/#60.
- **Current HTML:** header anchors use `href="#"`; search has no submit/API; notification badge is static; footer items are spans.
- **Expected:** route only to the inventory-defined screen that owns each action, carrying IDs only where its contract specifies. ME-04 does not define header search or notification behavior. No navigation event is considered runtime-wired.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
