# GS-03 — Chi tiết khóa học · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `GS-03` |
| Module | Guest / Discovery |
| Route | `/courses/:courseId` — Guest router source maps this route to GS03Page; browser runtime chưa xác minh |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD / implementation / runtime status | `DD BLOCKED` — loaded design and AC-05/F02 orchestration remain unresolved. `PARTIAL SOURCE-WIRED` — GS03 #08 detail 404 routes to SH-06; GS04/#09 and GS05/#10 load after the selected tab and published-course gate; enrollment remains unavailable. `STUB-BROWSER-VERIFIED` — prior local stub render only; live API/DB/deployment unverified. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.2 / 2026-11-17 |
| Nguồn đối chiếu | [GS-03.md](../../screen_stitch/02_guest_discovery/GS-03_chi-tiet-khoa-hoc/GS-03.md), [GS-03_PLAN.md](../../screen_stitch/02_guest_discovery/GS-03_chi-tiet-khoa-hoc/GS-03_PLAN.md), [GS-03_markers.json](../../screen_stitch/02_guest_discovery/GS-03_chi-tiet-khoa-hoc/GS-03_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Thông tin khóa học, mentor, giá, tab đề cương/đánh giá, CTA ghi danh.
- In-scope: GET #8 để xác định published → lazy GET #9 và #10 theo tab; course ID thống nhất.
- Out-of-scope: Xem gate bên dưới; source wiring không chứng minh browser/live runtime hoặc approval của loaded UI.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-05 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Thông tin khóa học, mentor, giá, tab đề cương/đánh giá, CTA ghi danh. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #08, #09, #10
- Liên kết màn hình dự kiến: [GS-04](../GS-04-DeCuongKhoaHoc/00-overview.md), [GS-05](../GS-05-DanhGiaVaThaoLuanCongKhai/00-overview.md), [GS-06](../GS-06-TaiNguyenKhoaHoc/00-overview.md), [ST-04](../ST-04-KiemTraGhiDanhTruocDangKy/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | loading/course-404/partial-tab-error |
| Current source/runtime | Guest router, GS03Page, GS05Page, API_010, specs and T021 browser evidence | GS03/#08, GS04/#09 and GS05/#10 source-wired locally; tests/build pass; browser used a temporary stub; live API/DB/deployment `NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [GS-03 source screen.png](../../screen_stitch/02_guest_discovery/GS-03_chi-tiet-khoa-hoc/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/02_guest_discovery/GS-03_chi-tiet-khoa-hoc/screen_annotated.png))
- Luồng: GET #8 để xác định published → lazy GET #9 và #10 theo tab; course ID thống nhất.
- Priority: P1; Gate/source status: **#08/#09/#10 SOURCE-WIRED LOCALLY; enrollment unavailable**; **PARTIAL SOURCE:** GS03 calls #08, then lazy #09 for curriculum or GS05/#10 for reviews after #08 confirms PUBLISHED. **BLOCK:** #08 singleton Page<Course>/LEFT JOIN differs from API DD; AC-05 eager/aggregate differs from F02 lazy; #10 title/rating/visibility/query gates remain Draft; G-01 enrollment; loaded design approval and live runtime/schema remain open.

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; source/runtime chưa được xác minh.
- 2026-11-17 — T021 enabled GS05/#10 as a bounded source-wired tab; 12/12 focused GS03/GS05 specs and full Study Web 153/153 pass; local desktop/mobile browser render used an in-memory API stub.

## Trạng thái và ranh giới bằng chứng

# GS-03 — Chi tiết khóa học

> **DD status:** `DD BLOCKED` — source HTML does not define the loaded detail UI or resolve the API orchestration conflicts.
> **Implementation status:** `PARTIAL SOURCE-WIRED` — GS03/#08 detail 404 routes to SH-06; GS04/#09 and GS05/#10 are wired locally after the published-course check; loaded detail/tab views are derived and enrollment remains unavailable.
> **Runtime status:** `STUB-BROWSER-VERIFIED; LIVE RUNTIME NOT VERIFIED` — focused/full tests and build pass; desktop/mobile browser render used an in-memory stub, with no live API/DB/deployment verification. T015 integrates GS04; T021 integrates GS05 as GS03-owned tabs.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID / tên | GS-03 — Chi tiết khóa học (Page) |
| Mục tiêu | Cho Guest xem thông tin của một khóa học đã xuất bản, mentor, giá và mở các tab đề cương/đánh giá; inventory còn yêu cầu CTA ghi danh. Các phần loaded này chưa có thiết kế/handler trong source HTML hiện có. |
| Actor | `Guest` theo AC-05. Link đăng nhập/đăng ký có trong HTML tĩnh. |
| Route | `/courses/:courseId` được Guest router ánh xạ tới GS03Page. API catalog khai báo `course_id:int64`; #08/#09 backend validators enforce signed-int64 bounds, client giữ route ID dạng string. |
| API tham chiếu | #08 detail and #09 curriculum are source-backed; #10 backend route/module/tests and Web `API_010`/GS05 caller are source-wired locally, while API #10 DD remains Draft. GS03 does not call #15. |
| Màn hình liên quan | GS-01/GS-02 là nguồn điều hướng vào detail; GS-04 curriculum, GS-05 reviews, GS-06 resources là tab liên quan; ST-04 là điểm tiếp theo được đề xuất cho ghi danh. Route/state handoff của các màn hình này chưa được runtime xác minh. |
| Điều kiện truy cập | Expected: route chứa course ID hợp lệ và #08 xác nhận course `PUBLISHED`. HTML hiện tại không đọc route hay kiểm tra quyền. #08/#09 là public và chỉ trả course/lessons `PUBLISHED`. |
| Kết quả truy cập | Expected: detail và tab data theo contract được xác nhận; hiện tại chỉ có empty/unavailable state tĩnh. Không có dữ liệu nào được cache hoặc lưu bởi HTML. |

### Expected behavior và current behavior

| Expected theo inventory/AC | Current source trong checkout |
|---|---|
| Hiển thị course detail, mentor, price và CTA ghi danh. | Không có course data, mentor, giá hoặc CTA trong `code.html`. |
| Dùng #08 để xác định course PUBLISHED; tab curriculum/reviews tải lười theo tab theo F02. | `code.html` là static asset không có handler. Current Angular GS03Page gọi #08; `?tab=curriculum` gọi #09 lazy sau #08. AC-05 vẫn mô tả tuần tự #08 → #09 → #10 trước khi render; discrepancy chưa được Product/BE giải quyết. |
| Có trạng thái loading, course-404 và partial-tab-error theo inventory. | HTML chỉ có một thông báo “Thông tin khóa học hiện chưa có sẵn.”; không có loading/error variants. |
| #09 cung cấp curriculum; #10 current source supplies public discussion content. | GS03 calls #09 for curriculum and mounts GS05/#10 for reviews. #10 returns `title: null` and no rating/aggregate; DD/source-schema conflicts remain unresolved. |

### Tài sản thiết kế

- [Ảnh nguồn `screen.png`](../../screen_stitch/02_guest_discovery/GS-03_chi-tiet-khoa-hoc/screen.png) được giữ nguyên, SHA-256 `94360a8b1b1a9bbe0cdc110f6c243ce5aaabd8b6923331c5667421cb1c37d34d`; 1280×1024, gần như trắng và không đọc được thành phần UI.
- [Ảnh render thay thế `screen_rendered.png`](../../screen_stitch/02_guest_discovery/GS-03_chi-tiet-khoa-hoc/screen_rendered.png) được tạo từ HTML gốc nguyên trạng bằng Firefox headless, 1440×1200. Ảnh render cho thấy đầy đủ header, breadcrumb, title, tab, empty panel và footer. Đây là bản render của prototype tĩnh, không phải runtime screenshot.
- [Ảnh có đánh số `screen_annotated.png`](../../screen_stitch/02_guest_discovery/GS-03_chi-tiet-khoa-hoc/screen_annotated.png) dựa trên `screen_rendered.png`; 10 marker ở gutter, không che nội dung.
- [Bản đồ marker `GS-03_markers.json`](../../screen_stitch/02_guest_discovery/GS-03_chi-tiet-khoa-hoc/GS-03_markers.json) là nguồn tọa độ/thứ tự và ánh xạ element.
- [Kế hoạch GS-03](../../screen_stitch/02_guest_discovery/GS-03_chi-tiet-khoa-hoc/GS-03_PLAN.md) ghi expected/current behavior, trace và blocker trước khi tạo ảnh/DD.
- [`code.html`](../../screen_stitch/02_guest_discovery/GS-03_chi-tiet-khoa-hoc/code.html) được giữ nguyên; SHA-256 `d4f4bfdb56324b7c96589af75362903a491a3f565c97152b63634573c9d69619`.

`code.html` tải Tailwind và Google Fonts từ CDN. `.agents/web-study/design.md` là hướng dẫn đích yêu cầu không phụ thuộc font từ xa; do đó prototype này chưa chứng minh tuân thủ UI standard của Study2Work.

### T024 current source update (2026-11-17)

- The root app wildcard clears the unmatched path/query and redirects to SH-06. GS-03 API #08 detail 404 routes to SH-06 with `replaceUrl`, without forwarding the course ID or error body.
- API #08 500/network and API #09 curriculum 404 remain separate. Focused tests passed; broader build/runtime evidence is tracked in T024.
