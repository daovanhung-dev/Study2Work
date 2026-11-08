# ST-10 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `ST-10-EV-001` | `ST10-EV-01` / ST10-EV-01 — Mở route và nhận lesson context | See source event detail below |
| `ST-10-EV-002` | `ST10-EV-02` / ST10-EV-02 — Xác minh Student session | See source event detail below |
| `ST-10-EV-003` | `ST10-EV-03` / ST10-EV-03 — Gọi API #22 kiểm tra access | See source event detail below |
| `ST-10-EV-004` | `ST10-EV-04` / ST10-EV-04 — Chặn luồng khi access bị từ chối/lỗi | See source event detail below |
| `ST-10-EV-005` | `ST10-EV-05` / ST10-EV-05 — Gọi API #23 ghi nhận bắt đầu lesson | See source event detail below |
| `ST-10-EV-006` | `ST10-EV-06` / ST10-EV-06 — Gọi API #24 lấy lesson content | See source event detail below |
| `ST-10-EV-007` | `ST10-EV-07` / ST10-EV-07 — Mở ST-11 sau content success | See source event detail below |
| `ST-10-EV-008` | `ST10-EV-08` / ST10-EV-08 — Quay lại ST-09 | See source event detail below |
| `ST-10-EV-009` | `ST10-EV-09` / ST10-EV-09 — Header, brand và breadcrumb navigation | See source event detail below |
| `ST-10-EV-010` | `ST10-EV-10` / ST10-EV-10 — Footer terms/privacy/help navigation | See source event detail below |
| `ST-10-EV-011` | `Source heading` / API, authorization và bảo mật | See source event detail below |
| `ST-10-EV-012` | `Source heading` / Security rules for this screen | See source event detail below |
| `ST-10-EV-013` | `Source heading` / Required decisions | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả chi tiết từng sự kiện

> Các bước expected dưới đây chỉ trở thành implementation contract sau khi các API Draft và state/error decisions được duyệt. Không tự thêm retry, timeout, redirect, token, cache hoặc permission field.

### ST10-EV-01 — Mở route và nhận lesson context

| Trường | Đặc tả |
|---|---|
| Trigger / loại | Route entry / Load. |
| Element | Page-level; route inventory /student/lessons/:lessonId/start. |
| Input | lessonId từ route, expected int64 theo path parameter #22–#24; Student context từ auth/session. Upstream source dự kiến ST-09, nhưng asset ST-09 hiện không truyền lessonId. |
| Điều kiện | Route/runtime phải được nối và input phải có nguồn. Inventory không quy định positivity/range/parse-error behavior. |
| Quy trình | 1) Nhận path. 2) Parse lessonId theo kiểu contract; không tự đặt range hoặc fallback ID. 3) Kiểm tra có Student auth context theo product/auth contract. 4) Nếu thiếu lessonId hoặc session, không tạo fake ID hay call content endpoint. 5) Chỉ sau khi request context hợp lệ mới vào expected access check. |
| Kết quả/ngoại lệ | Current route không tồn tại trong editable client source; không có loading/error mapping. Missing/invalid path behavior cần API/client owner chốt. |

### ST10-EV-02 — Xác minh Student session

| Trường | Đặc tả |
|---|---|
| Trigger / loại | Page entry trước API calls; Auth guard / Load. |
| Element | Page-level; không có login control trong asset. |
| Input | Bearer JWT theo API catalog #22–#24; role Student. JWT claim mapping đến enrollment/user cần được xác nhận trong API DD. |
| Quy trình | 1) Đọc auth context từ implementation được duyệt. 2) Không lấy text “Học viên” tại #3 làm bằng chứng role. 3) Chỉ gửi Bearer header theo API contract nếu có session hợp lệ. 4) Endpoint phải tự kiểm tra access cho mỗi request; client gate không phải security boundary. |
| Kết quả/ngoại lệ | Catalog khai báo 401 DESIGN_AUTHENTICATION_REQUIRED và 403 DESIGN_ACCESS_DENIED cho cả ba API. Client redirect, refresh, session expiry UI và token transport chưa có Study Web source/contract; không tự đặt. |

### ST10-EV-03 — Gọi API #22 kiểm tra access

