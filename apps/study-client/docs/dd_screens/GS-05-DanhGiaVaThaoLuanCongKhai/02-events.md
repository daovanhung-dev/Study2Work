# GS-05 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `GS-05-EV-001` | `GS05-EV-01` / `GS05-EV-01` — Mở tab reviews và xác định course | See source event detail below |
| `GS-05-EV-002` | `GS05-EV-02` / `GS05-EV-02` — Tải page reviews bằng API #10 (declared, chưa runnable) | See source event detail below |
| `GS-05-EV-003` | `GS05-EV-03` / `GS05-EV-03` — Hiển thị review roots và replies (Draft projection only) | See source event detail below |
| `GS-05-EV-004` | `GS05-EV-04` / `GS05-EV-04` — Empty reviews | See source event detail below |
| `GS-05-EV-005` | `GS05-EV-05` / `GS05-EV-05` — Course not found/unpublished or reviews request failure | See source event detail below |
| `GS-05-EV-006` | `GS05-EV-06` / `GS05-EV-06` — Change review page (expected pagination; API not runnable) | See source event detail below |
| `GS-05-EV-007` | `GS05-EV-07` / `GS05-EV-07` — Trở về chi tiết khóa học cùng `courseId` | See source event detail below |
| `GS-05-EV-008` | `GS05-EV-08` / `GS05-EV-08` — Header/footer navigation | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: E. Event và xử lý

### `GS05-EV-01` — Mở tab reviews và xác định course

| Thuộc tính | Đặc tả |
|---|---|
| Event type / element | Route entry or tab-route change; expected route/query state owned by GS-03. No route control or listener exists in this HTML. |
| Trigger / input | Từ GS-03 chọn tab reviews hoặc direct-entry route proposal; input là path `courseId`, query `tab=reviews`, và optional #08 course value/cache từ GS-03. |
| Preconditions | Actor Guest theo inventory; expected course PUBLISHED. Catalog khai báo `course_id:int64`, nhưng current #08 route nhận `str` và shared parser không enforce signed-int64/positive bounds; GS-05 UI parser chưa tồn tại. Cache policy/direct-entry behavior chưa có contract. |
| Processing | 1) Đọc `courseId` từ route proposal; không có current UI parser. 2) Inventory nói reuse #08 từ cache; chỉ dùng cùng course ID nếu cache object tồn tại theo policy được duyệt. 3) Không tự đặt TTL/fallback nếu cache miss. 4) Chọn orchestration đã được Product/BE chốt: F02 lazy tab hay AC-05 eager sequence. |
| API / side effect | Không có current UI request. #08 current API là public GET/read-only; #10 hiện không có runtime route. |
| Output / error | Expected LOADING → review request khi prerequisite thỏa. Course 404 phải tách khỏi empty reviews. Current static screen luôn empty-like, không xử lý route/cache/API. |

### `GS05-EV-02` — Tải page reviews bằng API #10 (declared, chưa runnable)

