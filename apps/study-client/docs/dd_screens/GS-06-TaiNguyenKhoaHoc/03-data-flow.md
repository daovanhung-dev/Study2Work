# GS-06 — Data Flow & State

## 1. Nguồn dữ liệu
| Field / object | Type | Source | Destination | Cập nhật khi |
|---|---|---|---|---|
| Chỉ liệt kê theo bằng chứng trong excerpt bên dưới | Theo DD/API source | API/inventory/design; status phải giữ nguyên | UI/state nêu ở DD nguồn | Theo event source |

## 2. State model

> Không tạo DTO/ViewModel mới khi chưa có contract. State, DTO và mapping được trích nguyên ngữ cảnh từ DD nguồn bên dưới.

## 3. API DTO → ViewModel mapping

### Trích từ DD nguồn: B. Luồng hoạt động tổng thể

### Luồng dự kiến theo contract đã xác nhận được

1. GS-03 mở tab resource và chuyển cùng `courseId` vào route đề xuất. Current app không có route để kiểm chứng direct entry, query-state, back behavior hoặc auth/session.
2. Client cần xác nhận `courseId` có mặt trước khi tạo request. API #11 catalog yêu cầu `course_id:int64`, public/no Bearer, GET không body/query. Không có source implementation để xác định parser, validation response hay actual endpoint behavior.
3. Nếu gọi #11 theo design hiện có, response `data` được khai báo là một `Resource`. Do đó client không thể xác định collection rỗng, nhiều item, thứ tự hoặc tổng số. Không map response vào list; đánh dấu contract/config error và không hiển thị dữ liệu giả. Empty state chỉ hợp lệ khi API được sửa/duyệt trả một collection rỗng rõ ràng.
4. Khi collection contract được chốt và user chọn một item, lấy `resource.id` làm `resourceId`; không tự ghép URL từ ID hoặc đoán tên file.
5. Gọi #12 tại thời điểm user mở resource. API catalog là public GET không body/query; current backend đọc metadata và trả envelope. Current API không có visibility/access check hoặc storage signer, vì vậy không thể khẳng định 200 đồng nghĩa người dùng có quyền mở resource private.
6. Chỉ sau khi access policy, URL semantics và error contract được phê duyệt mới mở/tải `data.url`. Nếu thiếu URL, URL không hợp lệ, access bị từ chối hoặc mạng/API lỗi thì phải giữ nguyên state an toàn; exact copy/retry behavior cần product/API contract.
7. Khi được phép, điều hướng sang GS-07 với cùng `resourceId`; back trở lại GS-06 phải giữ `courseId` và tab. Cách lưu/restore state chưa được implement.

### Luồng hiện tại có thể xác nhận

- Browser chỉ có thể hiển thị ảnh/HTML tĩnh. Header, tabs và footer anchors phần lớn dùng `href="#"`; “Xem tài liệu tích hợp API” là anchor `#technical-contract-block`; nút tải có thuộc tính disabled. Không có API call hoặc JS handler trong HTML.
- API #11 chưa có executable route. API #12 là executable source, nhưng test chỉ được đọc, không chạy. Route/view evidence không chứng minh service đã deploy hoặc runtime end-to-end.
- Screenshot hiển thị “empty/gated” cùng lúc với giải thích contract đang chặn. Đây là design hand-off state, không chứng minh course thật không có resource. UI production phải phân biệt `empty collection` với `integration blocked/error`.

### Trích từ DD nguồn: D. Đặc tả sự kiện và xử lý dữ liệu

### Ma trận sự kiện

