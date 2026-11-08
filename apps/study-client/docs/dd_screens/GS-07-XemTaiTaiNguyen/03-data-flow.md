# GS-07 — Data Flow & State

## 1. Nguồn dữ liệu
| Field / object | Type | Source | Destination | Cập nhật khi |
|---|---|---|---|---|
| Chỉ liệt kê theo bằng chứng trong excerpt bên dưới | Theo DD/API source | API/inventory/design; status phải giữ nguyên | UI/state nêu ở DD nguồn | Theo event source |

## 2. State model

> Không tạo DTO/ViewModel mới khi chưa có contract. State, DTO và mapping được trích nguyên ngữ cảnh từ DD nguồn bên dưới.

## 3. API DTO → ViewModel mapping

### Trích từ DD nguồn: B. Luồng hoạt động tổng thể

### Luồng dự kiến sau khi contract được chốt

1. GS-06 hoặc ST-12 điều hướng tới route đã được duyệt, truyền `resourceId`; nếu cần giữ ngữ cảnh, nguồn cũng phải xác định `courseId`/`lessonId` và destination khi quay lại.
2. Client kiểm tra path param theo contract `resource_id:int64`. Không có client parser/route hiện tại để xác minh invalid-ID UX.
3. Hiển thị loading state và gọi #12 `GET /api/v1/resources/{resource_id}` theo catalog. Catalog khai báo public/no Bearer; thay đổi auth semantics cần được cập nhật trong hợp đồng trước khi triển khai.
4. Backend hiện kiểm tra ID dương signed-int64, truy vấn resource và, nếu `lesson_id` có giá trị, kiểm tra lesson không `DELETED` cùng course `PUBLISHED`. Thiếu row hoặc parent không hợp lệ trả 404. `lesson_id=null` bỏ qua parent check.
5. Backend hiện trả `id`, `name`, `type`, `url`, `lesson_id`; không kiểm tra access, visibility hoặc signer. Trước khi mở file cần product/backend/storage chốt liệu URL public hay signed, ai được truy cập, expiry và lỗi tương ứng. Hiện chưa đạt.
6. Sau khi policy và renderer được xác nhận: mở preview cho type/MIME được allowlist; fallback download khi download được phép. Trạng thái URL null, unsupported type, expiry, network failure, retry và URL safety chưa có contract.
7. Khi back, khôi phục đúng source (GS-06 hay ST-12) và context được xác nhận. Không mặc định luôn quay GS-06 chỉ từ prototype.

### Luồng hiện tại có thể xác nhận

- HTML render gated viewer tĩnh. Không có `iframe`, `video`, `object`, `embed`, fetch, XHR hoặc Axios. Không có resource metadata thật.
- Zoom in/out/fullscreen và download là disabled. Back, breadcrumb, header và footer anchors dùng `href="#"`; `data-path` không có router handler trong file.
- State simulator có thể đổi 6 tab và text của panel; không gọi API, render media, bật control, đổi permission hoặc lưu URL. Initial screenshot và code sau khi chọn tab Gated cũng có status copy khác nhau.
- Backend #12 có current route/view/query/validator/model và test source; các test được đọc nhưng không chạy. Không có bằng chứng runtime/deployment hoặc kết nối Study Web.

### Trích từ DD nguồn: D. Đặc tả sự kiện và xử lý dữ liệu

### Ma trận sự kiện

