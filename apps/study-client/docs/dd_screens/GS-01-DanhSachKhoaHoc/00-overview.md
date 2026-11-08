# GS-01 — Danh sách khóa học · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `GS-01` |
| Module | Guest / Discovery |
| Route | `/courses` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **DD status:** `BLOCKED` — the supplied design covers only an empty catalog; the required loaded list, sort, count and paging surfaces have no approved layout. Category filtering and search handoff also conflict with current contracts.; **Implementation status:** `IMPLEMENTATION BLOCKED` · **Runtime status:** `RUNTIME NOT VERIFIED`. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [GS-01.md](../../screen_stitch/02_guest_discovery/GS-01_danh-sach-khoa-hoc/GS-01.md), [GS-01_PLAN.md](../../screen_stitch/02_guest_discovery/GS-01_danh-sach-khoa-hoc/GS-01_PLAN.md), [GS-01_markers.json](../../screen_stitch/02_guest_discovery/GS-01_danh-sach-khoa-hoc/GS-01_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Grid/list khóa học public; sort, paging, số kết quả, thao tác xem chi tiết.
- In-scope: GET #5 cache-first locale → GET #6 page=1,size=20; reset page sau sort/filter; không gửi category đến khi BE hỗ trợ.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-03 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Grid/list khóa học public; sort, paging, số kết quả, thao tác xem chi tiết. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #05, #06
- Liên kết màn hình dự kiến: [GS-02](../GS-02-TimKiemKhoaHoc/00-overview.md), [GS-03](../GS-03-ChiTietKhoaHoc/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | loading/empty/ready/query-error |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [GS-01 source screen.png](../../screen_stitch/02_guest_discovery/GS-01_danh-sach-khoa-hoc/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/02_guest_discovery/GS-01_danh-sach-khoa-hoc/screen_annotated.png))
- Luồng: GET #5 cache-first locale → GET #6 page=1,size=20; reset page sau sort/filter; không gửi category đến khi BE hỗ trợ.
- Priority: P0; Gate/source status: **R**; **BLOCK:** Category chỉ hiển thị metadata; filter category chưa hoạt động

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# GS-01 — Danh sách khóa học

> **DD status:** `BLOCKED` — the supplied design covers only an empty catalog; the required loaded list, sort, count and paging surfaces have no approved layout. Category filtering and search handoff also conflict with current contracts.
> **Implementation status:** `IMPLEMENTATION BLOCKED` · **Runtime status:** `RUNTIME NOT VERIFIED`.
> This document specifies the observable source and the expected flow separately. It does not certify a Study Web implementation.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: 1. Tổng quan màn hình

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID / tên | GS-01 — Danh sách khóa học |
| Surface / route | Page; `/courses` là route đề xuất trong inventory. Checkout hiện không có Study Web source, package manifest, router hoặc entrypoint để xác nhận route. |
| Mục tiêu | Cho Guest khám phá khóa học đã xuất bản, xem tổng số kết quả và điều hướng sang tìm kiếm hoặc chi tiết khóa học theo thiết kế đã duyệt. Danh sách tải và card design còn thiếu. |
| Actor / quyền | Guest / truy cập công khai theo AC-03 và route API #05/#06. Hai API hiện tại không yêu cầu Bearer token. Không có bằng chứng về client auth guard. |
| Điều kiện trước | Người dùng mở trang khám phá. Inventory AC-03 mô tả tiền điều kiện có khóa học public; API hiện vẫn trả danh sách rỗng hợp lệ khi không có khóa học. |
| Điều kiện sau | Expected: hiển thị metadata danh mục và một trang khóa học PUBLISHED, hoặc trạng thái rỗng/lỗi phù hợp. Current: chưa có frontend gọi API hoặc điều hướng. |
| API | #05 `GET /api/v1/categories`; #06 `GET /api/v1/courses`. Chỉ #06 cung cấp course list. Không gọi #07 từ GS-01 theo suy luận; #07 thuộc GS-02. |
| Màn hình liên kết | SH-01 → GS-01; tìm kiếm GS-02 (`/courses/search?q=`) và xem khóa học GS-03 (`/courses/:courseId`) là destination đề xuất. Header/footer còn đề xuất `/`, `/login`, `/register`. Không link nào hiện có route runtime. |
| Side effect | Đọc metadata và danh sách; không tạo/cập nhật dữ liệu nghiệp vụ. |
| Nguồn giao diện | [`screen.png`](../../screen_stitch/02_guest_discovery/GS-01_danh-sach-khoa-hoc/screen.png) là ảnh gốc 1280×1114, hiển thị trạng thái rỗng. [`code.html`](../../screen_stitch/02_guest_discovery/GS-01_danh-sach-khoa-hoc/code.html) là prototype tham khảo, không phải Study Web runtime. [`screen_annotated.png`](../../screen_stitch/02_guest_discovery/GS-01_danh-sach-khoa-hoc/screen_annotated.png) là ảnh đánh số; [`GS-01_markers_overlay.svg`](../../screen_stitch/02_guest_discovery/GS-01_danh-sach-khoa-hoc/GS-01_markers_overlay.svg) và [`GS-01_markers.json`](../../screen_stitch/02_guest_discovery/GS-01_danh-sach-khoa-hoc/GS-01_markers.json) lưu marker map. |

### Expected behavior

- Inventory GS-01 yêu cầu danh sách/grid khóa học public, sort, paging, số kết quả và thao tác xem chi tiết; luồng F02 quy định #05 cache-first theo locale rồi #06 với `page=1`, `size=20`, reset page sau sort/filter. Không gửi `category` đến khi backend hỗ trợ.
- AC-03 mô tả Guest xem danh sách theo filter/pagination. Hiện chưa có design được duyệt cho loaded state, sort selector, count, card hoặc pagination.
- Tìm kiếm là màn GS-02 và API #07. `list_screen.md` mô tả `q` trim/lowercase ở F02 GS-02; chưa có contract xác nhận GS-01 chuyển query khi submit.

### Current behavior

- Ảnh gốc chỉ có header, hai search input, empty-state illustration/copy và footer; không có category chip, loaded card, sort, count hoặc pagination.
- HTML giữ title/search/empty state. Các vùng filter/card/pagination chỉ là comment. Không có `<form>`, card markup, `fetch` hoặc navigation implementation. Anchor dùng `href="#"`.
- Script prototype tham chiếu các ID không có trong DOM (`btnResetFilter`, `filterLevel`, `filterFormat`, `filterPrice`, `filteredCount`) và lỗi trước khi gắn search handlers. Ý định cập nhật count giả 4/9 không phải kết quả API.
- HTML có header brand/nav markup không hiện trong PNG; có duplicate brand/navigation markup. Nó nạp Plus Jakarta Sans, Material Symbols và Tailwind CDN, lệch hướng dẫn Study dùng Inter/system và tránh remote font.
- API #05/#06 hiện có route/module/test source. `.agents/web-work/study/AGENTS.md` và `INDEX.md` tồn tại, được đăng ký `study-web: UNWIRED`; chúng mô tả việc thiếu editable app source/package và không chứng minh Study Web gọi API. Không có live DB hoặc môi trường triển khai evidence.