| Thuộc tính | Đặc tả |
|---|---|
| Event type / element / precondition | Expected page-load GET after an approved tab activation/orchestration decision; no current tab control or handler is present. Requires same `courseId` and approved API #10 contract. |
| Trigger | Expected tab activation hoặc `GS05-EV-01`; không có control/handler trong HTML. |
| Input | `course_id:int64` path; optional `page:int32`. API catalog literal ghi thêm `rating filter?:string` nhưng không xác định physical query name/semantics. Không gửi `rating` cho tới khi contract xác nhận. `size` không nằm trong request contract. |
| Request declaration | `GET /api/v1/courses/{course_id}/reviews`; public, không Bearer/body. Catalog status: 200 `DESIGN_RESOURCE_RETRIEVED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 500 `DESIGN_INTERNAL_ERROR`. |
| Processing được Draft mô tả | Draft default `page=1`, min `page>=1` design-only; size cố định 20, review root query/count cùng scope, replies query theo review IDs. Status/page size/order/query behavior chưa có source runtime. Malformed page/rating không có declared 422 branch; semantics TBD. |
| Output dự kiến theo Draft | Common `ApiEnvelope<Page<Discussion>>`; đọc `data.items` và `data.pagination`. Empty `items=[]` vẫn là 200; non-empty mapping bị chặn bởi title/visibility contract gaps. |
| Runtime/error | Không có route/module/test #10 trong current checkout. Không thể xác minh HTTP response, retry, timeout, cache, request de-duplication hoặc deployment. |

### `GS05-EV-03` — Hiển thị review roots và replies (Draft projection only)

| Thuộc tính | Đặc tả |
|---|---|
| Event type / element | Expected response mapping; no loaded-list element exists in current HTML. |
| Trigger / precondition | #10 is approved and runnable, course gate has succeeded, and a valid HTTP 200 envelope contains non-empty `data.items`. This condition is not met by current runtime. |
| Input | Draft `data.items[]`: `id`, `course_id`, required `title`, `content`, `author{id,full_name,avatar_url?}`, `status`, `comments[]`; replies dự kiến có `id`, `discussion_id`, `content`, `author`, `created_at`. Đây là declared/Draft shape, chưa phải API runtime model. |
| Processing | 1) Check success envelope/business code. 2) Map review content/author and nest comments by the Draft `comments` array. 3) Keep `discussion_id` as parent identity if rendering a reply association. 4) Do not invent title from content. 5) Do not calculate or show rating/average. 6) Do not display root review timestamp; Draft response omits it. 7) Apply only approved moderation/public visibility rule; Draft `ACTIVE` filter is an assumption. |
| Output / errors / side effect | Expected READY list and pagination after approved projection; visual structure and ordering of replies/cards not present in design source. No mutation. If the response is malformed or lacks required title/access fields, no current client mapping/error behavior exists; implementation is blocked. Do not create a rating/error fallback. |
| Blockers | `discussions.title` source missing; no rating value/aggregate; public root/reply visibility and ordering not approved; no #10 executable source. |

### `GS05-EV-04` — Empty reviews

| Thuộc tính | Đặc tả |
|---|---|
| Event type / element / precondition | API success-state mapping after declared #10 returns HTTP 200 and a valid envelope for the same course; #6 is only static copy, not a current response-bound element. |
| Input / trigger | `data.items=[]`; API #10 Draft says `total=0`, `total_pages=0`. This is a declared empty branch, not verified runtime behavior. |
| Processing | Validate success envelope/business code and the empty array; keep it separate from #08/#10 course-not-found and from transport/server errors. Preserve the same course identity for the GS-03 return path. |
| Output / error | Expected `EMPTY`; current HTML's similar copy is not API-bound. If envelope/items are malformed, current GS-05 has no handler or error state. |
| Side effect / recovery | Read-only; no mutation. Refresh/retry behavior is unspecified and no such control exists in the asset. |

### `GS05-EV-05` — Course not found/unpublished or reviews request failure

| Thuộc tính | Đặc tả |
|---|---|
| Event type / element / trigger | API or transport failure mapping while resolving #08/#10; there is no current error panel or status listener. |
| Input / precondition | HTTP status/business code or network failure from the expected public-course/reviews request. #08 is source-backed; #10 error branches are catalog/Draft only. |
| Processing | Preserve course-gate errors as distinct from a valid empty review page; inspect status/code without inventing 403/422 or retry rules. |
| Output / side effect | Declared/current 404 or declared #10 500 may map to error states only after presentation is approved; GETs are expected read-only. No current UI output/handler exists. |
| Recovery / exception | Network timeout, retry, stale data and recovery destination have no approved rule; AC-05's 403 course branch conflicts with current #08 404 and #10's declared 404/500. |

The cases below separate current #08 source behavior from #10 declared behavior:

| Case | Source evidence / expected handling |
|---|---|
| Invalid/missing/unpublished course through #08 | Current #08 source returns HTTP 404 `DESIGN_RESOURCE_NOT_FOUND` for malformed path or no PUBLISHED course. Current fake-session test source covers invalid ID/missing course/404; tests were read, not run. |
| #10 draft course gate | API #10 Draft Q1 expects PUBLISHED course and 404 `DESIGN_RESOURCE_NOT_FOUND`; no runtime implementation verifies this. |
| #10 query/mapping failure | Catalog/Draft DD declares 500 `DESIGN_INTERNAL_ERROR`; no route/runtime behavior exists to verify. |
| Empty page | #10 Draft DD says 200 empty; do not map to 404. |
| Network timeout/retry | No policy in inventory, catalog, current source or approved DD; keep unspecified. |

Current HTML has no error state, status handler or retry action. AC-05 diagram includes an alternate `403` mention in course visibility branch, while current #08 returns 404 and API #10 catalog lists 404/500 only; record as discrepancy and don't add 403 to #10.

### `GS05-EV-06` — Change review page (expected pagination; API not runnable)

| Thuộc tính | Đặc tả |
|---|---|
| Event type / element / precondition | Expected change/select-page interaction; pagination control is absent from current HTML. It is valid only after #10 page semantics and the loaded-state design are approved. |
| Trigger / input | User selects a page (expected, no current trigger); input would be the selected page number and current `courseId`. |
| Validation | Draft #10 declares `page:int32`, default 1, min 1 design-only. Malformed page and out-of-range page semantics are not defined; no client clamp/reset behavior is approved. |
| Processing | If API becomes runnable and page contract is approved, request #10 for the selected page. Draft page size 20 and offset formula are design-only; client does not send `size`. |
| Output | Map response pagination metadata after validating success. Draft defines zero `total_pages` for empty. Current UI has no page state, URL synchronization, caching or request cancellation. |
| Errors | No declared 422 for malformed page; do not invent code. Preserve prior page results or clear them on failure only after product state policy is defined. |

### `GS05-EV-07` — Trở về chi tiết khóa học cùng `courseId`

| Thuộc tính | Đặc tả |
|---|---|
| Event type / element / precondition | Click/navigation from breadcrumb #3's course-detail anchor or CTA #7; requires a known current `courseId` and an approved return route. Current HTML contains both anchors but neither route nor ID binding. |
| Input / trigger | The same `courseId` carried from GS-03/current route; trigger is clicking “Chi tiết khóa học” or “Quay lại chi tiết khóa học”. No form payload. |
| Processing | Current browser behavior follows the literal `href="#"`; there is no router/history call. If approved later, construct `/courses/:courseId` with this same ID; preserve query/history behavior only after it is decided. |
| Output | Expected return to GS-03 detail for the same course. No API request or data mutation. |
| Error / exception | Missing ID, unknown route and back-stack behavior have no current handler or approved fallback; current placeholder does not complete the expected handoff. |

### `GS05-EV-08` — Header/footer navigation

| Thuộc tính | Đặc tả |
|---|---|
| Event type / element / precondition | Click/default-anchor navigation from #1, #2, #8, #9 and home/list anchors inside #3; an anchor must be selected. Footer brand #8 is also an anchor. |
| Input / trigger | The selected anchor's literal current `href` is `#`; labels are `Study2Work`, `Trang chủ`, `Khóa học`, `Đăng nhập`, `Đăng ký`. No user-entered or API data. |
| Processing | Browser default anchor behavior only; no API request, client state update, auth/session action or custom navigation code exists in the HTML. |
| Output | Current document/fragment behavior for `#`. Intended home, course list and auth destinations are not encoded by these links and remain unverified. |
| Error / exception | No application route-error, return-URL, focus-management or session-expiry handling exists; actual navigation behavior is unresolved with Study Web `UNWIRED`. |

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