| Event ID | Tên / loại / trigger | Element | Điều kiện tiên quyết | Runtime status |
|---|---|---|---|---|
| `GS07-EV-01` | Direct entry / load resource — `Load` khi vào route detail hoặc mở trực tiếp URL | Route đề xuất `/resources/:resourceId`; không có DOM control tương ứng | Có `resourceId` từ caller; route/client và access contract phải được duyệt | Current HTML không hydrate ID hoặc gọi API; Study Web `UNWIRED`. API #12 có source cục bộ nhưng không kiểm tra resource access. |
| `GS07-EV-02` | Thử zoom/fullscreen — `Click`/keyboard activation | #8–#10 | Không đạt: ba button mang `disabled` | Không đổi viewer; không có API hoặc Fullscreen API call. |
| `GS07-EV-03` | Tải resource — `Click`/keyboard activation | #15 | Không đạt: button `disabled`/`aria-disabled`; chưa có URL/access/download policy | Không tải file; không gọi API. |
| `GS07-EV-04` | Quay lại resource list — `Click/Anchor` | #16 | Anchor hiển thị; destination/context chưa wired | Native fragment `#`; không chuyển route hoặc giữ context. |
| `GS07-EV-05` | Breadcrumb — `Click/Anchor` | #2 | Anchor hiển thị; `data-path` không phải router contract | Native fragment `#`; không có Screen ID transition. |
| `GS07-EV-06` | Header navigation/login/register — `Click/Anchor` | #1 | Kích hoạt một anchor; profile icon là `div`, không phải control | Native fragment `#`; không có route/auth behavior. |
| `GS07-EV-07` | Chọn state hand-off — `Click` | #18–#23; cập nhật panel #24 | HTML script và các tab được render | Chỉ chạy local text simulator; không mô phỏng API/viewer/download. |
| `GS07-EV-08` | Footer navigation — `Click/Anchor` | #26 | Kích hoạt một footer anchor | Native fragment `#`; destination chưa map. |

### `GS07-EV-01` — Direct entry / load resource

- **Loại và trigger:** `Load`; mở trực tiếp `/resources/:resourceId` hoặc điều hướng từ màn hình nguồn. Route này mới là proposal trong inventory; Study Web hiện không có route/client.
- **Precondition:** GS-06 hoặc ST-12 phải cung cấp `resourceId` theo contract được duyệt. Với ST-12, cần xác định có giữ `lessonId`/source context hay không. Resource access policy phải rõ trước khi hiển thị hoặc mở URL.
- **Input:** `resourceId` trong proposed path, tương ứng catalog `resource_id:int64`; API #12 không có query/body và catalog ghi public/no Bearer. Catalog không quy định client parser, timeout, retry hoặc cache.
- **Processing tuần tự:**
  1. Nếu frontend được nối, nhận path param nguyên trạng; không suy ID từ tên file, text mock hoặc URL.
  2. **Current UI:** HTML chỉ hiển thị literal `:resourceId`; không có router/hydration/fetch. Do đó không request được phát trong prototype.
  3. **Current API route:** `GET /api/v1/resources/{resource_id}` được compose trong `apps/study-server/app/api/v1.py`; route nhận raw `str`, DB dependency và trace ID, không có Authorization dependency.
  4. `validate_resource_id` parse integer và chỉ nhận `1..9,223,372,036,854,775,807`; malformed, zero, âm hoặc overflow trả 404 `DESIGN_RESOURCE_NOT_FOUND` trước DB.
  5. Q1 đọc `id`, `lesson_id`, `name`, `resource_type AS type`, `url` từ `resources` theo bind `resource_id`; không có row thì trả 404.
  6. Chỉ khi `lesson_id` khác `NULL`, Q2 join `lessons`/`courses`, loại lesson `DELETED` và yêu cầu course `PUBLISHED`. Không có parent hợp lệ thì trả 404. Khi `lesson_id=NULL`, source bỏ qua parent lookup và vẫn có thể trả 200.
  7. Response model trả `id:int`, `name:string`, `type:string`, `url:string|null`, `lesson_id:int|null`; extra như `visibility` bị ignore. Success là HTTP 200 `DESIGN_RESOURCE_RETRIEVED` với direct `resources.url` trong `data`.
  8. SQLAlchemy query error rollback rồi trả 500 `DESIGN_INTERNAL_ERROR`; response mapping `ValidationError` cũng trả safe 500, không commit. Không có storage/network side effect trong API #12.
  9. Chỉ sau khi policy được phê duyệt mới quyết định preview/download và đưa URL vào viewer. Hiện không tự mở URL: 200 metadata không chứng minh quyền truy cập private resource.
- **Output:** Current browser output là gated static screen; không có response/API state. Nếu #12 được gọi ngoài UI, output source-backed là metadata trong envelope, không phải authorization result cho private object.
- **Error/exception:** Current #12 trả 404 `DESIGN_RESOURCE_NOT_FOUND` cho invalid path, absent resource hoặc parent check fail; 500 `DESIGN_INTERNAL_ERROR` cho query/mapping error. AC-06 có expected 403/404 access branch nhưng current route không có 403; catalog/source không có 401, 410, signer/expiry. Network/timeout, null URL UI, retry/copy mapping chưa được xác định.