| Trường | Đặc tả |
|---|---|
| Trigger / loại | Sau khi route input và Student context hợp lệ; Load/API. |
| Element | Page-level; #8/#15 chỉ minh họa checking. |
| Request | GET /api/v1/lessons/{lesson_id}/access; path lesson_id:int64!; Bearer JWT/Student; không query/body theo catalog. |
| Declared response | ApiEnvelope<Lesson>. Catalog codes: 200 DESIGN_RESOURCE_RETRIEVED; 401 DESIGN_AUTHENTICATION_REQUIRED; 403 DESIGN_ACCESS_DENIED; 404 DESIGN_RESOURCE_NOT_FOUND; 500 DESIGN_INTERNAL_ERROR. |
| Expected sequence | 1) Gửi request với lesson_id đã chọn. 2) API theo AC-14 kiểm tra enrollment/prerequisite. 3) Diagram dùng nhánh allow/deny; catalog chỉ khai báo 200 success và 403 denied, không có `allowed` field trong `Lesson`. 4) Không suy ra allow từ lesson.status hoặc public #09. 5) 403 reason cần payload contract được duyệt; không đọc reason từ message tự do theo giả định. |
| Open contract | Enrollment status đủ quyền, JWT claim/user binding, prerequisite source/order, 404 resource semantics, query/projection, 403 reason field/type/value chưa chốt. Body Lesson không có explicit access boolean; response schema/example chưa xác nhận. |
| Current result/error | #22 Draft, không có Study Server route/module/query/test. Network/timeout/retry/cache/cancellation policy chưa xác định. API catalog không khai 423; text 423_LOCKED trong #8 không phải response mapping. |

### ST10-EV-04 — Chặn luồng khi access bị từ chối/lỗi

| Trường | Đặc tả |
|---|---|
| Trigger / loại | #22 trả 403 hoặc nhánh lỗi access; API result/state transition. |
| Element | Expected state liên quan #9/#10/#16; hiện chỉ là static content. |
| Input | HTTP/business result #22 và reason nếu sau này được schema hóa. |
| Quy trình | 1) Khi contract xác nhận denied, dừng chuỗi. 2) Không gọi #23, không gọi #24 và không tải/phát media. 3) Chỉ hiển thị reason sau khi field/message contract được duyệt. 4) Không biến 401, 404, 500 hoặc network error thành “not enrolled” nếu chưa có mapping. 5) Không tự retry hoặc điều hướng. |
| Output | AC-14 yêu cầu denied không mở lesson; inventory state gồm denied/failure. Bố cục lỗi, CTA quay lại và error mapping chưa được thiết kế. Current mockup chỉ có card denied tĩnh. |

### ST10-EV-05 — Gọi API #23 ghi nhận bắt đầu lesson

| Trường | Đặc tả |
|---|---|
| Trigger / loại | Sau #22 allowed theo sequence inventory; chưa rõ #23 tự chạy hay đợi người học bấm #13 sau khi được enable. Current #13 disabled nên không có native click. |
| Trigger contract | Inventory chỉ ghi #23 sau nhánh allowed; không quy định auto-start hay user-submit. Không chọn một cách triển khai khi chưa có product decision. |
| Request | POST /api/v1/lessons/{lesson_id}/start; path lesson_id:int64!; Bearer JWT/Student; catalog không khai query hoặc body. |
| Declared response/status | ApiEnvelope<Lesson>; 201 DESIGN_RESOURCE_CREATED; 401 DESIGN_AUTHENTICATION_REQUIRED; 403 DESIGN_ACCESS_DENIED; 404 DESIGN_RESOURCE_NOT_FOUND; 422 DESIGN_VALIDATION_ERROR; 500 DESIGN_INTERNAL_ERROR. Catalog không khai 409/idempotency key. |
| Expected side effect | AC-14 diagram nói UPSERT lesson progress = IN_PROGRESS. Inventory nói chống submit lặp. DDL BIGINT `lesson_progress` có status/progress_percent/last_accessed_at/completed_at nhưng không có UNIQUE(user_id,lesson_id); V1-PILOT có UUID `lesson_progress_facts` với UNIQUE(enrollment_id,lesson_id), nhưng khác identity/fields. Cả hai là schema artifacts, không phải API #23 mapping/live schema. |
| Quy trình | 1) Chỉ chạy sau access allowed theo flow đã duyệt. 2) Gửi lesson_id và Bearer token; không thêm request body. 3) Chờ response theo catalog. 4) Không coi mọi POST retry là an toàn: repeated-start/new-row vs existing-row behavior, key, timestamp/progress preservation và 201 semantics còn mở. 5) Chỉ GET #24 sau start success theo sequence inventory. |
| Output/ngoại lệ | #23 Draft; transaction, rollback, direct-call entitlement, response projection Lesson và 404/422 conditions chưa chốt. Không retry mù khi network ambiguity; chưa có idempotency contract. |

