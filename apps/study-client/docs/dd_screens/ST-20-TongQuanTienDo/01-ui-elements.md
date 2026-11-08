# ST-20 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [ST-20_markers.json](../../screen_stitch/03_student/ST-20_tong-quan-tien-do/ST-20_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `ST-20-EL-001` | `ST20-EL-01` | Study2Work brand and home link |
| #2 | `ST-20-EL-002` | `ST20-EL-02` | Primary navigation group: overview, my courses, active progress |
| #3 | `ST-20-EL-003` | `ST20-EL-03` | Breadcrumb trail |
| #4 | `ST-20-EL-004` | `ST20-EL-04` | Page title “Tổng quan tiến độ” |
| #5 | `ST-20-EL-005` | `ST20-EL-05` | Page summary description |
| #6 | `ST-20-EL-006` | `ST20-EL-06` | Empty-state analytics icon |
| #7 | `ST-20-EL-007` | `ST20-EL-07` | Empty-state heading |
| #8 | `ST-20-EL-008` | `ST20-EL-08` | Empty-state explanatory copy |
| #9 | `ST-20-EL-009` | `ST20-EL-09` | View my courses button |
| #10 | `ST-20-EL-010` | `ST20-EL-10` | Footer brand and description |
| #11 | `ST-20-EL-011` | `ST20-EL-11` | Footer program link group |
| #12 | `ST-20-EL-012` | `ST20-EL-12` | Footer support link group |
| #13 | `ST-20-EL-013` | `ST20-EL-13` | Footer contact details |
| #14 | `ST-20-EL-014` | `ST20-EL-14` | Copyright and platform strip text |
| #15 | `ST-20-EL-015` | `ST20-EL-15` | Terms of use link |
| #16 | `ST-20-EL-016` | `ST20-EL-16` | Privacy policy link |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Đặc tả chi tiết element

Marker được đặt cạnh nhóm nội dung tương ứng trong `screen_annotated.png`; tọa độ target trong `ST-20_markers.json` tính theo ảnh `screen_rendered.png`. Các nội dung trong HTML là static prototype, không khẳng định route hoặc API đang hoạt động.

| ID / Marker | Element, loại, vị trí | Data / thuộc tính / trạng thái | Event |
|---|---|---|---|
| ST20-EL-01 | Brand Study2Work/LMS PORTAL, logo và home link; header trái | Text/icon tĩnh; href trong prototype không phải route runtime. Không có input/validation. | EV-10 |
| ST20-EL-02 | Nhóm điều hướng Tổng quan / Khóa học của tôi / Tiến độ; header | Ba link tĩnh; “Tiến độ” là active trong prototype. Destination/role guard chưa được wire. | EV-10 |
| ST20-EL-03 | Breadcrumb Trang chủ → Học viên → Tổng quan tiến độ | Nhãn tĩnh, không có route params; parent navigation và back behavior chưa được xác định. | EV-10 |
| ST20-EL-04 | Tiêu đề “Tổng quan tiến độ”; heading trong main | Static copy; không có data binding. Visible trong HTML render; source PNG ban đầu không có title. | — |
| ST20-EL-05 | Mô tả theo dõi tiến trình học; paragraph dưới title | Static copy; không phải metric hoặc cam kết về công thức tính. | — |
| ST20-EL-06 | Icon analytics của empty-state card | Static icon; không có giá trị, API field hoặc action riêng. | — |
| ST20-EL-07 | Tiêu đề empty state “Chưa có dữ liệu tiến độ để hiển thị.” | Copy tĩnh trong HTML. Điều kiện thực tế để hiện (không ghi danh, không có progress hay lỗi) chưa có contract. | EV-06 |
| ST20-EL-08 | Nội dung giải thích “Chưa có dữ liệu học tập ghi nhận hoặc hệ thống đang cập nhật. Vui lòng kiểm tra lại sau.” | Copy tĩnh; không xác định backend đang đồng bộ và không có timer/polling contract. | EV-06 |
| ST20-EL-09 | Link `<a>` được tạo kiểu button “Xem khóa học của tôi”; empty-state CTA | Anchor trong HTML tới `/student/courses`; không có current Study Web route. Không mang course ID. | EV-09 |
| ST20-EL-10 | Footer brand, logo và mô tả Study2Work LMS | Copy tĩnh; không lấy từ API ST-20. | EV-10 |
| ST20-EL-11 | Cột Chương trình và các link khóa học/lộ trình/đồ án | Link group tĩnh trong footer; destinations không được wire trong prototype. | EV-10 |
| ST20-EL-12 | Cột Hỗ trợ và các link diễn đàn/cố vấn/trung tâm trợ giúp | Link group tĩnh; không tạo support/discussion action từ ST-20. | EV-10 |
| ST20-EL-13 | Cột Liên hệ: địa điểm, hotline, email | Nội dung tĩnh; không phải profile/config API contract. | — |
| ST20-EL-14 | Dải bản quyền và mô tả nền tảng | Copy tĩnh trong legal strip; không có hành vi tương tác. | — |
| ST20-EL-15 | Link “Điều khoản sử dụng” | Href không chứng minh route/document đích hiện hành. | EV-10 |
| ST20-EL-16 | Link “Chính sách bảo mật” | Href không chứng minh route/document đích hiện hành. | EV-10 |

Không có element progress chart, course card, lesson count, achievement badge hoặc chứng nhận trong PNG gốc hay HTML render. Đây là phần expected behavior trong inventory, nhưng loaded-state component design chưa được cung cấp; không tạo marker giả cho các element này.

## 4. Conditional UI & state variations
- States theo inventory: loading/partial/empty/error
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/03_student/ST-20_tong-quan-tien-do/ST-20.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