| Event ID | Tên / loại / trigger | Element | Điều kiện tiên quyết | Runtime status |
|---|---|---|---|---|
| `GS06-EV-01` | Mở resource tab / load — `Load`; route/tab GS-06 được kích hoạt | #6 | `courseId` phải đến từ GS-03; route và API contract phải được chốt. | Route/client không có; API #11 declared-only, response singleton không định nghĩa list/empty. |
| `GS06-EV-02` | Chọn resource — `Click/Select`; chọn một row | Resource row chưa có trong ảnh; list tương lai | Collection #11 đã được duyệt và render; item phải có ID nguồn. | Expected AC-06 flow; chưa có UI/item để chọn. |
| `GS06-EV-03` | Mở resource — `Click`; người dùng yêu cầu mở/tải item | Resource row/viewer chưa có; GS-07 handoff | Resource ID hợp lệ và access/URL/open policy được duyệt. | API #12 source-backed locally, nhưng quyền/signing policy chưa đáp ứng AC-06. |
| `GS06-EV-04` | Thử bấm tải — `Click`; user click/keyboard activation | #11 | Không thỏa: button `disabled`. | Không phát click action/request trong HTML hiện tại. |
| `GS06-EV-05` | Xem chi tiết hợp đồng API — `Click/Anchor`; activate bằng pointer hoặc keyboard | #12 | Fragment target `technical-contract-block` tồn tại trong document. | Browser xử lý fragment nội trang; không gọi API. |
| `GS06-EV-06` | Header navigation — `Click/Anchor`; activate logo hoặc link | #1 | Anchor đang hiển thị và enabled. | Native `href="#"`; không có route binding. |
| `GS06-EV-07` | Login/Register — `Click/Anchor`; activate một trong hai link | #2 | Anchor đang hiển thị và enabled. | Native `href="#"`; avatar không phải control. |
| `GS06-EV-08` | Đổi course tab — `Click/Anchor`; activate một trong bốn tab | #6 | Anchor đang hiển thị và enabled. | Native `href="#"`; query/tab state không đổi qua router. |
| `GS06-EV-09` | Footer navigation — `Click/Anchor`; activate một trong bốn link | #22 | Anchor đang hiển thị và enabled. | Native `href="#"`; destination chưa có route. |
| `GS06-EV-10` | Hiện tooltip lý do disabled — `Hover/Focus-within`; pointer hover hoặc focus-within button wrapper | #11 | Tooltip container/wrapper và CSS phải được render; keyboard focus path chưa đạt vì button disabled. | CSS conditional content only; no app/API call. |

### `GS06-EV-01` — Mở resource tab / load

- **Loại và trigger:** `Load`; mở trực tiếp route đề xuất hoặc kích hoạt tab Resources từ course detail. Hiện không có app route/event handler.
- **Precondition:** GS-03 phải truyền đúng `courseId`; route/tab semantics và #11 collection/access contract phải được duyệt. Chưa thỏa trong current Study Web.
- **Input:** route path đề xuất `/courses/:courseId?tab=resources`; path value tương ứng catalog `course_id:int64`. Frontend normalization/range behavior chưa có nguồn. Không đọc ID từ tên khóa học trong mockup; session không yêu cầu API #11.
- **Xử lý tuần tự:**
  1. Nếu screen được wired, nhận `courseId` từ route; không suy ra từ text prototype.
  2. Catalog #11 khai báo public GET `/api/v1/courses/{course_id}/resources`, không body/query và không yêu cầu Bearer.
  3. **Current behavior:** Study Web không có route/client; Study Server không có #11 route/module/query/test, nên không gửi request.
  4. Declared response là `ApiEnvelope<Resource>` đơn dù mục đích và quan hệ ERD là danh sách. Không map singleton thành collection, không dựng `{items,total}`, và không biểu diễn contract failure thành `empty`.
  5. Chỉ sau khi #11 có collection contract được duyệt mới xác định mapping item/empty/order/pagination; nguồn hiện tại không cho phép chốt các quyết định này.
- **Output:** current output là prototype gated state; không có loading/list/empty response do API. Empty chỉ có thể được hiển thị sau successful collection response với zero items theo contract tương lai.
- **Error/exception:** catalog #11 liệt kê 404 `DESIGN_RESOURCE_NOT_FOUND` và 500 `DESIGN_INTERNAL_ERROR`; không định nghĩa 403/422, empty semantics, transport retry/timeout hoặc user-facing copy. Do API không có runtime route, hiện không có response để map.

### `GS06-EV-02` — Chọn resource

- **Loại và trigger:** `Click/Select`; user chọn một resource row trong list tương lai. Không có row trong PNG/HTML hiện tại.
- **Precondition:** #11 phải trả collection schema đã duyệt; item phải hiện trên UI và access policy xác định được.
- **Input:** `resource.id` (`int64` theo `Resource` catalog). Không suy ra ID từ file name hoặc URL.
- **Xử lý:** nhận ID đúng từ row và chuyển cùng `courseId` sang bước mở EV-03. Không có request riêng trong event này. Cache, selection persistence và prefetch không được contract hóa.
- **Output:** current output không có vì chưa có list row; expected handoff là `resourceId` nguồn cho EV-03 khi UI/API được chốt.
- **Error/exception:** collection không có hoặc chỉ là response singleton thì không có item để chọn; không tạo resource giả, không gọi #12. Copy và retry cho integration error chưa được duyệt.

### `GS06-EV-03` — Mở resource đã chọn