### ST10-EV-06 — Gọi API #24 lấy lesson content

| Trường | Đặc tả |
|---|---|
| Trigger / loại | Sau khi sequence #22/#23 được duyệt và #23 success; Load/API. |
| Request | GET /api/v1/lessons/{lesson_id}; path lesson_id:int64!; Bearer JWT/Student; không query/body theo catalog. |
| Declared response/status | ApiEnvelope<Lesson>; 200 DESIGN_RESOURCE_RETRIEVED; 401 DESIGN_AUTHENTICATION_REQUIRED; 403 DESIGN_ACCESS_DENIED; 404 DESIGN_RESOURCE_NOT_FOUND; 500 DESIGN_INTERNAL_ERROR. |
| Lesson schema | id:int64, course_id:int64, title:string, content?:string, video_url?:uri, order:int32, status:LessonStatus theo reusable/catalog schema. #24 nullable/omit serialization và enum values chưa xác nhận. |
| Quy trình | 1) Không prefetch content/video trước access. 2) Gửi path/token. 3) Backend phải có contract authorization/publish check áp dụng cho lời gọi trực tiếp; việc client đã gọi #22 không đủ bảo vệ endpoint. 4) Chỉ map Lesson/media field khi #24 success và policy/projection được duyệt. 5) 403/404 không tự phân biệt denied, unpublished hay missing cho đến khi mapping chốt. |
| Security/open | AC-15 nói check access + publish; chưa rõ lesson, parent course hay cả hai; enrollment/prerequisite/JWT identity, query, projection, 403/404, schema baseline/course_id nullability và video_url behavior còn mở. Public #09 hiện trả content/video_url không auth/enrollment context; không dùng thay #24, đồng thời cần Product/Security xác nhận mức độ truy cập nội dung public curriculum. |
| Current result | #24 Draft, không có route/module/query/test. Error payload/null rules, retry/cache/timeout chưa source-backed. |

### ST10-EV-07 — Mở ST-11 sau content success

| Trường | Đặc tả |
|---|---|
| Trigger / loại | Expected navigation sau #24 success; no current handler. |
| Element | #13 Start button disabled hiện tại; FSM #17 chỉ là copy. |
| Input | lessonId đã qua approved access/start/content sequence; exact state handoff/cache policy chưa được duyệt. |
| Quy trình | 1) Chỉ navigate khi #24 response success. 2) Dùng ST-11 route /student/lessons/:lessonId theo inventory nếu route owner xác nhận. 3) Không lấy button click riêng lẻ làm authorization evidence. 4) Không phát media từ #23 response/session-token copy nếu contract không cấp field/token. |
| Kết quả | Expected ST-11. Không có Study Web router hoặc ST-11 integration để xác minh. Inventory ST-11 cũng liệt kê GET #24 khi mở player; cần xác nhận một hay hai lần fetch để tránh duplicate request. |

### ST10-EV-08 — Quay lại ST-09

| Trường | Đặc tả |
|---|---|
| Trigger / loại | Click #12; navigation. |
| Input | Anchor href=#, data-path=tong-quan-khoa-hoc; không có courseId/lesson selection state. |
| Current processing | Static anchor only; không API call/router handler. |
| Expected result | ST-09. Return context, history, selected lesson/course restoration và auth guard chưa chốt. |

### ST10-EV-09 — Header, brand và breadcrumb navigation

