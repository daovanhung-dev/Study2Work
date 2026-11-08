# GS-07 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `GS-07-EV-001` | `Source heading` / Ma trận sự kiện | See source event detail below |
| `GS-07-EV-002` | `GS07-EV-01` / `GS07-EV-01` — Direct entry / load resource | See source event detail below |
| `GS-07-EV-003` | `GS07-EV-02` / `GS07-EV-02` — Thử zoom hoặc fullscreen | See source event detail below |
| `GS-07-EV-004` | `GS07-EV-03` / `GS07-EV-03` — Tải resource | See source event detail below |
| `GS-07-EV-005` | `GS07-EV-04` / `GS07-EV-04` — Quay lại resource list | See source event detail below |
| `GS-07-EV-006` | `GS07-EV-05` / `GS07-EV-05` — Breadcrumb | See source event detail below |
| `GS-07-EV-007` | `GS07-EV-06` / `GS07-EV-06` — Header navigation và auth links | See source event detail below |
| `GS-07-EV-008` | `GS07-EV-07` / `GS07-EV-07` — Local hand-off state simulator | See source event detail below |
| `GS-07-EV-009` | `GS07-EV-08` / `GS07-EV-08` — Footer navigation | See source event detail below |
| `GS-07-EV-010` | `Source heading` / API #12 request/response và error mapping | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

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

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
