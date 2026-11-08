# AD-17 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [AD-17_markers.json](../../screen_stitch/05_admin/AD-17_thong-ke-bai-kiem-tra/AD-17_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `AD-17-EL-001` | `not supplied in marker JSON` | Study2Work LMS brand |
| #2 | `AD-17-EL-002` | `not supplied in marker JSON` | Shell navigation — Tổng quan |
| #3 | `AD-17-EL-003` | `not supplied in marker JSON` | Shell navigation — Người dùng |
| #4 | `AD-17-EL-004` | `not supplied in marker JSON` | Shell navigation — Khóa học & Nội dung |
| #5 | `AD-17-EL-005` | `not supplied in marker JSON` | Shell navigation — Kiểm duyệt |
| #6 | `AD-17-EL-006` | `not supplied in marker JSON` | Shell navigation — Báo cáo |
| #7 | `AD-17-EL-007` | `not supplied in marker JSON` | SYSTEM NORMAL badge (static copy) |
| #8 | `AD-17-EL-008` | `not supplied in marker JSON` | Notification button (no handler) |
| #9 | `AD-17-EL-009` | `not supplied in marker JSON` | Admin identity and avatar |
| #10 | `AD-17-EL-010` | `not supplied in marker JSON` | Global breadcrumb |
| #11 | `AD-17-EL-011` | `not supplied in marker JSON` | Chuẩn xác thực RBAC badge (static copy) |
| #12 | `AD-17-EL-012` | `not supplied in marker JSON` | Local breadcrumb — Quản trị khảo thí |
| #13 | `AD-17-EL-013` | `not supplied in marker JSON` | Local breadcrumb link — Danh sách bài kiểm tra |
| #14 | `AD-17-EL-014` | `not supplied in marker JSON` | Local breadcrumb — Báo cáo thống kê |
| #15 | `AD-17-EL-015` | `not supplied in marker JSON` | AD-17 page title |
| #16 | `AD-17-EL-016` | `not supplied in marker JSON` | Page subtitle |
| #17 | `AD-17-EL-017` | `not supplied in marker JSON` | Top return link to AD-15 |
| #18 | `AD-17-EL-018` | `not supplied in marker JSON` | Target Quiz card heading |
| #19 | `AD-17-EL-019` | `not supplied in marker JSON` | Thực thể Quiz độc lập badge |
| #20 | `AD-17-EL-020` | `not supplied in marker JSON` | Quiz title placeholder KPI |
| #21 | `AD-17-EL-021` | `not supplied in marker JSON` | Route ID placeholder KPI |
| #22 | `AD-17-EL-022` | `not supplied in marker JSON` | Sync status placeholder KPI |
| #23 | `AD-17-EL-023` | `not supplied in marker JSON` | Empty-state illustration |
| #24 | `AD-17-EL-024` | `not supplied in marker JSON` | Empty-state heading |
| #25 | `AD-17-EL-025` | `not supplied in marker JSON` | Empty-state explanatory text |
| #26 | `AD-17-EL-026` | `not supplied in marker JSON` | Return to AD-15 primary action |
| #27 | `AD-17-EL-027` | `not supplied in marker JSON` | Check data connection button |
| #28 | `AD-17-EL-028` | `not supplied in marker JSON` | Data integrity note card |
| #29 | `AD-17-EL-029` | `not supplied in marker JSON` | Analysis process note card |
| #30 | `AD-17-EL-030` | `not supplied in marker JSON` | Footer copyright and system label |
| #31 | `AD-17-EL-031` | `not supplied in marker JSON` | Footer privacy link |
| #32 | `AD-17-EL-032` | `not supplied in marker JSON` | Footer RBAC link |
| #33 | `AD-17-EL-033` | `not supplied in marker JSON` | Footer technical support link |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Đặc tả element

Marker positions là tâm theo ảnh gốc `screen.png` 1600×1440. `screen_annotated.png` được tạo 2×; thứ tự và ID khớp `AD-17_markers.json` / `AD-17_markers.svg`. Các nhóm icon/trang trí nền nằm trong marker của nhóm UI chứa chúng. Element `syncFeedback` là DOM-only state, đang ẩn trong ảnh gốc; được mô tả ở EV-07 nhưng không có marker hiển thị.

