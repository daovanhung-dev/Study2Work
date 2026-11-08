# GS-03 — Chi tiết khóa học · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `GS-03` |
| Module | Guest / Discovery |
| Route | `/courses/:courseId` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **DD status:** `DD BLOCKED` — this DD fully describes the only static state available in the source HTML and traces the current API sources. It does not define the missing loaded course detail UI or resolve the API orchestration conflicts.; **Implementation status:** `IMPLEMENTATION BLOCKED`.; **Runtime status:** `RUNTIME NOT VERIFIED` — Study Web has no wired app/router in the current checkout. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [GS-03.md](../../screen_stitch/02_guest_discovery/GS-03_chi-tiet-khoa-hoc/GS-03.md), [GS-03_PLAN.md](../../screen_stitch/02_guest_discovery/GS-03_chi-tiet-khoa-hoc/GS-03_PLAN.md), [GS-03_markers.json](../../screen_stitch/02_guest_discovery/GS-03_chi-tiet-khoa-hoc/GS-03_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Thông tin khóa học, mentor, giá, tab đề cương/đánh giá, CTA ghi danh.
- In-scope: GET #8 để xác định published → lazy GET #9 và #10 theo tab; course ID thống nhất.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

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
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [GS-03 source screen.png](../../screen_stitch/02_guest_discovery/GS-03_chi-tiet-khoa-hoc/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/02_guest_discovery/GS-03_chi-tiet-khoa-hoc/screen_annotated.png))
- Luồng: GET #8 để xác định published → lazy GET #9 và #10 theo tab; course ID thống nhất.
- Priority: P1; Gate/source status: **R (#08/#09), D (#10)**; **BLOCK:** #08 trả singleton Page<Course>, source LEFT JOIN khác API DD INNER JOIN; int64 course_id chưa khớp validator raw-string không có signed int64 range; AC-05 eager khác F02 lazy; #10 thiếu route/title-rating source; G-01 enrollment handoff; Study Web UNWIRED

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# GS-03 — Chi tiết khóa học

> **DD status:** `DD BLOCKED` — this DD fully describes the only static state available in the source HTML and traces the current API sources. It does not define the missing loaded course detail UI or resolve the API orchestration conflicts.  
> **Implementation status:** `IMPLEMENTATION BLOCKED`.  
> **Runtime status:** `RUNTIME NOT VERIFIED` — Study Web has no wired app/router in the current checkout.  
> **Session scope:** GS-03 only; do not start GS-04 in this session.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID / tên | GS-03 — Chi tiết khóa học (Page) |
| Mục tiêu | Cho Guest xem thông tin của một khóa học đã xuất bản, mentor, giá và mở các tab đề cương/đánh giá; inventory còn yêu cầu CTA ghi danh. Các phần loaded này chưa có thiết kế/handler trong source HTML hiện có. |
| Actor | `Guest` theo AC-05. Link đăng nhập/đăng ký có trong HTML tĩnh. |
| Route đề xuất | `/courses/:courseId` từ `apps/study-client/docs/list_screen.md`; chưa được Study Web router thực thi. API catalog khai báo `course_id:int64`, nhưng current #08/#09 routes nhận `str` và parser không enforce signed int64 hoặc positive range. Min/max chưa được xác nhận. |
| API tham chiếu | #08 detail (`SOURCE_BACKED`); #09 curriculum (`SOURCE_BACKED`); #10 reviews (`DECLARED_NOT_RUNNABLE`). GS-03 không gọi API #15 enrollment status. |
| Màn hình liên quan | GS-01/GS-02 là nguồn điều hướng vào detail; GS-04 curriculum, GS-05 reviews, GS-06 resources là tab liên quan; ST-04 là điểm tiếp theo được đề xuất cho ghi danh. Route/state handoff của các màn hình này chưa được runtime xác minh. |
| Điều kiện truy cập | Expected: route chứa course ID hợp lệ và #08 xác nhận course `PUBLISHED`. HTML hiện tại không đọc route hay kiểm tra quyền. #08/#09 là public và chỉ trả course/lessons `PUBLISHED`. |
| Kết quả truy cập | Expected: detail và tab data theo contract được xác nhận; hiện tại chỉ có empty/unavailable state tĩnh. Không có dữ liệu nào được cache hoặc lưu bởi HTML. |

### Expected behavior và current behavior

| Expected theo inventory/AC | Current source trong checkout |
|---|---|
| Hiển thị course detail, mentor, price và CTA ghi danh. | Không có course data, mentor, giá hoặc CTA trong `code.html`. |
| Dùng #08 để xác định course PUBLISHED; tab curriculum/reviews tải lười theo tab theo F02. | Không có route parser, API call hoặc JavaScript handler trong `code.html`. AC-05 lại mô tả tuần tự #08 → #09 → #10 trước khi render. Đây là discrepancy; DD giữ nguyên cả hai nguồn. |
| Có trạng thái loading, course-404 và partial-tab-error theo inventory. | HTML chỉ có một thông báo “Thông tin khóa học hiện chưa có sẵn.”; không có loading/error variants. |
| #09 cung cấp curriculum; #10 cung cấp reviews và rating theo catalog/AC. | #09 có route/module/test backend; #10 chỉ được khai báo trong catalog/API DD, không có route/module/test. DDL không có title/rating source. |

### Tài sản thiết kế

- [Ảnh nguồn `screen.png`](../../screen_stitch/02_guest_discovery/GS-03_chi-tiet-khoa-hoc/screen.png) được giữ nguyên, SHA-256 `94360a8b1b1a9bbe0cdc110f6c243ce5aaabd8b6923331c5667421cb1c37d34d`; 1280×1024, gần như trắng và không đọc được thành phần UI.
- [Ảnh render thay thế `screen_rendered.png`](../../screen_stitch/02_guest_discovery/GS-03_chi-tiet-khoa-hoc/screen_rendered.png) được tạo từ HTML gốc nguyên trạng bằng Firefox headless, 1440×1200. Ảnh render cho thấy đầy đủ header, breadcrumb, title, tab, empty panel và footer. Đây là bản render của prototype tĩnh, không phải runtime screenshot.
- [Ảnh có đánh số `screen_annotated.png`](../../screen_stitch/02_guest_discovery/GS-03_chi-tiet-khoa-hoc/screen_annotated.png) dựa trên `screen_rendered.png`; 10 marker ở gutter, không che nội dung.
- [Bản đồ marker `GS-03_markers.json`](../../screen_stitch/02_guest_discovery/GS-03_chi-tiet-khoa-hoc/GS-03_markers.json) là nguồn tọa độ/thứ tự và ánh xạ element.
- [Kế hoạch GS-03](../../screen_stitch/02_guest_discovery/GS-03_chi-tiet-khoa-hoc/GS-03_PLAN.md) ghi expected/current behavior, trace và blocker trước khi tạo ảnh/DD.
- [`code.html`](../../screen_stitch/02_guest_discovery/GS-03_chi-tiet-khoa-hoc/code.html) được giữ nguyên; SHA-256 `d4f4bfdb56324b7c96589af75362903a491a3f565c97152b63634573c9d69619`.

`code.html` tải Tailwind và Google Fonts từ CDN. `.agents/web-study/design.md` là hướng dẫn đích yêu cầu không phụ thuộc font từ xa; do đó prototype này chưa chứng minh tuân thủ UI standard của Study2Work.
