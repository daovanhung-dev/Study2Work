# ME-01 — Dashboard mentor · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `ME-01` |
| Module | Mentor |
| Route | `/mentor` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **DD status:** `DD BLOCKED` — chưa đủ dữ liệu và quyết định để chuyển màn hình mẫu thành đặc tả triển khai hoàn chỉnh.; **Implementation status:** `IMPLEMENTATION BLOCKED` — Study Web source/router không có trong checkout; một số widget và luồng điều hướng chưa có contract.; **Runtime status:** `RUNTIME NOT VERIFIED` — chỉ xác minh source và asset tĩnh; không xác minh deployment, database live hoặc UI chạy thật. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [ME-01.md](../../screen_stitch/04_mentor/ME-01_dashboard-mentor/ME-01.md), [ME-01_PLAN.md](../../screen_stitch/04_mentor/ME-01_dashboard-mentor/ME-01_PLAN.md), [ME-01_markers.json](../../screen_stitch/04_mentor/ME-01_dashboard-mentor/ME-01_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Card khóa đang phụ trách, submission chưa chấm, yêu cầu hỗ trợ.
- In-scope: GET #46/#54/#58 theo quyền; mỗi widget có trạng thái lỗi độc lập.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-21,AC-23,AC-24 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Card khóa đang phụ trách, submission chưa chấm, yêu cầu hỗ trợ. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #46, #54, #58
- Liên kết màn hình dự kiến: [ME-02](../ME-02-CacKhoaHocPhuTrach/00-overview.md), [ME-09](../ME-09-DanhSachBaiCanCham/00-overview.md), [ME-11](../ME-11-HopThuHoTroHocVien/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | loading/partial/empty/error |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [ME-01 source screen.png](../../screen_stitch/04_mentor/ME-01_dashboard-mentor/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/04_mentor/ME-01_dashboard-mentor/screen_annotated.png))
- Luồng: GET #46/#54/#58 theo quyền; mỗi widget có trạng thái lỗi độc lập.
- Priority: P1; Gate/source status: **D**; **BLOCK:** Role introspection Mentor chưa có

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# ME-01 — Dashboard mentor

> **DD status:** `DD BLOCKED` — chưa đủ dữ liệu và quyết định để chuyển màn hình mẫu thành đặc tả triển khai hoàn chỉnh.
>
> **Implementation status:** `IMPLEMENTATION BLOCKED` — Study Web source/router không có trong checkout; một số widget và luồng điều hướng chưa có contract.
>
> **Runtime status:** `RUNTIME NOT VERIFIED` — chỉ xác minh source và asset tĩnh; không xác minh deployment, database live hoặc UI chạy thật.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: 1. Tổng quan

| Thuộc tính | Giá trị |
|---|---|
| Screen ID / tên | ME-01 — Dashboard mentor |
| Surface / route | Page; route đề xuất `/mentor` theo inventory, chưa phải route runtime |
| Actor | Mentor đã đăng nhập; role được kiểm tra ở các API server, client role shell hiện không có source để xác minh |
| Mục đích dự kiến | Điểm vào các tác vụ khóa học, bài nộp cần chấm và hỗ trợ học viên; inventory yêu cầu các widget có trạng thái lỗi độc lập |
| AC tham chiếu | AC-21, AC-23, AC-24. Các diagram đặc tả tạo lecture, chấm bài và hỗ trợ; không mô tả đầy đủ dashboard hay các widget lịch/rating/thông báo trong ảnh. |
| API inventory | #46 courses; #54 submissions; #58 support requests. Ba route/module hiện có source. Các API DD/catalog snapshots còn trạng thái Draft/Design snapshot và một số response choice là derived. |
| Màn hình liên kết | ME-02 khóa học phụ trách; ME-03 workspace; ME-06 cây nội dung; ME-09 danh sách bài cần chấm; ME-10 chấm bài; ME-11 hộp thư hỗ trợ; ME-12 thread hỗ trợ. Link chính thức theo inventory của ME-01 là ME-02/ME-09/ME-11; các direct action ME-03/06/10/12 đến từ nội dung asset và cần chốt. |
| Điều kiện trước | JWT access hợp lệ, `sub` là ID số dương, `roles` chứa `MENTOR`; API #46/#54/#58 kiểm tra Bearer và role trước truy vấn. Không có bằng chứng về client session persistence, route guard hay Mentor profile bootstrap. |
| Kết quả khi tải thành công | Các response read-only được ánh xạ theo từng widget; API không mutation. Không có bằng chứng dữ liệu được cache/lưu ở client. |

### Tài sản và nguồn thẩm quyền

| Tài sản/nguồn | Quan sát | Thẩm quyền |
|---|---|---|
| [Ảnh nguyên trạng](../../screen_stitch/04_mentor/ME-01_dashboard-mentor/screen.png) | PNG 1086×1600. SHA-256 `f135d0b109a05d276654a6b8b51545d9f2996ab474c47b7829c9983739eea3d2`. Giữ nguyên. | Ảnh thiết kế tĩnh, không phải runtime capture. |
| [HTML tĩnh](../../screen_stitch/04_mentor/ME-01_dashboard-mentor/code.html) | 52,234 bytes; SHA-256 `f10dfa929e89288165bf0264b1b1f863f2380006d064f8e470118a7cfe626334`. Cấu trúc chính tương ứng PNG; anchors dùng `href="#"`, input không có `id`/`name`, không có handler/API/router client. | Prototype/source thiết kế, không phải ứng dụng đang chạy. |
| [Ảnh chú thích](../../screen_stitch/04_mentor/ME-01_dashboard-mentor/screen_annotated.png) | Được tạo riêng từ PNG nguyên trạng ở tỉ lệ 2×; không thay ảnh nguồn. | Dùng để định vị 23 nhóm element. |
| [Marker map](../../screen_stitch/04_mentor/ME-01_dashboard-mentor/ME-01_markers.json) và [SVG overlay](../../screen_stitch/04_mentor/ME-01_dashboard-mentor/ME-01_markers_overlay.svg) | Marker `#1–#23`, `ME01-EL-01..23`, tọa độ theo ảnh nguồn. | Mỗi marker ánh xạ tới đúng một hàng element ở §4. |
| [Screen inventory](../../list_screen.md) và [kế hoạch tổng](../../screen_stitch/dd_screens/PLAN.md) | Tên, actor, route đề xuất, links, API và states dự kiến. | Expected design, không chứng minh client behavior. |
| [Study Web status](../../../../../.agents/web-work/study/INDEX.md) | Recheck checkout: có `docs`, `dist`, `tsconfig.tsbuildinfo`; không có `src/` hay `package.json`. Bundle dist hiện chỉ có route `/`. | Current client source status: `UNWIRED`; serving/deployment không xác minh. |
| [Study Web design guide](../../../../../.agents/web-study/design.md) | Ocean-primary `#0B5F8A`, Inter/system font, content width khoảng 1120px, điều khiển tối thiểu 44px, không dùng large gradient/remote font. | Đích giao diện; không phải runtime evidence. |

Ảnh và HTML là mẫu dashboard có dữ liệu minh họa: tên Mentor/học viên, vai trò công ty, số lượng khóa học/học viên, deadline/SLA, điểm đánh giá, lịch hẹn, meeting URL, kỳ học, thông báo, hotline và tổ chức đối tác. Không dùng các giá trị này làm default, dữ liệu thật, KPI hoặc business rule.

Prototype dùng Plus Jakarta Sans và tải Google Fonts/Tailwind từ CDN, màu chính `#004ac6`, hero gradient rộng, icon button khoảng 40×40px và body text nhỏ hơn guide. Đây là các sai khác với Study Web design guide; không sửa asset nguồn và chưa tự chọn palette/type thay thế. Cần chốt thiết kế khi có UI implementation.