### `GS07-EV-02` — Thử zoom hoặc fullscreen

- **Loại và trigger:** `Click` hoặc keyboard activation khi user thử một trong #8 (zoom in), #9 (zoom out), #10 (fullscreen).
- **Precondition:** Không đạt trong current HTML: cả ba `<button>` đều `disabled`.
- **Input:** Attempted activation; không có scale, keyboard modifier, resource ID hoặc request payload được gắn với handler.
- **Processing:** Browser native disabled-button behavior chặn activation; không đổi scale, không gọi Fullscreen API, không đổi layout và không gọi #12.
- **Output:** Toolbar và viewer giữ nguyên gated appearance.
- **Error/exception:** Không phát application/API error. Limits, keyboard behavior, mobile behavior và renderer capability phải được quyết định trước khi bật controls; hiện chưa có source/contract.

### `GS07-EV-03` — Tải resource

- **Loại và trigger:** `Click` hoặc keyboard activation trên #15 “Tải xuống tài nguyên”.
- **Precondition:** Không đạt vì button có `disabled` và `aria-disabled="true"`; HTML không có href/URL/filename/download handler. Future activation còn phụ thuộc access authorization, URL/origin, MIME/content-disposition, expiry và download policy.
- **Input:** Attempted activation only; không có `resourceId`/URL/filename được gửi.
- **Processing:** Native disabled-button behavior chặn hành động; không phát request, không tạo download và không thay đổi state.
- **Output:** Không có file được mở/lưu; page giữ nguyên.
- **Error/exception:** Không có app/API error hiện tại. Retry, signed-link renewal, expired-link mapping, file naming và network failure behavior đều chưa được contract hóa.

### `GS07-EV-04` — Quay lại resource list

- **Loại và trigger:** `Click/Anchor`; activate #16 bằng pointer hoặc keyboard.
- **Precondition:** Page đã render static anchor. Return destination và source context chưa được wired.
- **Input:** `href="#"`, `data-path="khoa-hoc"`; không có `resourceId`, `courseId`, `lessonId` hoặc source-screen token trong URL.
- **Processing:** Browser xử lý empty fragment; không chạy router, history restore hoặc API call. Không thể xác định đây là GS-06 runtime transition chỉ từ `data-path`.
- **Output:** Không có supported Screen ID handoff hay context preservation; trang prototype vẫn là nguồn evidence duy nhất.
- **Error/exception:** Không có business/API error. Quyết định quay GS-06 hay ST-12 và bảo toàn list/lesson position còn mở.

### `GS07-EV-05` — Breadcrumb

- **Loại và trigger:** `Click/Anchor`; activate một trong hai breadcrumb anchors #2.
- **Precondition:** Anchor hiển thị và browser đang ở prototype page.
- **Input:** Cả hai link dùng `href="#"`; `data-path="khoa-hoc"`; không mang resource/course/lesson ID.
- **Processing:** Native empty-fragment navigation; không route, không gọi API và không phục hồi filter/scroll state.
- **Output:** Không chuyển tới resource list/course route trong source hiện tại.
- **Error/exception:** Không có app/API error. Exact destinations cần route contract; chữ breadcrumb không chứng minh route.

### `GS07-EV-06` — Header navigation và auth links

