# ST-11 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `ST-11-EV-001` | `ST11-EV-01` / ST11-EV-01 — Mở route và nhận lesson context | See source event detail below |
| `ST-11-EV-002` | `ST11-EV-02` / ST11-EV-02 — Nạp nội dung lesson bằng API #24 | See source event detail below |
| `ST-11-EV-003` | `ST11-EV-03` / ST11-EV-03 — Phát/dừng/điều khiển media | See source event detail below |
| `ST-11-EV-004` | `ST11-EV-04` / ST11-EV-04 — Lưu lesson progress bằng API #25 | See source event detail below |
| `ST-11-EV-005` | `ST11-EV-05` / ST11-EV-05 — Hoàn thành bài và lấy bài kế tiếp bằng API #27 | See source event detail below |
| `ST-11-EV-006` | `ST11-EV-06` / ST11-EV-06 — Tải tài nguyên đính kèm bằng API #26 | See source event detail below |
| `ST-11-EV-007` | `ST11-EV-07` / ST11-EV-07 — Quay lại khóa học | See source event detail below |
| `ST-11-EV-008` | `ST11-EV-08` / ST11-EV-08 — Footer navigation | See source event detail below |
| `ST-11-EV-009` | `Source heading` / API, authorization và bảo mật | See source event detail below |
| `ST-11-EV-010` | `Source heading` / Security decisions and handling | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả chi tiết từng sự kiện

> Các phần dưới đây tách expected inventory/AC khỏi current HTML. Mọi quyết định chưa có trong catalog/API DD được giữ là `SOURCE_REQUIRED`; không tự đặt polling, retry, timeout, debounce, throttle, autosave interval, position unit, cache hay next-navigation behavior.

### ST11-EV-01 — Mở route và nhận lesson context

| Trường | Đặc tả |
|---|---|
| Trigger / loại | Browser route load `/student/lessons/:lessonId`; page-level load. |
| Element | Page-level; không có route element trong static HTML. |
| Input | `lessonId` từ ST-10; APIs #24–#27 khai path `lesson_id:int64!`; Student auth context theo catalog Bearer JWT/role Student. |
| Điều kiện | Route phải được wire; lessonId và Student context phải có nguồn hợp lệ. ST-10/ST-09 asset hiện không cung cấp ID. Positive/range/parse-error behavior chưa được chốt. |
| Quy trình expected | 1) Nhận route. 2) Parse ID theo contract đã duyệt; không tự tạo/fallback ID. 3) Kiểm tra auth context theo auth owner; không dùng text UI làm role proof. 4) Không gọi content/resources/progress/next nếu input/auth không được xác nhận. 5) Đợi quyết định fetch ownership #24 với ST-10 trước khi triển khai. |
| Current result / ngoại lệ | Không có route/router/auth guard trong editable Study Web source. Không có error/redirect UI. API endpoint parse behavior chưa source-backed. |

### ST11-EV-02 — Nạp nội dung lesson bằng API #24

| Trường | Đặc tả |
|---|---|
| Trigger / loại | Expected page load sau khi route/session context hợp lệ; GET/API. |
| Element | Expected data mapping cho #7 và player (player hiện không có); #8 là static fallback copy. |
| Request | `GET /api/v1/lessons/{lesson_id}`; path `lesson_id:int64!`; Bearer JWT/Student theo catalog; không query/body. |
| Declared response | `ApiEnvelope<Lesson>`; success 200 `DESIGN_RESOURCE_RETRIEVED`; errors 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 500 `DESIGN_INTERNAL_ERROR`. |
| Lesson mapping | `id:int64`, `course_id:int64`, `title:string`, `content?:string`, `video_url?:uri`, `order:int32`, `status:LessonStatus`. Optional/null serialization và enum values chưa chốt. |
| Quy trình | 1) Chọn request owner giữa ST-10 và ST-11; hiện inventory của hai màn hình đều liệt kê #24. 2) Nếu ST-11 owner theo quyết định, gửi path/JWT không kèm parameter khác. 3) Chỉ map `Lesson` sau success và server-side access/publish approval. 4) Giữ content/media ẩn ở các nhánh lỗi/deny. 5) Không tự biến 403/404 thành một trạng thái khác nếu error mapping chưa duyệt. |
| Current result / ngoại lệ | #24 Draft; không có Student route/module/query/test. Authorization độc lập, publish scope, response projection, 403/404, path parse và media URL access còn mở. Static “nội dung chưa sẵn sàng” không phải HTTP error state. |

### ST11-EV-03 — Phát/dừng/điều khiển media

