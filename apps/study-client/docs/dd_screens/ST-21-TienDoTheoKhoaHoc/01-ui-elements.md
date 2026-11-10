# ST-21 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [ST-21_markers.json](../../screen_stitch/03_student/ST-21_tien-do-theo-khoa-hoc/ST-21_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `ST-21-EL-001` | `ST21-EL-01` | Study2Work brand and home link |
| #2 | `ST-21-EL-002` | `ST21-EL-02` | Primary navigation group: overview, my courses, active progress |
| #3 | `ST-21-EL-003` | `ST21-EL-03` | Breadcrumb trail |
| #4 | `ST-21-EL-004` | `ST21-EL-04` | Page title “Tiến độ theo khóa học” |
| #5 | `ST-21-EL-005` | `ST21-EL-05` | Page summary description |
| #6 | `ST-21-EL-006` | `ST21-EL-06` | Empty-state progress icon |
| #7 | `ST-21-EL-007` | `ST21-EL-07` | Empty-state heading |
| #8 | `ST-21-EL-008` | `ST21-EL-08` | Empty-state explanatory copy |
| #9 | `ST-21-EL-009` | `ST21-EL-09` | Return-to-overview button |
| #10 | `ST-21-EL-010` | `ST21-EL-10` | Footer brand and LMS name |
| #11 | `ST-21-EL-011` | `ST21-EL-11` | Footer policy and support links group |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Đặc tả chi tiết element

Marker đặt cạnh nhóm nội dung trong `screen_annotated.png`; `x/y` trong `ST-21_markers.json` là tọa độ target theo `screen_rendered.png`. Tất cả element dưới đây là HTML prototype tĩnh; không chứng minh route/runtime behavior.

| ID / Marker | Element, loại, vị trí | Data / thuộc tính / trạng thái | Event |
|---|---|---|---|
| ST21-EL-01 | Brand Study2Work/LMS Portal, logo và home link; header trái | Logo/text tĩnh; `href="#"` không xác nhận route trang chủ. Không có input. | EV-08 |
| ST21-EL-02 | Nhóm nav Tổng quan / Khóa học của tôi / Tiến độ; header | Ba anchor tĩnh; Tiến độ active trong prototype. Destination và role guard chưa wire. | EV-08 |
| ST21-EL-03 | Breadcrumb Trang chủ → Tiến độ → Tiến độ theo khóa học | Label tĩnh; anchor Tiến độ trỏ `/student/progress`; không có course ID được bind vào breadcrumb. | EV-07, EV-08 |
| ST21-EL-04 | Heading “Tiến độ theo khóa học” | Static h1; không đổi theo course title hoặc API data. Visible trong HTML render; không có trong PNG nguồn. | — |
| ST21-EL-05 | Mô tả “Xem chi tiết tỷ lệ hoàn thành, bài giảng và chứng chỉ theo từng khóa học của bạn.” | Static copy; không xác nhận chứng chỉ hoặc có field/metric tương ứng trong #37. | — |
| ST21-EL-06 | Icon empty progress (donut) trong card | Icon trang trí; không phải phần trăm/vòng tiến độ có data. | — |
| ST21-EL-07 | Tiêu đề empty state “Chưa có dữ liệu tiến độ cho khóa học này.” | Static copy trong HTML. Điều kiện thật để hiển thị (no enrollment/no activity/404/sync) chưa có contract. | EV-05 |
| ST21-EL-08 | Copy “Hệ thống chưa ghi nhận dữ liệu tiến trình học tập của khóa học này. Vui lòng quay lại tổng quan tiến độ.” | Static copy; không chứng minh API đã được gọi hoặc data đang thiếu. | EV-05 |
| ST21-EL-09 | CTA “Quay lại tổng quan tiến độ”; button-styled anchor | href `/student/progress`, không truyền query/body. Route runtime chưa có. | EV-07 |
| ST21-EL-10 | Footer logo/brand “Study2Work LMS” | Static presentation text/icon; không lấy từ #37. | EV-08 |
| ST21-EL-11 | Footer link group: Điều khoản, Chính sách bảo mật dữ liệu, Tiêu chuẩn học thuật, Hỗ trợ học viên | Static anchors; destinations hiện là `#`; không tạo legal/support routes hoặc APIs từ chúng. | EV-08 |

Không có course header/card, lesson list, unit status, progress bar/ring, timestamp, quiz/assignment item hoặc certificate trong PNG/HTML hiện có. Đây là expected loaded-state data theo inventory/AC-18 nhưng thiếu design element nguồn; không bịa marker/field.

## 4. Conditional UI & state variations
- States theo inventory: loading/empty/in-progress/completed
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/03_student/ST-21_tien-do-theo-khoa-hoc/ST-21.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
