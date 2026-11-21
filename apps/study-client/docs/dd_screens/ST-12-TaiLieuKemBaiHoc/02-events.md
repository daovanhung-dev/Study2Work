# ST-12 — Events (đặc tả xử lý)

## Current-source reconciliation — 2026-11-20

Current source supersedes the historical “no route/caller” statements in the
snapshot below: ST-12 calls #26 on `lessonId` changes, cancels stale requests,
validates the exact success code, lesson/resource identity, ascending resource
IDs and `url=null`, and renders loading/error/retry/empty/list states. The
resource action hands `resourceId` plus lesson return context to GS-07; GS-07
owns #12 and its PUBLIC/PRIVATE URL access policy. #26 requires ACTIVE
enrollment and a PUBLISHED lesson/course. Catalog response shape, resource
producer/schema, runtime and design fidelity remain unresolved.

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `ST-12-EV-001` | `ST12-EV-01` / ST12-EV-01 — Vào route và tải tài nguyên theo lesson | See source event detail below |
| `ST-12-EV-002` | `ST12-EV-02` / ST12-EV-02 — Chọn resource và đọc metadata qua API #12 | See source event detail below |
| `ST-12-EV-003` | `ST12-EV-03` / ST12-EV-03 — Quay lại trình học bài (ST-11) | See source event detail below |
| `ST-12-EV-004` | `ST12-EV-04` / ST12-EV-04 — Mở diễn đàn để xin tài liệu | See source event detail below |
| `ST-12-EV-005` | `ST12-EV-05` / ST12-EV-05 — Navigation và legal links của shell | See source event detail below |
| `ST-12-EV-006` | `Source heading` / Badge “Tự động làm mới mỗi 30s” không phải event | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả sự kiện

### ST12-EV-01 — Vào route và tải tài nguyên theo lesson

| Trường | Đặc tả |
|---|---|
| Element / loại | Route entry; `Load` theo inventory. Không có marker control riêng; thẻ trạng thái #15 mô tả contract. |
| Điều kiện tiên quyết | Expected: route có `lessonId`, Student session hợp lệ và có quyền xem lesson (AC-15/catalog). Current: route/router/auth client không có trong checkout. |
| Input | `lessonId` từ route; catalog khai báo required `int64`. Bearer Student theo catalog. Không query/body/header tùy biến nào khác được khai báo cho #26. |
| Request kỳ vọng | `GET /api/v1/lessons/{lesson_id}/resources`; #26 được xem là API declared-only, không có current route/module/query/test. |
| Bước xử lý | 1) Route/session kiểm tra thuộc tính đầu vào theo contract sau khi được duyệt. 2) Catalog yêu cầu gọi dưới Student Bearer; token transport/storage hiện không có source. 3) Gửi path `lesson_id`, không tự thêm pagination/filter. 4) Response hiện khai báo `ApiEnvelope<Lesson>`; không thể diễn giải thành `Resource[]` hoặc chọn `Lesson.id` làm `resource_id`. 5) Dừng mapping cho tới khi API owner chốt response/cardinality. 6) Chỉ render empty/list/error theo semantics được chốt, không dựa trên fallback screenshot. |
| Response/status khai báo | 200 `DESIGN_RESOURCE_RETRIEVED`; 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 404 `DESIGN_RESOURCE_NOT_FOUND`; 500 `DESIGN_INTERNAL_ERROR`. Catalog chưa đủ schema để quy định payload/error fields chi tiết. |
| Kết quả/ngoại lệ | #26 hiện `NOT_FOUND`; không có response runtime để map. Empty list, 404-vs-empty, order, retry, timeout, cache và refresh policy đều `OPEN`. Session/access UI không được suy ra từ screenshot. |
| Chống lặp/tác dụng phụ | GET được khai báo read-only; không có client dedupe/cache/retry policy hay server side effect source để xác nhận. Không bật refresh mỗi 30 giây từ badge tĩnh. |

### ST12-EV-02 — Chọn resource và đọc metadata qua API #12