- **Loại và trigger:** `Click/Anchor`; activate logo, header link, login hoặc register (#1). Profile icon chỉ là `div`.
- **Precondition:** Anchor đang hiển thị. Avatar không có button/link role hoặc event handler trong HTML.
- **Input:** `href="#"`; các `data-path` ghi `trang-chu`, `khoa-hoc`, `tim-kiem`, `dang-nhap`, `dang-ky`; không có auth form/session data.
- **Processing:** Browser theo empty fragment; không gọi auth API, không đổi session/token và không chạy route resolver.
- **Output:** Không có route transition hoặc data handoff có thể xác nhận.
- **Error/exception:** Không có business/API error. Login return-to-resource behavior và các destination chưa được app shell xác định.

### `GS07-EV-07` — Local hand-off state simulator

- **Loại và trigger:** `Click`; activate một trong sáu tab #18–#23.
- **Precondition:** `code.html` đã render và inline `switchHandOffState(state)` tồn tại.
- **Input:** Một trong sáu literal `loading`, `gated`, `ready`, `403`, `404`, `expired`; không có resource ID, API response hoặc user permission input.
- **Processing:** Hàm xóa class selected khỏi `.state-tab`, thêm selected class cho tab có ID `tab-${state}`, rồi ghi hard-coded title/description/code vào #24. Nó không gọi fetch/XHR/API, không thay đổi disabled state của toolbar/download và không dựng viewer. Click `gated` ghi `423 Locked / DESIGN_ONLY`, trong khi initial screenshot ghi `423 Locked / 501 Blocked Implementation`. `ready` text sample nêu `signed_url`/`expires_in:3600`, còn `403/404/expired` samples ghi code/status không khớp #12 source/catalog.
- **Output:** Chỉ text/class của state inspector thay đổi. Không có network response, preview, download hay access decision.
- **Error/exception:** Không có API error. Switch không có default branch cho state lạ; UI chỉ expose sáu literal trên. Mọi status/code trong tab là sample hand-off, không phải runtime mapping.

### `GS07-EV-08` — Footer navigation

- **Loại và trigger:** `Click/Anchor`; activate một trong bốn footer links trong #26.
- **Precondition:** Footer anchor hiển thị và được activate.
- **Input:** `href="#"` cùng metadata `data-path` tĩnh; không có route params.
- **Processing:** Browser theo empty fragment; không router/API call.
- **Output:** Không có supported destination hoặc session/resource state change.
- **Error/exception:** Không có business/API error; destination/return behavior chưa được xác định.

### API #12 request/response và error mapping

| Chủ đề | Declared contract / expected | Current source evidence |
|---|---|---|
| Method/path | `GET /api/v1/resources/{resource_id}`; `resource_id:int64` required; no query/body; public/no Bearer. | Route compose trong `app/api/v1.py`, raw string path để custom validator ánh xạ invalid ID thành 404; không có Authorization dependency. |
| Success | `ApiEnvelope<Resource>`; catalog/API DD liệt kê `id/name/type/url/visibility/lesson_id`; 200 `DESIGN_RESOURCE_RETRIEVED`. | Current `ResourceDetail` trả `id/name/type/url/lesson_id`; `url` nullable trong model và lấy direct từ DB; query/response không có `visibility`. |
| Not found | Declared 404 `DESIGN_RESOURCE_NOT_FOUND`. | Invalid/non-positive/overflow ID, resource missing, hoặc parent check fail trả cùng 404/code. Parent check chỉ chạy nếu `lesson_id` khác null. |
| Internal failure | Declared 500 `DESIGN_INTERNAL_ERROR`. | SQLAlchemy query error rollback và trả safe 500; Pydantic mapping error trả safe 500. |
| Access and URL | AC-06 yêu cầu public-or-authorized, 403 khi không có quyền, và Object Storage signed URL cho private resource. | Current route không auth; không visibility/enrollment check, không signer; trả direct `resources.url`. Không có current 403/410/expiry contract. |
| API DD/runtime label | API DD #12 `Draft — Needs Confirmation`; có dòng `RUNTIME_STATUS: ... DECLARED_NOT_RUNNABLE`. | `v1.py` compose #12 và test source tồn tại; đây là documentation/source discrepancy về local composition. Test source không được chạy; production/deployment/browser runtime vẫn chưa xác minh. |

Catalog, API DD và current source không hoàn toàn cùng một mức bảo đảm. `resources.url`/`lesson_id` của legacy DDL khác nullable flags của model/contract; V1-PILOT DDL không có generic `resources` table. Live schema vẫn chưa xác minh.

### Trích từ DD nguồn: E. Ma trận trạng thái, điều hướng và khả năng tiếp cận

| State | Nguồn/điều kiện | UI xử lý có thể xác nhận / cần chốt |
|---|---|---|
| Initial/Gated | Initial screenshot/HTML | Viewer trống, controls disabled, `ACCESS_UNRESOLVED`; prototype-only. |
| Loading | State tab | Text mô tả shimmer/busy; không có skeleton thật, aria-busy runtime hoặc request. |
| Ready | State tab | Text mẫu 200/signed URL; không mở preview, không enable download. Cần access/URL/type policy trước khi triển khai. |
| Forbidden | State tab / AC-06 expected | Simulator 403; API #12 hiện không emit 403. UX/copy/login/recovery còn mở. |
| Not found | State tab / API source current | #12 404 `DESIGN_RESOURCE_NOT_FOUND`; simulator dùng code khác. Mapping SH-06/inline 404 chưa chốt. |
| Link expired | State tab / AC/prototype expected | Simulator 410/401; API #12 không có expiry field/status/refresh flow. |
| Internal/service error | API #12 current source | 500 `DESIGN_INTERNAL_ERROR`; prototype không có tab. Client display/retry behavior chưa được chỉ định. |
| Unsupported/null URL | Model allows nullable URL; type policy absent | Không có current UI state; không đoán preview, fallback hoặc copy. Cần contract. |

### Điều hướng và dữ liệu bàn giao

- **Entry:** GS-06 chọn resource → `resourceId`; ST-12 có thể gửi cùng ID kèm `lessonId`, nhưng ST-12/API #26 cardinality và return semantics còn mở. Route `resourceId` không thể hiện entry source.
- **Return:** mockup ghi GS-06; ST-12 context có thể cần quay lại bài học. Cần quyết định destination/history behavior và các ID được giữ.
- **404:** API #12 current 404 có nhiều nguyên nhân (invalid ID, resource missing, parent lesson/course check). SH-06 hiện gắn với #08; không điều hướng sang SH-06 cho #12 tới khi error ownership/copy được chốt.
- **URL:** `data.url` là direct URL theo source, không phải signed URL. Không ghi vào mock cache hoặc tự mở tab trước khi policy được xác nhận.

### Responsive, accessibility và riêng tư

- Screenshot là desktop prototype 1588×1600. Prototype tải font Plus Jakarta Sans và Tailwind CSS từ CDN, dùng cobalt `#004ac6/#2563eb` và max-width 1440px; Study Web guide yêu cầu Inter/system, không thêm remote font, semantic ocean tokens và content width khoảng 1120px.
- Header nav dùng `hidden md:flex` mà không có mobile-menu replacement. Zoom controls là 32×32px và disabled, trong khi guide yêu cầu controls tối thiểu 44px. Status dot có `animate-pulse`; prototype không có reduced-motion override.
- WCAG contrast badge và security copy là static claims. Contrast, focus-visible, keyboard order, reflow, browser zoom và touch targets chưa được audit theo composed states; đây là design discrepancy, không phải runtime measurement.
- Khi implement, yêu cầu keyboard focus, accessible names/status announcements, touch targets và contrast phải được đo theo `.agents/web-study/design.md`/accessibility policy hiện hành. Đây là điều kiện thiết kế, không phải kết quả hiện tại.
- Safe-release copy yêu cầu không lộ bucket/path/file size/expiry; current API trả `url` trực tiếp. Chưa thể xác nhận điều đó không tiết lộ storage origin; cần URL contract và allowlist.

## 4. Luồng đọc (Read)
- Orchestration từ inventory: GET #12 tại thời điểm mở; không cache signed URL vô hạn hoặc lộ internal storage key.
- Chi tiết current/source mapping: xem [API Integration](04-api-integration.md) và DD nguồn.

## 5. Luồng ghi (Write)
- Chỉ mô tả mutation được DD/API source nêu; không thêm endpoint hoặc side effect.
- Source trace: [GS-07](../../screen_stitch/02_guest_discovery/GS-07_xem-tai-tai-nguyen/GS-07.md)

## 6. Cache / concurrency / lifecycle
- Cache, race, cleanup, pagination: xem các section source bên dưới; nếu không có bằng chứng thì để `CẦN_XÁC_NHẬN`.

## 7. Data errors & security
- Theo error/security/source-status section của DD nguồn; không coi state trong mockup là runtime behavior.

## 8. Trace
[Events](02-events.md) · [API](04-api-integration.md) · [Rules](05-business-rules.md)
