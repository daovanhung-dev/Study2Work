# GS-04 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `GS-04-EV-001` | `GS04-EV-01` / `GS04-EV-01` — Mở query tab và tải curriculum (partial source wired) | See source event detail below |
| `GS-04-EV-002` | `GS04-EV-02` / `GS04-EV-02` — Map danh sách khi #09 trả lesson (expected; access blocker) | See source event detail below |
| `GS-04-EV-003` | `GS04-EV-03` / `GS04-EV-03` — Empty curriculum | See source event detail below |
| `GS-04-EV-004` | `GS04-EV-04` / `GS04-EV-04` — #09 thất bại | See source event detail below |
| `GS-04-EV-005` | `GS04-EV-05` / `GS04-EV-05` — Trở về GS-03 cùng `courseId` | See source event detail below |
| `GS-04-EV-006` | `GS04-EV-06` / `GS04-EV-06` — Header/footer anchor navigation | See source event detail below |
| `GS-04-EV-007` | `Source heading` / Lesson-open interaction — chưa được đặc tả hoặc triển khai | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: E. Event và xử lý

### `GS04-EV-01` — Mở query tab và tải curriculum (expected; partial source wired)

| Thuộc tính | Đặc tả |
|---|---|
| Trigger / input | Chọn GS04 trong GS03 hoặc direct-entry tới `/courses/:courseId?tab=curriculum`; `courseId` là path segment. Current direct-entry first requests #08; no #08 cache exists. |
| Guard / validation | API catalog khai báo `course_id:int64`; current route nhận `str`, rồi #09 validator gọi shared `parse_integer` và enforce signed-int64 bounds. Malformed/out-of-range ID trả 404 `DESIGN_RESOURCE_NOT_FOUND`; source tests cover inclusive bounds and out-of-range cases. Client giữ ID dưới dạng string. |
| Request | After #08 succeeds, GS03-local service calls `GET /api/v1/courses/{course_id}/curriculum`; public, no Bearer/body/query. No client cache/retry is implemented. |
| Processing | Backend query Q1 confirms course exists and is `PUBLISHED`; Q2 selects published lessons ordered by `sort_order ASC, id ASC`. Client maps title/order only. |
| Output | Current panel renders loading/ready/empty/not-found/error. Ready rows expose order/title only; no content/video or lesson action. This is derived UI, not an approved loaded design. |
| Error / side effect | 404 `DESIGN_RESOURCE_NOT_FOUND`; 500 `DESIGN_INTERNAL_ERROR`. GET không mutate DB. Không có retry/timeout/cache recovery behavior đã xác nhận. |

### `GS04-EV-02` — Map danh sách khi #09 trả lesson (expected; access blocker)

| Thuộc tính | Đặc tả |
|---|---|
| Trigger / input | `GS04-EV-01` trả HTTP 200, `data.items` có phần tử. API item hiện có `id`, `course_id`, `title`, `content`, `video_url`, `order`, `status`. |
| Processing | Backend already orders by `order` (`sort_order`) then `id`; GS03 mapper copies only title/order and preserves response order. |
| Access rule | Không cho Guest mở private lesson theo inventory. Nhưng API #09 current query chỉ filter `PUBLISHED`, DD gọi đó là assumption, response không có `is_preview`/permission. Do đó chưa thể quyết định lesson nào có thể mở hoặc có thể render content/media. |
| Output / error | Current derived list renders metadata only. No #22–#24/ST-10 or lesson/media action is called from Guest. Approved loaded-list/access design remains blocked. |

### `GS04-EV-03` — Empty curriculum

| Thuộc tính | Đặc tả |
|---|---|
| Input / trigger | #09 trả HTTP 200 với `success=true`, `businessCode=DESIGN_RESOURCE_RETRIEVED`, `data.items=[]`; pagination hiện tại `page=1,size=0,total=0,total_pages=0`. |
| Processing | Xác nhận successful envelope và empty `items`; cập nhật curriculum view sang `EMPTY`, tách khỏi lỗi. Không gọi thêm API hoặc tạo lesson placeholder. |
| Output | Current panel shows `Chưa có nội dung đề cương để hiển thị.` after a successful empty response; copy/layout approval remains open. |
| Recovery / error / side effect | Không có mutation. Không có refresh/retry control trong source; network/API failure thuộc EV-04, không được map thành `EMPTY`. |

### `GS04-EV-04` — #09 thất bại

| Input / trigger | API trả 404 `DESIGN_RESOURCE_NOT_FOUND` cho parse failure/missing/unpublished course; 500 `DESIGN_INTERNAL_ERROR` cho DB/mapping failure. Transport error không có current source. |
| Processing | Đọc HTTP status và business code; tách 404 thành `NOT_FOUND`, 500/transport failure thành error state. Không chuyển 404 thành 403 hoặc empty state. |
| Output expected | State `NOT_FOUND` for 404, or safe service error for 500/transport; approved copy/retry behavior remains open. |
| Current behavior / side effect | GS03 maps 404 separately from other errors; GET is read-only. Angular test covers 404/500, but browser/live runtime is not verified. |

### `GS04-EV-05` — Trở về GS-03 cùng `courseId`

| Thuộc tính | Đặc tả |
|---|---|
| Element / trigger | Breadcrumb element #3 “Chi tiết khóa học” hoặc CTA #8. |
| Input | Same `courseId` in GS03; no form data or request body. |
| Processing | Select the Overview tab to return to detail; it clears only the `tab` query parameter, preserves other query parameters, and makes no new API call. |
| Expected output | `/courses/:courseId` for the same course; back-stack behavior is not specified. |
| Current behavior / error | Angular tab query is wired; static HTML anchors still use `href="#"` and do not prove app routing. |

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
