# ST-23 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [ST-23_markers.json](../../screen_stitch/03_student/ST-23_danh-sach-thao-luan/ST-23_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `ST-23-EL-001` | `ST23-EL-01` | Study2Work brand/logo |
| #2 | `ST-23-EL-002` | `ST23-EL-02` | Primary Student navigation |
| #3 | `ST-23-EL-003` | `ST23-EL-03` | Institution breadcrumb bar |
| #4 | `ST-23-EL-004` | `ST23-EL-04` | Page breadcrumb |
| #5 | `ST-23-EL-005` | `ST23-EL-05` | Page heading |
| #6 | `ST-23-EL-006` | `ST23-EL-06` | Empty-state card |
| #7 | `ST-23-EL-007` | `ST23-EL-07` | Empty-state icon |
| #8 | `ST-23-EL-008` | `ST23-EL-08` | Empty-state heading |
| #9 | `ST-23-EL-009` | `ST23-EL-09` | Empty-state explanatory copy |
| #10 | `ST-23-EL-010` | `ST23-EL-10` | Return-to-courses link |
| #11 | `ST-23-EL-011` | `ST23-EL-11` | Footer brand and description |
| #12 | `ST-23-EL-012` | `ST23-EL-12` | Footer program links |
| #13 | `ST-23-EL-013` | `ST23-EL-13` | Footer community/support links |
| #14 | `ST-23-EL-014` | `ST23-EL-14` | Footer contact information |
| #15 | `ST-23-EL-015` | `ST23-EL-15` | Copyright and legal links strip |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Đặc tả chi tiết element

`screen_annotated.png` annotates `screen_rendered.png`; `x/y` trong JSON là target coordinates trên HTML render. Tất cả các element nhìn thấy là static prototype values, không có data binding. State chung: rendered/default only; hover/focus/pressed/disabled/loading/success/error, keyboard behavior, accessible name và responsive behavior không được chứng minh bởi asset, cần theo Study Web design guide khi frontend được thiết kế. Expected elements vắng mặt được liệt kê ở A.5, không có marker.

| Element ID / marker | Element, loại, vị trí/mục đích | Thuộc tính, nguồn, visibility/state/validation | Event |
|---|---|---|---|
| ST23-EL-01 | Study2Work logo/brand; header trái | Static logo/text; anchor `href="#"`; không có route target được wire. | EV-09 |
| ST23-EL-02 | Primary Student nav: Tổng quan, Khóa học của tôi, Diễn đàn/Thảo luận; header | Ba static anchors; forum tab active trong prototype; links `#`, không có destination/session guard runtime. | EV-09 |
| ST23-EL-03 | Upper institutional breadcrumb bar | Home icon + “Cổng Học Viên Study2Work”; home anchor `#`; text không từ API #39. | EV-09 |
| ST23-EL-04 | Page breadcrumb Trang chủ > Diễn đàn & Thảo luận | Static text/anchors `#`; không giữ course context hoặc return URL. | EV-09 |
| ST23-EL-05 | H1 “Danh sách thảo luận” | Static page title; không có course title/API field binding. Visible trong render. | — |
| ST23-EL-06 | Empty-state container/card; main center | White surface, static layout; điều kiện thực để render chưa được chứng minh. Không map network/auth failure thành empty. | EV-03 |
| ST23-EL-07 | Empty-state decorative discussion icon | Icon `question_answer`; decorative, no data/interaction. Render state only. | — |
| ST23-EL-08 | Empty-state heading “Chưa có chủ đề thảo luận để hiển thị.” | Static HTML copy; không chứng minh backend đã trả `items=[]`. | EV-03 |
| ST23-EL-09 | Empty-state message về chưa có thảo luận/đang đồng bộ | Static copy; trạng thái sync không có API/worker source. | EV-03 |
| ST23-EL-10 | “Quay lại khóa học của tôi” link/button | Anchor target `/student/courses`; maps by inventory to ST-08 route proposal; accessible visual is static; role/return behavior not wired. | EV-09 |
| ST23-EL-11 | Footer brand/logo và mô tả | Static Study2Work LMS text/logo/copy; no API source or verified home destination. | EV-09 |
| ST23-EL-12 | Footer “Chương trình” links | Static program links; one course link `/student/courses`, other links `#`; destinations not wired/verified. | EV-09 |
| ST23-EL-13 | Footer “Cộng đồng & Hỗ trợ” links | Static forum/mentor/help labels; hrefs `#`; no service routes or support API. | EV-09 |
| ST23-EL-14 | Footer office address/phone/email | Static contact text; no authoritative config/API source in ST-23. | — |
| ST23-EL-15 | Copyright strip/legal links | Static copyright and legal anchors, mostly `#`; legal routes not established here. | EV-09 |

**Expected nhưng không có marker/source visual:** course selector/filter, sort selector, create-topic action, discussion rows/cards, author/avatar/time/count/status, pagination/page-size controls, loading skeleton, populated state, filter-empty state and error state. They require product-approved design; no element properties/validation defaults are inferred.

## 4. Conditional UI & state variations
- States theo inventory: loading/empty/ready/error
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/03_student/ST-23_danh-sach-thao-luan/ST-23.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