| Trường | Đặc tả |
|---|---|
| Trigger / loại | Click #1, #2 hoặc breadcrumb links thuộc #4. |
| Input | data-path slugs (trang-chu, khoa-hoc-cua-toi, tien-do, thao-luan, thong-bao, tong-quan-khoa-hoc); href thực tế đều #. |
| Xử lý | Không gọi API trong HTML. Router/role guard/current item state không có source. |
| Kết quả | Destination screens theo inventory nếu được wired; hiện không thể xác nhận điều hướng hoặc session handoff. |

### ST10-EV-10 — Footer terms/privacy/help navigation

| Trường | Đặc tả |
|---|---|
| Trigger / loại | Click footer links #21. |
| Input | data-path slugs dieu-khoan-dich-vu, chinh-sach-bao-mat, tro-giup; href=#. |
| Xử lý | Không có API. Route hoặc external URL chưa được contract/source xác định. |
| Kết quả | Current action là placeholder fragment navigation; không giả định mở tab/window hoặc destination. |

### API, authorization và bảo mật

| API | Declared contract | Current source | Vai trò trong transition |
|---|---|---|---|
| #22 | GET /api/v1/lessons/{lesson_id}/access; Student Bearer; path int64; no query/body; ApiEnvelope<Lesson>; 200/401/403/404/500. | NOT_FOUND route/module/query/test; Draft DD. | Expected entitlement/prerequisite decision; response has no declared `allowed` or reason field. |
| #23 | POST /api/v1/lessons/{lesson_id}/start; Student Bearer; path int64; no query/body; ApiEnvelope<Lesson>; 201/401/403/404/422/500. | NOT_FOUND route/module/query/test; Draft DD. | Expected UPSERT progress IN_PROGRESS; conflicting BIGINT/UUID candidate schemas; key/idempotency/state updates unresolved. |
| #24 | GET /api/v1/lessons/{lesson_id}; Student Bearer; path int64; no query/body; ApiEnvelope<Lesson>; 200/401/403/404/500. | NOT_FOUND route/module/query/test; Draft DD. | Expected content retrieval; independent authorization/publish/projection unresolved. |

### Security rules for this screen

- Treat client order as UX orchestration only. Every protected server endpoint must own its authorization decision; direct calls to #23/#24 cannot rely on prior browser call to #22.
- Do not request/render content or video before the backend content endpoint confirms authorization. Do not copy public #09 fields into the protected flow.
- Current #09 itself is public and returns `content`/`video_url` for published lessons without checking enrollment. That current behavior is distinct from the missing #24 contract and requires a separate product/security decision if these fields are intended to be protected.
- Do not treat static SECURITY_GATE_ENFORCED, disabled button, 423_LOCKED, “Active” badge, bar width or Session Token copy as enforcement evidence.
- Do not assert that API #23 returns a media token: catalog type is Lesson, and no token field is declared.
- API #22 status 403 is catalogued, but its reason field/value/message is not. Do not create a reason enum or error body.
- Keep 403 vs 404 behavior, hiding of unpublished resources, enrollment status and prerequisite policy open until Product/Backend/security approve them.
- DDL and fake/test artifacts do not prove live schema. Do not build an upsert key or query from candidate DDL alone.

### Required decisions

1. #22 access predicate: eligible enrollment states, prerequisite model/order, JWT claim binding, allow signal, 403 reason field/type and 404 condition.
2. #23 progress upsert schema/identity and key: reconcile BIGINT `lesson_progress(user_id,lesson_id)` without composite unique against V1-PILOT UUID `lesson_progress_facts(enrollment_id,lesson_id)` with a unique pair; then decide fields updated/preserved, repeated-call and HTTP 201 semantics, idempotency/retry, transaction and direct-call authorization.
3. #24 server-side entitlement for independent calls; lesson and parent-course publish policy; 403/404 visibility; query/projection; content/video_url access and null serialization; LessonStatus enum; checked schema/nullability.
4. Resolve whether #23 response Lesson can include content/video_url before the separate #24 read.
5. ST-09 lesson-selection/lessonId source and ST-11 route/fetch ownership.
6. Error/loading/denied/failure UI and retry policy; no 423 mapping without catalog update.
7. Chốt trigger của #23 sau #22 allowed: auto-start theo sequence hay chờ thao tác Start; đồng thời chốt enabled state của #13.
8. Remove/approve static claims about “Session Token”, “permanent lock”, 423 and WCAG 2.1 AA; confirm Study design tokens and responsive/navigation behavior.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