| Trường | Đặc tả |
|---|---|
| Trigger / loại | Expected player controls: play/pause/seek/timeupdate; các loại event cụ thể chưa có nguồn. |
| Element | Không có player/media/control trong screenshot hoặc HTML; icon #6 chỉ trang trí. |
| Input | Có thể gồm `video_url?` từ #24, nhưng allowed URL/signed URL, player engine, media metadata và caption source chưa được quy định. |
| Quy trình | Chưa thể đặc tả implementation steps vì không có control, source media policy, playback state model hoặc player choice. Khi có contract: chỉ dùng URL từ authorized #24; không lấy URL từ public curriculum #09 hoặc tự tạo token. |
| Current result / ngoại lệ | Không có `<video>`, `<audio>`, `<iframe>`, `<source>`, fetch/handler hoặc playback state. Không auto-play, seek, resume, retry media hay phát stream trong current design. |

### ST11-EV-04 — Lưu lesson progress bằng API #25

| Trường | Đặc tả |
|---|---|
| Trigger / loại | Inventory ghi PATCH #25 khi có progress event hợp lệ; event source/tần suất chưa chốt. |
| Element | Không có progress/player control trong asset; event page-level kỳ vọng. |
| Input/request | `PATCH /api/v1/lessons/{lesson_id}/progress`; Bearer JWT/Student; body bắt buộc `{position:int32, percent:int32, completed:boolean}`; no query theo catalog. |
| Declared response/status | `ApiEnvelope<Lesson>`; 200 `DESIGN_RESOURCE_UPDATED`; 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 404 `DESIGN_RESOURCE_NOT_FOUND`; 422 `DESIGN_VALIDATION_ERROR`; 500 `DESIGN_INTERNAL_ERROR`. |
| Quy trình kỳ vọng | 1) Chỉ trigger khi product xác định event hợp lệ. 2) Map position unit/range và percent consistency sau API/schema decision. 3) Gửi đúng ba fields bắt buộc; không thêm fields. 4) Chờ response; giữ an toàn trước response hoặc network ambiguity. 5) Chỉ áp dụng response mapping sau khi Lesson/progress payload được xác nhận; response type Lesson hiện không nêu progress fields. 6) AC-14 nói update lesson progress + course aggregate; aggregate update/transaction chưa có implementation contract. |
| Retry/dedup | API catalog không khai idempotency key/409. Open questions chưa chốt request ordering, duplicate writes, out-of-order progress, throttle, autosave, retry/backoff hoặc offline queue. Không tự chọn interval/retry hoặc cho phép request cũ ghi đè state mới. |
| Current result / ngoại lệ | #25 Draft, không có Student route/module/query/test. Legacy `lesson_progress` candidate không có `position` hay unique `(user_id,lesson_id)`; V1-PILOT `lesson_progress_facts` cũng không có `position`/`percent`, còn `block_progress_facts.last_position_seconds` là block-scoped. Range, completed transition/timestamp, identity binding, direct-call authorization, 404/422 và aggregate semantics open. |

### ST11-EV-05 — Hoàn thành bài và lấy bài kế tiếp bằng API #27

| Trường | Đặc tả |
|---|---|
| Trigger / loại | Inventory nói GET #27 sau completed; completion signal và auto-navigation/button trigger chưa được đặc tả. |
| Element | Không có completion control, finished state hoặc Next CTA trong asset. |
| Input/request | `GET /api/v1/lessons/{lesson_id}/next`; path `lesson_id:int64!`; Bearer JWT/Student; no query/body theo catalog. |
| Declared response/status | `ApiEnvelope<Lesson>`; 200 `DESIGN_RESOURCE_RETRIEVED`; 401/403/404/500 với business codes tương ứng catalog. |
| Quy trình | 1) Chỉ gọi sau khi completion condition được chốt. 2) API owner phải định nghĩa entitlement/publish check cho lời gọi trực tiếp; không dùng một client call trước đó làm bằng chứng quyền. 3) Nếu có Lesson success, chỉ map field theo approved projection. 4) Không giả định route update, tự động chuyển trang hoặc bài kế tiếp tồn tại. |
| Open contract | Curriculum/course scope, sort order/tie-break, hidden/draft lesson filter, 403/404, current lesson missing, “đã là bài cuối” và response null/empty semantics đều mở. 404 chưa thể được diễn giải thành finished. |
| Current result / ngoại lệ | #27 Draft; không có Student route/module/query/test hoặc control để kích hoạt. Không có end-of-course state hiện hữu. |

### ST11-EV-06 — Tải tài nguyên đính kèm bằng API #26