- **Loại và trigger:** `Click`; user activates a selected resource's open/download action. Row/action is absent from current source image.
- **Precondition:** #11 collection/ID mapping, resource authorization, direct-vs-signed URL, expiry and open/download mode must be approved. Current implementation does not satisfy AC-06 private access.
- **Input:** `resourceId:int64` from selected `Resource.id`; current #12 has no query/body and catalog says no Bearer. No URL is formed by the client from ID.
- **Request:** current Study route is `GET /api/v1/resources/{resource_id}` with raw path `str`, DB dependency and trace ID; no Authorization parameter/dependency.
- **Current source processing, sequentially:**
  1. `validate_resource_id` parses the raw value using the shared integer parser and accepts only `1..9,223,372,036,854,775,807`; malformed, zero, negative or larger values return 404 before query.
  2. `RESOURCE_BY_ID` selects `id`, `lesson_id`, `name`, `resource_type AS type`, and direct `url` from legacy `resources` by ID.
  3. Missing resource returns 404.
  4. When `lesson_id` is non-null, `PUBLISHED_PARENT_COURSE` joins `lessons` to `courses`, excludes lesson status `DELETED`, and requires course status `PUBLISHED`; no matching parent returns 404. When `lesson_id` is null, this check is skipped and success remains possible.
  5. `ResourceDetail` maps `id:int`, `name:string`, `type:string`, `url:string|null`, `lesson_id:int|null`; `extra="ignore"` discards any `visibility` field.
  6. Success returns HTTP 200 `DESIGN_RESOURCE_RETRIEVED` with `data` metadata and the direct `resources.url`; source has no enrollment/visibility check and no Object Storage signer.
  7. SQLAlchemy query errors roll back and return safe HTTP 500 `DESIGN_INTERNAL_ERROR`; response-mapping `ValidationError` returns safe 500 without a write/commit. Neither branch exposes SQL/stack details.
- **Output:** endpoint response may contain a direct external URL, but HTTP 200 alone does not prove private-resource permission or safe download. Do not auto-open it while access policy is unresolved. GS-07 destination/return state is only proposed.
- **Error/exception:** current route returns 404 for malformed/out-of-range/non-positive ID, missing resource, missing/deleted parent lesson, or unpublished/missing parent course; 500 for query/mapping failure. There is no current 403, 410, signed-link expiry, retry or timeout contract. A network error has no current Study Web mapping.

### `GS06-EV-04` — Bấm nút tải

- **Loại và trigger:** `Click`; user click/keyboard-activates #11.
- **Precondition:** không thỏa vì HTML button mang thuộc tính `disabled` và `aria-disabled="true"`.
- **Input:** attempted activation only; no resource ID or request data is attached.
- **Processing:** native disabled-button behavior prevents the action; no API #11/#12 call, download or local state update occurs.
- **Output:** visible gated UI remains unchanged.
- **Error/exception:** no application/API error is produced. Enabling it requires approved selection, access, URL, download and expiry semantics; those remain open.

### `GS06-EV-05` — Xem chi tiết hợp đồng API

- **Loại và trigger:** `Click/Anchor`; pointer click or keyboard Enter on #12.
- **Precondition:** link is enabled and `id="technical-contract-block"` exists in the same HTML document.
- **Input:** fragment href `#technical-contract-block`; no API input.
- **Processing:** browser follows the fragment and scrolls to the contract section; no JavaScript/API handler runs.
- **Output:** current-document URL fragment changes and the contract section is brought into view; no `courseId` or resource state changes.
- **Error/exception:** no app/API error. If the fragment target is absent in a future document, the browser cannot scroll to that section; no recovery contract is defined.

### `GS06-EV-06` — Header primary navigation

