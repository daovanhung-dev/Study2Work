# AD-22 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [AD-22_markers.json](../../screen_stitch/05_admin/AD-22_danh-sach-thao-luan-bi-bao-cao/AD-22_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `AD-22-EL-001` | `AD22-EL-01` | Study2Work brand / portal mark |
| #2 | `AD-22-EL-002` | `AD22-EL-02` | Navigation — Tổng quan |
| #3 | `AD-22-EL-003` | `AD22-EL-03` | Navigation — Người dùng |
| #4 | `AD-22-EL-004` | `AD22-EL-04` | Navigation — Khóa học & Nội dung |
| #5 | `AD-22-EL-005` | `AD22-EL-05` | Navigation — Kiểm duyệt |
| #6 | `AD-22-EL-006` | `AD22-EL-06` | Navigation — Báo cáo |
| #7 | `AD-22-EL-007` | `AD22-EL-07` | System Normal status badge |
| #8 | `AD-22-EL-008` | `AD22-EL-08` | Notifications bell |
| #9 | `AD-22-EL-009` | `AD22-EL-09` | Admin identity / avatar |
| #10 | `AD-22-EL-010` | `AD22-EL-10` | Global breadcrumb |
| #11 | `AD-22-EL-011` | `AD22-EL-11` | RBAC verification badge |
| #12 | `AD-22-EL-012` | `AD22-EL-12` | Local moderation breadcrumb |
| #13 | `AD-22-EL-013` | `AD22-EL-13` | Page title |
| #14 | `AD-22-EL-014` | `AD22-EL-14` | SẠCH VI PHẠM status badge |
| #15 | `AD-22-EL-015` | `AD22-EL-15` | Supporting description |
| #16 | `AD-22-EL-016` | `AD22-EL-16` | Outstanding queue metric |
| #17 | `AD-22-EL-017` | `AD22-EL-17` | Approved in 24h metric |
| #18 | `AD-22-EL-018` | `AD22-EL-18` | Search input |
| #19 | `AD-22-EL-019` | `AD22-EL-19` | Severity filter |
| #20 | `AD-22-EL-020` | `AD22-EL-20` | Reason filter |
| #21 | `AD-22-EL-021` | `AD22-EL-21` | Status filter |
| #22 | `AD-22-EL-022` | `AD22-EL-22` | Toolbar refresh button |
| #23 | `AD-22-EL-023` | `AD22-EL-23` | Table column — Discussion ID |
| #24 | `AD-22-EL-024` | `AD22-EL-24` | Table column — Topic title |
| #25 | `AD-22-EL-025` | `AD22-EL-25` | Table column — Creator |
| #26 | `AD-22-EL-026` | `AD22-EL-26` | Table column — Report count |
| #27 | `AD-22-EL-027` | `AD22-EL-27` | Table column — Flag reason |
| #28 | `AD-22-EL-028` | `AD22-EL-28` | Table column — Reported time |
| #29 | `AD-22-EL-029` | `AD22-EL-29` | Table column — Action |
| #30 | `AD-22-EL-030` | `AD22-EL-30` | Empty-state shield icon |
| #31 | `AD-22-EL-031` | `AD22-EL-31` | Empty-state title |
| #32 | `AD-22-EL-032` | `AD22-EL-32` | Empty-state explanatory copy |
| #33 | `AD-22-EL-033` | `AD22-EL-33` | Empty-state refresh button |
| #34 | `AD-22-EL-034` | `AD22-EL-34` | Static “60 giây” analysis claim |
| #35 | `AD-22-EL-035` | `AD22-EL-35` | Pagination result summary |
| #36 | `AD-22-EL-036` | `AD22-EL-36` | Current page summary |
| #37 | `AD-22-EL-037` | `AD22-EL-37` | First-page control |
| #38 | `AD-22-EL-038` | `AD22-EL-38` | Previous-page control |
| #39 | `AD-22-EL-039` | `AD22-EL-39` | Current page button |
| #40 | `AD-22-EL-040` | `AD22-EL-40` | Next-page control |
| #41 | `AD-22-EL-041` | `AD22-EL-41` | Last-page control |
| #42 | `AD-22-EL-042` | `AD22-EL-42` | Strict-processing policy card |
| #43 | `AD-22-EL-043` | `AD22-EL-43` | Response-SLA policy card |
| #44 | `AD-22-EL-044` | `AD22-EL-44` | Audit-trail policy card |
| #45 | `AD-22-EL-045` | `AD22-EL-45` | Footer copyright text |
| #46 | `AD-22-EL-046` | `AD22-EL-46` | Footer privacy link |
| #47 | `AD-22-EL-047` | `AD22-EL-47` | Footer RBAC link |
| #48 | `AD-22-EL-048` | `AD22-EL-48` | Footer support link |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Đặc tả chi tiết từng element