| Trường | Đặc tả |
|---|---|
| Trigger / loại | Inventory ghi GET #26 lazy; intended resource-panel open/load, nhưng trigger chưa có UI/AC detail. |
| Element | Không có tài nguyên panel, tab hoặc link trong asset; ST-12 là màn hình liên quan riêng. |
| Request | `GET /api/v1/lessons/{lesson_id}/resources`; path `lesson_id:int64!`; Bearer JWT/Student; no query/body theo catalog. |
| Declared response/status | `ApiEnvelope<Lesson>`; 200 `DESIGN_RESOURCE_RETRIEVED`; 401/403/404/500 với business codes tương ứng. |
| Quy trình | 1) Chỉ thực hiện sau khi resource UI/trigger và lazy/eager ownership được duyệt. 2) Gửi path/JWT, không thêm filter/paging. 3) Không thể map list từ `Lesson` nếu response contract chưa đổi/giải thích. 4) Không mở stored URL, signed URL hay external site trước khi URL/visibility policy và server-side entitlement được duyệt. |
| Current result / ngoại lệ | #26 Draft, không có route/module/query/test. Response type/cardinality, ordering, empty state, resource visibility, #12 signed URL relation, 403/404 và path semantics open. |

### ST11-EV-07 — Quay lại khóa học

| Trường | Đặc tả |
|---|---|
| Trigger / loại | Click #1/#2/#3/#10/#13; native anchor navigation. |
| Input | Static href `/student/courses`; no `courseId`, lessonId or history context. |
| Current processing | HTML có anchor và visible text; không có click handler. Browser path navigation có thể phát sinh nhưng Study Web router/serving chưa xác minh. |
| Expected result | Inventory liên kết ST-09 (`/student/courses/:courseId`), trong khi href hiện tại chỉ `/student/courses`. Chọn danh sách hay course overview, return context và auth guard chưa chốt. Không tuyên bố anchor này tới ST-09. |

### ST11-EV-08 — Footer navigation

| Trường | Đặc tả |
|---|---|
| Trigger / loại | Click #12, #13 hoặc #14; native anchor. |
| Input | Href lần lượt `/student`, `/student/courses`, `/student/progress`. |
| Current processing | Static links, không API/handler. |
| Expected result / gaps | Các path không được xác nhận bằng router runtime. `/student/courses` thiếu `courseId`; footer link không mang lesson context. Không tự thêm query, return stack hoặc session behavior. |

### API, authorization và bảo mật

| API | Declared contract | Current source | Vai trò / open issue |
|---|---|---|---|
| #24 | GET `/api/v1/lessons/{lesson_id}`; Student Bearer; path int64; `ApiEnvelope<Lesson>`; 200/401/403/404/500. | NOT_FOUND Student route/module/query/test; DD Draft. | Lesson retrieval; direct entitlement, publish, projection/null/error/path chưa chốt; fetch ownership đè lên ST-10. |
| #25 | PATCH `/api/v1/lessons/{lesson_id}/progress`; Student Bearer; required int64 path + body `position:int32!`, `percent:int32!`, `completed:boolean!`; `ApiEnvelope<Lesson>`; 200/401/403/404/422/500. | NOT_FOUND Student route/module/query/test; DD Draft. | Progress update + AC aggregate intent; body semantics, storage, identity, update order/idempotency/throttle/retry/transaction unresolved. |
| #26 | GET `/api/v1/lessons/{lesson_id}/resources`; Student Bearer; int64 path; no query/body; `ApiEnvelope<Lesson>`; 200/401/403/404/500. | NOT_FOUND Student route/module/query/test; DD Draft. | Resource retrieval; declared payload conflicts with resource purpose/schema; URL/visibility/cardinality/access open. |
| #27 | GET `/api/v1/lessons/{lesson_id}/next`; Student Bearer; int64 path; no query/body; `ApiEnvelope<Lesson>`; 200/401/403/404/500. | NOT_FOUND Student route/module/query/test; DD Draft. | Next lesson lookup; order/tie-break/access/end-of-curriculum semantics open. |

#### Security decisions and handling

- API catalog declares Student Bearer authentication for #24–#27. The API DD open questions still require the owner to define the entitlement predicate and direct-call behavior for each endpoint; a prior client call to #22 or #24 is not evidence that a later independent request is authorized.
- Keep protected content/media out of UI until a successful #24 response under the approved access policy. Public curriculum API #09 is not a protected-content substitute; do not rely on a client route guard as a security boundary.
- Do not assume `video_url` is signed, public, stream-safe or allowed outside the authorized player; the catalog merely marks it optional URI.
- Do not assume #25 response carries progress or a safe position. Catalog response is Lesson and the position storage is unresolved.
- Do not treat absent resources, terminal next lesson, 403, 404, expired session or network error as interchangeable; mapping is open.
- Do not use either checked-in DDL artifact as live schema or combine their identifiers. Legacy `lesson_progress` has nullable user/lesson IDs and no lesson `position` or user/lesson unique key; V1-PILOT `lesson_progress_facts` is UUID/enrollment-based and also has no `position`/`percent`. Neither artifact provides `resources.visibility`.
- Do not create a token/session field, player URL, signed URL, cache key, retry protocol or telemetry event without a canonical source.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
