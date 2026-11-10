# GS-04 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `GS-04-EV-001` | `GS04-EV-01` / `GS04-EV-01` — Mở route và tải curriculum (expected; chưa wired) | See source event detail below |
| `GS-04-EV-002` | `GS04-EV-02` / `GS04-EV-02` — Map danh sách khi #09 trả lesson (expected; access blocker) | See source event detail below |
| `GS-04-EV-003` | `GS04-EV-03` / `GS04-EV-03` — Empty curriculum | See source event detail below |
| `GS-04-EV-004` | `GS04-EV-04` / `GS04-EV-04` — #09 thất bại | See source event detail below |
| `GS-04-EV-005` | `GS04-EV-05` / `GS04-EV-05` — Trở về GS-03 cùng `courseId` | See source event detail below |
| `GS-04-EV-006` | `GS04-EV-06` / `GS04-EV-06` — Header/footer anchor navigation | See source event detail below |
| `GS-04-EV-007` | `Source heading` / Lesson-open interaction — chưa được đặc tả hoặc triển khai | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: E. Event và xử lý

### `GS04-EV-01` — Mở route và tải curriculum (expected; chưa wired)

| Thuộc tính | Đặc tả |
|---|---|
| Trigger / input | Điều hướng từ GS-03 hoặc direct-entry tới route đề xuất; `courseId` là path segment, tab là `curriculum`. Inventory đề xuất giữ #08 từ cache. |
| Guard / validation | API catalog khai báo `course_id:int64`; current route nhận `str` và shared `parse_integer` chỉ kiểm tra integer syntax, không enforce signed int64/positive range. Parse failure thành 404 `DESIGN_RESOURCE_NOT_FOUND`; oversized path chưa được test/runtime xác minh. Client path validation chưa tồn tại. |
| Request | `GET /api/v1/courses/{course_id}/curriculum`; public, không Bearer/body/query theo route hiện tại. Cache lookup/call order phụ thuộc policy chưa chốt; không giả định miss fallback hoặc cache TTL. |
| Processing | Backend query Q1 xác nhận course tồn tại và `PUBLISHED`; Q2 lấy lesson cùng course `PUBLISHED`, order `sort_order ASC, id ASC`. Client chưa có code. |
| Output | Loading → ready/empty theo response, sau khi thiết kế được duyệt. Với ready, `order` là thứ tự hiện tại. Không render `content`/`video_url` trong Guest UI trước khi preview/access projection được chốt. |
| Error / side effect | 404 `DESIGN_RESOURCE_NOT_FOUND`; 500 `DESIGN_INTERNAL_ERROR`. GET không mutate DB. Không có retry/timeout/cache recovery behavior đã xác nhận. |

### `GS04-EV-02` — Map danh sách khi #09 trả lesson (expected; access blocker)

| Thuộc tính | Đặc tả |
|---|---|
| Trigger / input | `GS04-EV-01` trả HTTP 200, `data.items` có phần tử. API item hiện có `id`, `course_id`, `title`, `content`, `video_url`, `order`, `status`. |
| Processing | Sắp xếp đã được backend thực hiện theo `order` (`sort_order`) rồi `id`; client không nên đổi thứ tự. Chỉ map metadata cần thiết sau khi field/display policy được phê duyệt. |
| Access rule | Không cho Guest mở private lesson theo inventory. Nhưng API #09 current query chỉ filter `PUBLISHED`, DD gọi đó là assumption, response không có `is_preview`/permission. Do đó chưa thể quyết định lesson nào có thể mở hoặc có thể render content/media. |
| Output / error | Loaded list UI chưa có design/source; event là expected contract, chưa tồn tại trong app. Không gọi #22–#24/ST-10 từ Guest. Blocked cho tới khi BE/Product chốt projection, preview/access rule và interaction. |

### `GS04-EV-03` — Empty curriculum

| Thuộc tính | Đặc tả |
|---|---|
| Input / trigger | #09 trả HTTP 200 với `success=true`, `businessCode=DESIGN_RESOURCE_RETRIEVED`, `data.items=[]`; pagination hiện tại `page=1,size=0,total=0,total_pages=0`. |
| Processing | Xác nhận successful envelope và empty `items`; cập nhật curriculum view sang `EMPTY`, tách khỏi lỗi. Không gọi thêm API hoặc tạo lesson placeholder. |
| Output | Empty-state UI sau khi copy/layout được duyệt. HTML có empty-like card/copy nhưng không được ràng buộc với response này cho tới khi UI được nối. |
| Recovery / error / side effect | Không có mutation. Không có refresh/retry control trong source; network/API failure thuộc EV-04, không được map thành `EMPTY`. |

### `GS04-EV-04` — #09 thất bại

| Input / trigger | API trả 404 `DESIGN_RESOURCE_NOT_FOUND` cho parse failure/missing/unpublished course; 500 `DESIGN_INTERNAL_ERROR` cho DB/mapping failure. Transport error không có current source. |
| Processing | Đọc HTTP status và business code; tách 404 thành `NOT_FOUND`, 500/transport failure thành error state. Không chuyển 404 thành 403 hoặc empty state. |
| Output expected | State `NOT_FOUND` hoặc `SERVICE_ERROR`; thiết kế copy, route recovery, retry và network-error behavior chưa có. |
| Current behavior / side effect | Không có handler/error UI trong `code.html`; GET read-only, chưa có Study Web runtime để xác nhận. |

### `GS04-EV-05` — Trở về GS-03 cùng `courseId`

| Thuộc tính | Đặc tả |
|---|---|
| Element / trigger | Breadcrumb element #3 “Chi tiết khóa học” hoặc CTA #8. |
| Input | Cùng `courseId` của route GS-04; không có form data hoặc request body. Current HTML href không mang ID. |
| Processing | Sau khi route/back behavior được duyệt, điều hướng về detail cùng `courseId`; không gọi API hoặc thay đổi server data. Không tự quyết định giữ history hay tab query. |
| Expected output | `/courses/:courseId` cho cùng course; preserve query/back-stack behavior cần quyết định. |
| Current behavior / error | Cả hai anchor dùng `href="#"`; không có interpolation `courseId`, router hay history action. Route failure/back behavior chưa có UI handler. |

### `GS04-EV-06` — Header/footer anchor navigation

| Thuộc tính | Đặc tả |
|---|---|
| Input / trigger | Click anchor ở #1, #2, #3 hoặc #10; input là literal `href`, không có form/state payload. Brand #9 không phải link. |
| Processing | Browser xử lý anchor mặc định; không có API request hoặc local state mutation trong HTML. |
| Expected output | `/` (brand/home), `/courses` (course list), `/login` hoặc `/register` theo anchor được chọn. |
| Current behavior / error | Các path là literal trong HTML; Study Web router/session behavior, active state, return URL và route failure chưa được xác minh. |

### Lesson-open interaction — chưa được đặc tả hoặc triển khai

Không có lesson item hoặc trigger trong GS-04 source. Guest private lesson phải không mở được theo inventory. Không phát sinh `GS04-EV` mở bài, không gọi ST-10 APIs #22–#24, không phát media. Nếu yêu cầu preview được duyệt sau này, cần API projection/authorization contract và design rõ trước khi thêm event.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
