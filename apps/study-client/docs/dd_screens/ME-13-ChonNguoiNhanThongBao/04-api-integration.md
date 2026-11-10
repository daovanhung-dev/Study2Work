# ME-13 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `ME-13-API-001` | #46 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `ME-13-API-002` | #62 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #46, #62
- Orchestration/data notes: GET #46 → GET #62 theo numeric course_id → giữ unique Student IDs int64 cho ME-14; handoff carrier chưa được duyệt.
- BE/source status và gate: **R**; #46/#62 route/module/query/model/test source-backed locally. **BLOCK:** prototype slugs không ánh xạ int64; #46 không có semester/assigned-course; course status eligibility; support_needed thiếu progress/attendance source; loaded roster/selection UI chưa có; #63 CSV recipient mapping vẫn Draft/DERIVED, không có course_id, content:int64 lệch text, privacy/email/WCAG claims chưa được xác nhận; live schema và Study Web UNWIRED
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: API dependency trace

**API #46 — GET /api/v1/mentor/courses**

- Route tại [v1.py](../../../../study-server/app/api/v1.py#L777); view/query/validator tại [api_46_mentor_courses](../../../../study-server/app/modules/mentor/api_46_mentor_courses).
- Authorization: Bearer token, role MENTOR, lấy numeric mentor identity trước query. Owner predicate là c.id thuộc mentor_id xác thực.
- Query: status tùy chọn, chỉ DRAFT/PUBLISHED; page mặc định từ shared DEFAULT_PAGE, phải ≥1; size từ DEFAULT_SIZE, 1..100.
- Order: created_at DESC, id ASC. Response success envelope DESIGN_RESOURCE_RETRIEVED, data CoursePage gồm items và pagination {page,size,total,total_pages}; không có course thì 200 với items rỗng. Chỉ map fields có trong Course model; ME-13 cần tối thiểu id và title.
- Lỗi: 401 DESIGN_AUTHENTICATION_REQUIRED, 403 DESIGN_ACCESS_DENIED, 422 DESIGN_VALIDATION_ERROR cho query sai, 500 DESIGN_INTERNAL_ERROR khi query/mapping thất bại. Không có semester filter hay assignment relation.
- Local API test: [test_mentor_courses.py](../../../../study-server/tests/modules/mentor/api_46_mentor_courses/test_mentor_courses.py). Test source có sẵn nhưng không chạy trong phiên DD này; fake DB không chứng minh live schema.

**API #62 — GET /api/v1/mentor/courses/{course_id}/students**

- Route tại [v1.py](../../../../study-server/app/api/v1.py#L1268); view/query/model tại [api_62_mentor_course_students](../../../../study-server/app/modules/mentor/api_62_mentor_course_students).
- Authorization: Bearer token, role MENTOR. course_id là path int64; source parse ID sau auth. Sai format/range hoặc không tồn tại trả 404 DESIGN_RESOURCE_NOT_FOUND; course không thuộc Mentor trực tiếp trả 403 DESIGN_ACCESS_DENIED.
- Query joins course/enrollment/user, filters e.status=ACTIVE and u.role=STUDENT, selects distinct Student and orders u.id ASC. Không lọc account status và không kiểm tra course status.
- Success: HTTP 200, DESIGN_RESOURCE_RETRIEVED, data array [{id:int64,full_name:string,avatar_url?:string}], meta {}. Empty roster là 200 với data:[].
- Lỗi khác: 401 DESIGN_AUTHENTICATION_REQUIRED; 500 DESIGN_INTERNAL_ERROR khi DB/projection lỗi. Không pagination, email, course display label, progress, checkpoint, due date hoặc attendance.
- Local API test: [test_mentor_course_students.py](../../../../study-server/tests/modules/mentor/api_62_mentor_course_students/test_mentor_course_students.py). Không chạy trong phiên này.

**API #63 — POST /api/v1/mentor/notifications (downstream ME-14, not called by ME-13)**

- Route/view/model/validator/query tại [api_63_mentor_notifications_create](../../../../study-server/app/modules/mentor/api_63_mentor_notifications_create); API DD [03_Request.md](../../../../study-server/docs/dd/63_mentor_notifications_create/03_Request.md) còn Draft — Needs Confirmation; [OPEN_QUESTIONS.md](../../../../study-server/docs/dd/63_mentor_notifications_create/OPEN_QUESTIONS.md) ghi recipient mapping còn mở.
- Request hiện tại là JSON strict, extra fields bị từ chối: recipients:string (CSV positive int64 Student IDs), title:string tối đa 200, content:signed int64, channels:string (CSV PUSH/EMAIL). Mọi field required. recipients/channel CSV parse trim tokens và collapse duplicate theo lần đầu; blank/malformed/empty list là 422 DESIGN_VALIDATION_ERROR. Screenshot free-form content chưa tương thích content:int64.
- Server xác thực Mentor, rồi xác minh toàn bộ recipients là Student có enrollment ACTIVE trong ít nhất một common course do Mentor trực tiếp sở hữu. Không có course_id, scope enum, anonymity flag hay email preference field. Recipient mismatch trả 403 DESIGN_ACCESS_DENIED.
- Khi hợp lệ, source tạo một legacy notification row mỗi recipient và một QUEUED delivery-outbox row mỗi channel trong transaction; chỉ sau commit mới trả 202 DESIGN_OPERATION_ACCEPTED. data là Operation {id:UUID,kind:NOTIFICATION_DISPATCH,status:QUEUED,owner_id:int64,submitted_at,updated_at}; meta.notification_ids:int64[] giữ ID thông báo riêng. 202 không chứng minh worker/provider đã gửi.
- Các lỗi còn lại: 401 DESIGN_AUTHENTICATION_REQUIRED, 422 DESIGN_VALIDATION_ERROR, 503 DESIGN_DEPENDENCY_UNAVAILABLE cho DB unavailable, 500 DESIGN_INTERNAL_ERROR. Không có idempotency key; retry sau timeout có thể tạo batch trùng. Không dùng operation UUID thay notification_id; API #18 và #64 là handoff sau, thuộc ME-15.
- API #63 local tests nằm tại [test_mentor_notifications_create.py](../../../../study-server/tests/modules/mentor/api_63_mentor_notifications_create/test_mentor_notifications_create.py). DD này không chạy tests; local tests/fallback schema không xác minh live DB/deployment/worker.

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/04_mentor/ME-13_chon-nguoi-nhan-thong-bao/ME-13.md)