- **Loại và trigger:** `Click/Anchor`; activate the logo or one of the three header links (#1), by pointer or keyboard.
- **Precondition:** a visible anchor is activated; native HTML anchor behavior applies.
- **Input:** `href="#"`; `data-path` strings are `trang-chu`, `khoa-hoc`, `tim-kiem` and are not consumed by a handler.
- **Processing:** browser follows the current-document empty fragment (normally returning scroll to the top); there is no router/API call.
- **Output:** no supported Screen ID transition, data handoff or state update can be claimed.
- **Error/exception:** no business/API error exists. Destination, back behavior and active-nav state are not defined in current Study Web source.

### `GS06-EV-07` — Login/Register

- **Loại và trigger:** `Click/Anchor`; activate Đăng nhập or Đăng ký (#2).
- **Precondition:** one of the visible anchors is activated. Profile icon has no action/control semantics.
- **Input:** `href="#"` with `data-path=dang-nhap` or `dang-ky`; no credential/session input.
- **Processing:** native anchor follows the current-document fragment; no auth handler or API request is present.
- **Output:** no supported transition to SH-02/SH-03 and no session/token change.
- **Error/exception:** no API error. Authentication route and return-to-resource policy are not present in current app source.

### `GS06-EV-08` — Đổi course tab

- **Loại và trigger:** `Click/Anchor`; activate one of four course tabs (#6).
- **Precondition:** tab anchor is visible/enabled; the page is the static prototype.
- **Input:** anchor `href="#"`; visible labels identify overview, curriculum GS-04, reviews GS-05, resources GS-06. `courseId` is not encoded in the anchor.
- **Processing:** browser follows the current-document fragment; no route/query update, #08/#09/#10/#11 request, cache operation or history-state update occurs. Resources remains styled active in the static markup.
- **Output:** tab content and route do not change; no data is handed off.
- **Error/exception:** no API error occurs. Expected route is `/courses/:courseId?tab=resources`, but route preservation/back behavior has no current wiring.

### `GS06-EV-09` — Footer navigation

- **Loại và trigger:** `Click/Anchor`; activate any of the four footer links (#22).
- **Precondition:** link is visible/enabled; browser has loaded the current prototype document.
- **Input:** `href="#"` and static `data-path` metadata; no route params or form data.
- **Processing:** browser follows the empty fragment; no route handler/API call runs.
- **Output:** no supported destination, resource-state change or Screen ID handoff.
- **Error/exception:** no business/API error. Destination and recovery/back behavior are unspecified.

### `GS06-EV-10` — Hiện tooltip lý do disabled

- **Loại và trigger:** `Hover/Focus-within`; pointer enters the `group` wrapper around #11, or an element inside it receives focus.
- **Precondition:** CSS utility styles load and the wrapper/tooltip exist. Tooltip starts with `hidden` and is shown by `group-hover:flex` or `group-focus-within:flex`.
- **Input:** pointer hover or DOM focus state; no resource ID, form value or network input.
- **Processing:** CSS changes tooltip display only. Its static copy says API #12 needs a time-limited signed URL; that copy is not current API behavior. No JavaScript handler or API request runs.
- **Output:** mouse hover can reveal the tooltip. The button is `disabled`, so keyboard users cannot focus it; current markup does not establish the advertised focus-within path as keyboard-accessible.
- **Error/exception:** no app/API error. If external Tailwind CSS is unavailable, utility-driven reveal/styling is not established; no fallback interaction is implemented.

### API request/response và giới hạn

| API | Request | Current/design response | Auth/access | Status và giới hạn |
|---|---|---|---|---|
| #11 | `GET /api/v1/courses/{course_id}/resources`; `course_id:int64`; no body/query; public/no Bearer. | Catalog/API DD `ApiEnvelope<Resource>` đơn: `id`, `name`, `type`, `url`, `visibility`, `lesson_id`; `visibility` không có source. Không có current route/module/query/test. | Catalog nói public; AC-06 yêu cầu public-or-authorized. Chưa thống nhất. | Declared 200/404/500; không có list cardinality, pagination/order hoặc empty semantics. `DECLARED_NOT_RUNNABLE`; API DD Draft. |
| #12 | `GET /api/v1/resources/{resource_id}`; catalog type `int64`; no body/query; public/no Bearer. Current router nhận raw path `str` rồi validator chấp nhận positive signed-int64. | Current response `data={id:int,name:string,type:string,url:string|null,lesson_id:int|null}` trong envelope; bỏ `visibility`; URL là `resources.url` trực tiếp. API DD vẫn Draft và câu `DECLARED_NOT_RUNNABLE` đã stale so với source/test/report. | Route không có Bearer dependency; conditional parent gate chỉ khi `lesson_id` non-null. Không có visibility/enrollment check hoặc signer; null `lesson_id` không bị parent-gate. | Current source: 200 `DESIGN_RESOURCE_RETRIEVED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 500 `DESIGN_INTERNAL_ERROR`; SQL error rollback; mapping error 500. Không có 403/410/TTL. |

Đối với cả hai GET, retry, timeout, cache invalidation, de-duplication khi click liên tiếp, CORS/storage headers và download disposition chưa có client contract. Không tự đặt giá trị mặc định. Legacy `DB.sql` có `resources` nhưng thiếu `visibility`; V1-PILOT schema không có `resources`; live schema/deployment chưa được xác minh.

### Trích từ DD nguồn: E. Ma trận trạng thái và điều hướng

| State | Điều kiện vào | Hiển thị/behavior | Trạng thái bằng chứng |
|---|---|---|---|
| `prototype-gated` | HTML/PNG hiện tại được mở | Gated headline, disabled download, API reference và state inventory. | **Current static asset**; không phải server response. |
| `loading` | #11 được gọi khi route/tab active. | Loading skeleton/spinner chưa có trong asset; nội dung/timeout chưa được thiết kế. | Expected implementation state; Study Web/API #11 chưa wired. |
| `contract-blocked` | API #11 không runnable hoặc trả shape không khớp collection consumer. | Không render resource giả; thông báo integration/unavailable cần copy được duyệt. Không map sang empty. | Current integration blocker; error code/display chưa có contract. |
| `empty` | Chỉ khi API đã duyệt trả collection thành công với zero items. | Empty message và action chưa được chốt; prototype gated copy không đủ để phân biệt rỗng thật. | Future state; không thể xác nhận bằng `ApiEnvelope<Resource>` singleton. |
| `list-ready` | API #11 trả collection schema đã duyệt. | Render từng item bằng fields có nguồn; chọn item → EV-02. Type grouping, order, paging, duplicate IDs chưa có contract. | Future state; data model/UI chưa hoàn thiện. |
| `resource-loading` | User chọn item và EV-03 gọi #12. | Progress state chưa có asset. | Future state; #12 source exists, UI not wired. |
| `resource-ready` | #12 200 và access policy/URL semantics đã xác nhận. | Handoff/open selected resource; destination GS-07 với `resourceId`. | #12 current source returns direct URL, nhưng AC-06 security requirement chưa được đáp ứng/approved. |
| `not-found-or-not-public` | #11/#12 404 theo catalog/source, gồm resource thiếu và parent lesson/course không đạt gate của current #12. | Không tự phân biệt các trường hợp cùng 404 hoặc tự điều hướng tới SH-06; destination/copy cần contract. | Status source-backed for #12; exact client copy/navigation not defined. |
| `forbidden` | Access denied theo AC-06 (403). | Không mở URL; có thể yêu cầu sign-in/permission only after product decides copy/path. | AC-06 only; API catalog/#12 source không khai báo 403. |
| `expired-link` | Signed URL hết hạn (prototype nêu 410). | Không dùng URL cũ; prototype nhắc tạo lại nhưng không có nút/endpoint thực tế. | No current signer, TTL, or 410 contract. |
| `request-error` | #11/#12 500 hoặc network failure. | Không chuyển lỗi thành empty; retry action/copy/policy chưa có nguồn. | API catalog/current #12 declares 500; client error UI is absent. |

### Điều hướng và dữ liệu bàn giao

- **GS-03 → GS-06:** truyền nguyên `courseId`, giữ tab `resources`; expected route query state, current tabs không đổi route.
- **GS-06 → GS-07:** chỉ sau chọn resource và xác nhận quyền; truyền `resourceId`; route inventory `/resources/:resourceId`. Current card/link để mở resource chưa tồn tại.
- **GS-06 → ST-12:** inventory liên kết tài liệu kèm bài học. ST-12 route dùng `lessonId` và API #26; không suy ra lesson resource semantics từ #11/#12. `lesson_id` trong #12 nullable model/current source; API #11 list mapping chưa có.
- **Back:** cần giữ `courseId`/tab và tránh reuse URL tạm hết hạn; router/cache policy chưa có.
- **Header/footer/auth links:** tất cả placeholder `href="#"` (trừ #9 fragment link); không suy ra route target hoặc auth requirement.

## 4. Luồng đọc (Read)
- Orchestration từ inventory: GET #11 → người dùng chọn id → GET #12 trước khi mở URL; không suy diễn visibility.
- Chi tiết current/source mapping: xem [API Integration](04-api-integration.md) và DD nguồn.

## 5. Luồng ghi (Write)
- Chỉ mô tả mutation được DD/API source nêu; không thêm endpoint hoặc side effect.
- Source trace: [GS-06](../../screen_stitch/02_guest_discovery/GS-06_tai-nguyen-khoa-hoc/GS-06.md)

## 6. Cache / concurrency / lifecycle
- Cache, race, cleanup, pagination: xem các section source bên dưới; nếu không có bằng chứng thì để `CẦN_XÁC_NHẬN`.

## 7. Data errors & security
- Theo error/security/source-status section của DD nguồn; không coi state trong mockup là runtime behavior.

## 8. Trace
[Events](02-events.md) · [API](04-api-integration.md) · [Rules](05-business-rules.md)