48 marker `#1`–`#48` theo [`AD-22_markers.json`](../../screen_stitch/05_admin/AD-22_danh-sach-thao-luan-bi-bao-cao/AD-22_markers.json), đặt trong hệ tọa độ ảnh gốc 1280×1148. “Static” dưới đây có nghĩa là text/markup của prototype, không phải server data. Element IDs cố định theo marker.

| # / Element ID | Tên / loại / vị trí | Thuộc tính, nguồn, validation | Hiển thị / trạng thái | Event |
|---:|---|---|---|---|
| **#1 `AD22-EL-01`** | Brand `Study2Work / LMS / ADMIN PORTAL`; shell header. | Text/mark tĩnh; không phải link hay tenant config. | Luôn thấy trong prototype. | — |
| **#2 `AD22-EL-02`** | Nav “Tổng quan”; anchor trong shell. | `href="#"`, `data-path="tong-quan"`; không có router mapping. | Visible theo desktop nav (`xl`). | EV-10 |
| **#3 `AD22-EL-03`** | Nav “Người dùng”; anchor. | `href="#"`, `data-path="nguoi-dung"`. | Visible desktop. | EV-10 |
| **#4 `AD22-EL-04`** | Nav “Khóa học & Nội dung”; anchor. | `href="#"`, `data-path="khoa-hoc-noi-dung"`. | Visible desktop. | EV-10 |
| **#5 `AD22-EL-05`** | Nav “Kiểm duyệt”; anchor. | `href="#"`, `data-path="kiem-duyet"`. | Visible desktop. | EV-10 |
| **#6 `AD22-EL-06`** | Nav “Báo cáo”; anchor. | `href="#"`, `data-path="bao-cao"`. | Visible desktop. | EV-10 |
| **#7 `AD22-EL-07`** | “System Normal” badge. | Literal status text and animated pulse dot; không có health API. | Visible desktop; không xác minh tình trạng hệ thống. | — |
| **#8 `AD22-EL-08`** | Notifications bell; button. | `aria-label="Notifications"`; dot unread tĩnh; không có handler/count source. | Enabled-looking; click không có effect trong HTML. | EV-10 |
| **#9 `AD22-EL-09`** | Admin name, role text, avatar. | Literal `TS. Quản Trị Viên`, `ADMIN / QUẢN TRỊ VIÊN`; không bind auth/session. | Visible theo breakpoint; không xác nhận actor. | — |
| **#10 `AD22-EL-10`** | Global breadcrumb “Hệ thống > Quản trị trung tâm > Không gian làm việc”. | Shell text/icon; không mang route state hay source data. | Visible. | EV-10 |
| **#11 `AD22-EL-11`** | “Chuẩn xác thực RBAC” badge. | Static text/icon; không chứng minh policy hoặc authorization result. | Visible ở desktop breakpoint. | — |
| **#12 `AD22-EL-12`** | Local breadcrumb “Kiểm duyệt cộng đồng > Thảo luận bị báo cáo”. | Text/link style của prototype; không có Study router. | Visible trước title. | EV-10 |
| **#13 `AD22-EL-13`** | Page heading “Hàng đợi kiểm duyệt thảo luận và báo cáo vi phạm”. | Literal title; không API binding. | Visible. | — |
| **#14 `AD22-EL-14`** | Green “SẠCH VI PHẠM” badge. | Static claim; không gắn với queue size hoặc risk calculation. | Visible dù mockup cũng ghi `TỒN ĐỌNG 0`; không coi là result. | — |
| **#15 `AD22-EL-15`** | Supporting description. | Static text về thảo luận/reports; không có API mapping. | Visible; wraps theo viewport. | — |
| **#16 `AD22-EL-16`** | Metric card “TỒN ĐỌNG 0”. | Literal count `0`; không có metric field/API/definition. | Static; không tính từ #97. | — |
| **#17 `AD22-EL-17`** | Metric card “ĐÃ DUYỆT 24H 18”. | Literal `18`; không có approved-at range/metric endpoint. | Static; không dùng làm KPI. | — |
| **#18 `AD22-EL-18`** | Search input. | `type=text`, accessible label tìm nội dung, placeholder chứa từ khóa/ID; không có giới hạn, debounce, URL sync hoặc listener. API #97 không có `q`. | Visible; nhập được trong HTML, nhưng không filter/send request. | EV-02 |
| **#19 `AD22-EL-19`** | Severity select. | `id=filter-severity`; options `all`, `low`, `medium`, `high`; taxonomy lấy từ prototype, không được catalog duyệt. Local #97 exact-match chuỗi severity; `all` không được normalize thành bỏ filter. | Visible/enabled-looking; không có change listener. | EV-03 |
| **#20 `AD22-EL-20`** | Reason select. | `id=filter-reason`; options `all`, `spam`, `inappropriate`, `copyright`; taxonomy là prototype-only. Local #97 exact-match `reason_code`; `all` không được normalize. | Visible/enabled-looking; không có change listener. | EV-04 |
| **#21 `AD22-EL-21`** | Status select. | `id=filter-status`; `pending` mặc định hiển thị; options `pending`, `investigating`, `resolved`. API #97 không nhận status; local query cố định OPEN/IN_REVIEW. | Visible/enabled-looking; không có change listener. | EV-05 |
| **#22 `AD22-EL-22`** | Toolbar “Làm mới” button. | `id=btn-refresh`; click gọi local handler; không API call. | Enabled; icon spin 700 ms trong prototype. | EV-06 |
| **#23 `AD22-EL-23`** | Table header “Mã thảo luận”. | Column label; không row/value hiển thị. ID từ current #97 item có thể là int64 nếu response hợp lệ. | Header visible; body empty state. | EV-09 (chỉ khi có row ở thiết kế tương lai) |
| **#24 `AD22-EL-24`** | Table header “Tiêu đề chủ đề”. | Column label; #97 local title là snippet content DERIVED, không phải persisted title. | Header visible; không có row. | — |
| **#25 `AD22-EL-25`** | Table header “Người tạo”. | Column label; current local #97 author projection includes `full_name` and optional `avatar_url`; live integrity chưa xác minh. | Header visible; không có row. | — |
| **#26 `AD22-EL-26`** | Table header “Số lượng báo cáo”. | Report count không tồn tại trong #97 catalog/local response. | Header visible nhưng không thể bind từ #97. | — |
| **#27 `AD22-EL-27`** | Table header “Lý do gắn cờ”. | Reason filter parameter không đồng nghĩa response reason; #97 không trả report reason. | Header visible nhưng không thể bind từ #97. | — |
| **#28 `AD22-EL-28`** | Table header “Thời điểm báo cáo”. | `created_at` report timestamp không có trong #97 response. Query nội bộ chọn timestamp nhưng view không project ra item. | Header visible nhưng không thể bind từ response. | — |
| **#29 `AD22-EL-29`** | Table header “Thao tác”. | Prototype không render action control hoặc row. | Header visible; no row action to activate. | EV-09 (future only) |
| **#30 `AD22-EL-30`** | Empty-state shield icon. | Decorative Material Symbol; no status/data source. | Visible in prototype empty state. | — |
| **#31 `AD22-EL-31`** | Empty-state heading “Hàng đợi kiểm duyệt hiện không có báo cáo nào”. | Static text; not conditionally driven by #97. | Visible in screenshot. | — |
| **#32 `AD22-EL-32`** | Empty-state explanatory copy. | Static claim all comply or flags completed; #97 does not prove either cause. | Visible; not a server result. | — |
| **#33 `AD22-EL-33`** | Empty-state “Làm mới hàng đợi báo cáo” button. | Inline `onclick=handleRefreshAction()`; same local icon animation and no request. | Enabled; animation only. | EV-07 |
| **#34 `AD22-EL-34`** | “Hệ thống phân tích tự động kiểm tra định kỳ 60 giây”. | Static text; no `setInterval`, scheduler connection, or API. | Visible; must not be implemented as polling requirement without approval. | — |
| **#35 `AD22-EL-35`** | Result count summary “Hiển thị 0 trên 0 bản ghi”. | Literal zeros; not bound to local `pagination.total` or `items`. | Visible; static. | — |
| **#36 `AD22-EL-36`** | Page summary “Trang 0 / 0”. | Literal current/total page display; current local API defaults page 1 and can return `total_pages=0`; display convention not approved. | Visible; static. | EV-08 |
| **#37 `AD22-EL-37`** | First-page button “Đầu tiên”. | Button disabled and `aria-disabled=true`. | Disabled. | EV-08 |
| **#38 `AD22-EL-38`** | Previous-page button “Trước”. | Button disabled and `aria-disabled=true`. | Disabled. | EV-08 |
| **#39 `AD22-EL-39`** | Current page box `0`. | Static non-button `<div>` with `0`; no current-page state. | Disabled-looking/static. | EV-08 |
| **#40 `AD22-EL-40`** | Next-page button “Sau”. | Button disabled and `aria-disabled=true`. | Disabled. | EV-08 |
| **#41 `AD22-EL-41`** | Last-page button “Cuối cùng”. | Button disabled and `aria-disabled=true`. | Disabled. | EV-08 |
| **#42 `AD22-EL-42`** | Policy card “Tiêu chí xử lý nghiêm ngặt”. | Prototype says >3 flags from verified accounts auto-hide pending approval. No matching rule/API/AC evidence located. | Static copy; not an executable rule. | — |
| **#43 `AD22-EL-43`** | Policy card “Thời gian phản hồi SLA”. | Prototype states hostile-language SLA up to 2 work hours; no SLA contract/service source located. | Static copy; not a timer or SLA guarantee. | — |
| **#44 `AD22-EL-44`** | Policy card “Minh bạch & Lưu vết”. | Prototype claims every hide/restore is written to Audit Trail. #97 is read-only; no audit action is performed here. | Static copy; not evidence of audit persistence. | — |
| **#45 `AD22-EL-45`** | Footer copyright/system text. | Literal `© 2025` and management-center label. | Visible. | — |
| **#46 `AD22-EL-46`** | Footer “Quy chế bảo mật dữ liệu” link. | `href="#"`; destination not defined. | Visible anchor; no app route. | EV-10 |
| **#47 `AD22-EL-47`** | Footer “Tiêu chuẩn phân quyền RBAC” link. | `href="#"`; destination not defined. | Visible anchor; no app route. | EV-10 |
| **#48 `AD22-EL-48`** | Footer “Hỗ trợ kỹ thuật hệ thống” link. | `href="#"`; destination not defined. | Visible anchor; no app route. | EV-10 |

## 4. Conditional UI & state variations
- States theo inventory: loading/empty/ready/error
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/05_admin/AD-22_danh-sach-thao-luan-bi-bao-cao/AD-22.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