| Trường | Đặc tả |
|---|---|
| Element / loại | Resource selection/`Click` dự kiến; không có resource row/card/control trong ST-12 asset hiện tại. |
| Điều kiện tiên quyết | Chỉ có thể thực hiện sau khi API #26 trả Resource item theo contract đã duyệt, có `resource_id`, và owner xác định #12 có còn cần gọi hay không. Access/URL policy phải được phê duyệt trước khi expose hoặc mở URL. |
| Input | `resource_id` from a validated #26 row. #12 accepts a signed-int64 path; PUBLIC is unauthenticated, PRIVATE requires Student Bearer. |
| Request hiện có | `GET /api/v1/resources/{resource_id}`. Route đăng ký trong `apps/study-server/app/api/v1.py`, gọi `get_resource_detail`, sau đó `validate_resource_id` → `find_resource` (Q1) → nếu `lesson_id != null`, `find_published_parent_course` (Q2). |
| Current success mapping | 200 `DESIGN_RESOURCE_RETRIEVED`; `data` includes `id/name/type/url/visibility/lesson_id`. PUBLIC URL is direct HTTP(S); PRIVATE URL is signed for 300 seconds. |
| Current access/publish behavior | PUBLIC needs no token. PRIVATE requires Student auth, a non-deleted lesson, published parent course and ACTIVE enrollment; private resources without a valid parent are hidden as 404. |
| Status/lỗi source | Invalid/missing/unpublished resource → 404; unauthenticated/invalid Student → 401; no ACTIVE enrollment → 403; query/mapping error → 500; signer unavailable → 503. |
| Bước tiếp theo | ST-12 does not call #12 directly; it hands off ID/context to GS-07. GS-07 validates the response and opens an allowed URL only after a user action. MIME-specific preview and expiry recovery are not implemented. |
| Kết quả/ngoại lệ | API #12 source-backed nhưng API DD `Draft — Needs Confirmation`; source tests được đọc, không chạy. Không có UI control để kích hoạt trong screenshot và không có e2e evidence. |

### ST12-EV-03 — Quay lại trình học bài (ST-11)

| Trường | Đặc tả |
|---|---|
| Element / loại | #11, click anchor. |
| Input | `lessonId` hiện tại nếu route đã được triển khai; trạng thái video/playback position nếu muốn khôi phục cần contract riêng. |
| Hiện trạng | HTML có `data-path="student-lessons-lessonId"` và `href="#"`; không có router handler. Native target hiện không truyền `lessonId`. |
| Luồng kỳ vọng | Sau khi route/lesson context được xác nhận, điều hướng về `/student/lessons/:lessonId`; chỉ giữ playback position/history nếu có nguồn state đã duyệt. Không gọi API bởi click quay lại. |
| Ngoại lệ | Thiếu/invalid `lessonId`, hết session, hoặc lesson access bị thu hồi cần recovery policy; hiện chưa có UI/runtime mapping. |

### ST12-EV-04 — Mở diễn đàn để xin tài liệu

| Trường | Đặc tả |
|---|---|
| Element / loại | #24, click anchor sau copy hỗ trợ ở #23. |
| Input | HTML chỉ có `data-path="thao-luan"`; không có `courseId`, discussion ID hoặc destination URL. |
| Hiện trạng | `href="#"`; không có API call/router. |
| Kết quả kỳ vọng | Product cần xác định room/route nào tiếp nhận yêu cầu và dữ liệu context nào được truyền. Không tự map sang ST-23 vì inventory/route đó cần course context chưa có ở asset này. |

### ST12-EV-05 — Navigation và legal links của shell

| Trường | Đặc tả |
|---|---|
| Element / loại | #1, #3, #27; click anchors. |
| Input | Các `data-path` metadata: `trang-chu`, `khoa-hoc-cua-toi`, `tien-do`, `thao-luan`, `thong-bao`, `dieu-khoan-dich-vu`, `chinh-sach-bao-mat`, `tro-giup`; không có route table trong HTML. |
| Hiện trạng/kết quả | Tất cả `href="#"`, không có router script. Không xác định route, auth gating hay data handoff từ mockup. Cần app shell/route contract trước khi triển khai. |

### Badge “Tự động làm mới mỗi 30s” không phải event

HTML không chứa polling/timer hoặc request handler. Không tạo `setInterval`, retry hay refresh API dựa trên text này. Nếu product thật sự yêu cầu polling, cần xác định endpoint, visibility state, overlap/cancel, timeout, backoff, focus/tab behavior và chi phí trước khi cập nhật thiết kế.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