| ID | Tâm marker (x,y) | Tên / loại / vị trí | Thuộc tính, dữ liệu và điều kiện | Trạng thái / event |
|---:|:---:|---|---|---|
| 1 | (15,15) | Logo/brand Study2Work LMS; header trái | Logo “S”, brand, badge LMS/Admin Portal; static. | Default; shell placeholder, EV-08. |
| 2 | (340,15) | Nav “Tổng quan”; header | Anchor `href="#"`; không có route mapping. | Default/hover CSS; EV-08. |
| 3 | (488,15) | Nav “Người dùng”; header | Anchor `href="#"`; không có route mapping. | Default/hover CSS; EV-08. |
| 4 | (652,15) | Nav “Khóa học & Nội dung”; header | Anchor `href="#"`; không có route mapping. | Default/hover CSS; EV-08. |
| 5 | (858,15) | Nav “Kiểm duyệt”; header | Anchor `href="#"`; không có route mapping. | Default/hover CSS; EV-08. |
| 6 | (1008,15) | Nav “Báo cáo”; header | Anchor `href="#"`; không có route mapping. | Default/hover CSS; EV-08. |
| 7 | (1165,15) | Badge `SYSTEM NORMAL`; header | Copy tĩnh; không có health-check source. | Static; không biểu thị trạng thái API; EV-08. |
| 8 | (1307,15) | Nút notification; header | Button không có handler screen-specific. | Default/hover CSS; EV-08. |
| 9 | (1570,15) | Danh tính Admin/avatar; header | Tên vai trò tĩnh; không có profile/auth binding. | Static; không chứng minh session/permission; EV-02, EV-08. |
| 10 | (520,95) | Breadcrumb hệ thống; dưới header | Các nhãn Hệ thống → Quản trị trung tâm → Không gian làm việc; không có route source. | Static; EV-08. |
| 11 | (1585,95) | Badge “Chuẩn xác thực RBAC”; phải breadcrumb | Copy tĩnh; không có guard wiring. | Static; không chứng minh authorization; EV-02. |
| 12 | (95,145) | Breadcrumb “Quản trị khảo thí” | Span/click-style, không có `href`. | Static; EV-08. |
| 13 | (258,145) | Breadcrumb link “Danh sách bài kiểm tra” | `href="/admin/quizzes"`; target AD-15 candidate. | Hover CSS; EV-06. |
| 14 | (430,145) | Current breadcrumb “Báo cáo thống kê” | Span current page. | Static; EV-01. |
| 15 | (650,200) | Title “Báo cáo thống kê kết quả kiểm tra” | H1; static text. | Default; EV-01/EV-04. |
| 16 | (680,300) | Subtitle | “Giám sát tình trạng ghi nhận chỉ số thực thi và phân tích phân phối bài làm”; static claim, không phải metric contract. | Default; EV-04. |
| 17 | (1585,294) | Top return link to AD-15 | Anchor `/admin/quizzes`. | Click navigation target theo HTML; client router chưa xác minh; EV-06. |
| 18 | (315,365) | Heading “THỰC THỂ BÀI THI MỤC TIÊU” | Section/card title; static. | Default; EV-01/EV-04. |
| 19 | (1318,375) | Badge “Thực thể Quiz độc lập” | Static copy; không có schema/entity proof. | Default; EV-04. |
| 20 | (518,415) | Quiz title KPI card | Label TÊN BÀI THI, value `--`, copy “Chưa gán bản ghi bài kiểm tra”; không bind response. | Placeholder/no-data tĩnh; EV-01/EV-04. |
| 21 | (1018,415) | Quiz ID KPI card | Copy “Chưa nạp tham số ID hợp lệ” và `:quizId`; chưa đọc URL param. | Placeholder; candidate input thuộc EV-01. |
| 22 | (1515,415) | Sync status KPI card | “Chờ liên kết dữ liệu”, “Phản hồi không mang gói analytics”; static. | Placeholder; không phải network state; EV-03/EV-04. |
| 23 | (700,684) | Empty-state icon/illustration | Icon biểu đồ + kính lúp, trang trí; không là chart dữ liệu. | Empty-state static; EV-04. |
| 24 | (1174,827) | Empty-state heading | “Chưa có số liệu thống kê phân tích”; luôn hiển thị. | No-data copy chưa dựa response; EV-04. |
| 25 | (350,878) | Empty-state explanation | Claim chưa cấu hình dịch vụ; nêu phổ điểm, tỷ lệ hoàn thành, thời gian trung bình và hiển thị tự động sau enable. Không được xem như behavior đã xác nhận. | Static; unsupported claims; EV-04, EV-09. |
| 26 | (426,1029) | CTA “Quay lại danh sách bài kiểm tra (AD-15)” | Anchor `/admin/quizzes`; thứ hai trong page. | Click; EV-06. |
| 27 | (1175,1029) | Button “Kiểm tra kết nối dữ liệu” | `button#btnCheckConnection`; không có API/fetch. | Default → disabled/spinner/label → fixed feedback sau 700 ms → reset label/enable sau 3 giây; EV-07. |
| 28 | (758,1206) | Note card “Chính sách xử lý dữ liệu chuẩn xác thực” | Shield icon, title/body; static assurance about no estimate/telemetry. | Static copy, not policy evidence; EV-04. |
| 29 | (1546,1205) | Note card “Quy trình ghi nhận phân tích kết quả” | Icon, title/body; claims background aggregate after student submit. | Static claim conflicts with GET-only path evidence; EV-09. |
| 30 | (245,1357) | Footer copyright/system label | `© 2025 Study2Work LMS`, hệ thống quản trị; static. | Default; EV-08. |
| 31 | (970,1357) | Footer privacy link | `href="#"`; no destination. | Hover CSS; EV-08. |
| 32 | (1190,1357) | Footer RBAC link | `href="#"`; no destination. | Hover CSS; EV-08. |
| 33 | (1450,1357) | Footer technical support link | `href="#"`; no destination. | Hover CSS; EV-08. |

## 4. Conditional UI & state variations
- States theo inventory: unwired/loading/no-data/ready/unauthorized/forbidden/not-found/error
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/05_admin/AD-17_thong-ke-bai-kiem-tra/AD-17.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
