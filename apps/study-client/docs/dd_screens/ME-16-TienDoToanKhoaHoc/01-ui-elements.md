# ME-16 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [ME-16_markers.json](../../screen_stitch/04_mentor/ME-16_tien-do-toan-khoa-hoc/ME-16_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `ME-16-EL-001` | `not supplied in marker JSON` | Study2Work brand and LMS Mentor label |
| #2 | `ME-16-EL-002` | `not supplied in marker JSON` | Tổng quan navigation |
| #3 | `ME-16-EL-003` | `not supplied in marker JSON` | Khóa học phụ trách navigation hiện hành |
| #4 | `ME-16-EL-004` | `not supplied in marker JSON` | Chấm bài navigation |
| #5 | `ME-16-EL-005` | `not supplied in marker JSON` | Hộp thư hỗ trợ navigation |
| #6 | `ME-16-EL-006` | `not supplied in marker JSON` | Thông báo navigation |
| #7 | `ME-16-EL-007` | `not supplied in marker JSON` | Notification bell link and unread indicator |
| #8 | `ME-16-EL-008` | `not supplied in marker JSON` | Mentor name, role and avatar profile |
| #9 | `ME-16-EL-009` | `not supplied in marker JSON` | Breadcrumb link: Khóa học phụ trách |
| #10 | `ME-16-EL-010` | `not supplied in marker JSON` | Breadcrumb link: Chi tiết khóa học |
| #11 | `ME-16-EL-011` | `not supplied in marker JSON` | Current breadcrumb: Tiến độ học tập chung |
| #12 | `ME-16-EL-012` | `not supplied in marker JSON` | Mã lớp pill: CS-2025-FE02 |
| #13 | `ME-16-EL-013` | `not supplied in marker JSON` | Hero module label: Hệ thống Điều phối Đào tạo |
| #14 | `ME-16-EL-014` | `not supplied in marker JSON` | Page title: Tiến độ học tập toàn khóa học |
| #15 | `ME-16-EL-015` | `not supplied in marker JSON` | Course progress introduction copy |
| #16 | `ME-16-EL-016` | `not supplied in marker JSON` | Tổng ghi danh metric |
| #17 | `ME-16-EL-017` | `not supplied in marker JSON` | Cập nhật: Vừa xong metric |
| #18 | `ME-16-EL-018` | `not supplied in marker JSON` | Course selector label |
| #19 | `ME-16-EL-019` | `not supplied in marker JSON` | Course selector and three static options |
| #20 | `ME-16-EL-020` | `not supplied in marker JSON` | Mức độ hoàn thành label |
| #21 | `ME-16-EL-021` | `not supplied in marker JSON` | Tất cả completion filter |
| #22 | `ME-16-EL-022` | `not supplied in marker JSON` | Đúng tiến độ filter |
| #23 | `ME-16-EL-023` | `not supplied in marker JSON` | Cần nhắc nhở filter |
| #24 | `ME-16-EL-024` | `not supplied in marker JSON` | Tìm kiếm học viên label |
| #25 | `ME-16-EL-025` | `not supplied in marker JSON` | Student search input |
| #26 | `ME-16-EL-026` | `not supplied in marker JSON` | Bảng tổng hợp học viên & Tiến trình heading |
| #27 | `ME-16-EL-027` | `not supplied in marker JSON` | Hệ thống đồng bộ trực tiếp status badge |
| #28 | `ME-16-EL-028` | `not supplied in marker JSON` | Empty progress illustration |
| #29 | `ME-16-EL-029` | `not supplied in marker JSON` | Hourglass status badge on illustration |
| #30 | `ME-16-EL-030` | `not supplied in marker JSON` | Empty-state heading |
| #31 | `ME-16-EL-031` | `not supplied in marker JSON` | Empty-state explanatory copy |
| #32 | `ME-16-EL-032` | `not supplied in marker JSON` | Làm mới dữ liệu tiến độ button |
| #33 | `ME-16-EL-033` | `not supplied in marker JSON` | Xem phân tích khóa học (ME-18) link button |
| #34 | `ME-16-EL-034` | `not supplied in marker JSON` | Kiểm tra đợt tuyển sinh mới nhất diagnostic |
| #35 | `ME-16-EL-035` | `not supplied in marker JSON` | Xem sổ tay hướng dẫn đồng bộ LMS link |
| #36 | `ME-16-EL-036` | `not supplied in marker JSON` | SCORM/xAPI and WCAG 2.1 AA status claim |
| #37 | `ME-16-EL-037` | `not supplied in marker JSON` | Automatic refresh interval claim: every 15 minutes |
| #38 | `ME-16-EL-038` | `not supplied in marker JSON` | Footer Study2Work brand icon |
| #39 | `ME-16-EL-039` | `not supplied in marker JSON` | Footer copyright and WCAG claim |
| #40 | `ME-16-EL-040` | `not supplied in marker JSON` | Quy chế Giảng viên footer link |
| #41 | `ME-16-EL-041` | `not supplied in marker JSON` | Tiêu chuẩn đánh giá footer link |
| #42 | `ME-16-EL-042` | `not supplied in marker JSON` | Hỗ trợ kỹ thuật footer link |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Đặc tả từng element

Vị trí là vùng tương đối theo ảnh 1600×1440. Marker dùng số trong [`ME-16_markers.json`](../../screen_stitch/04_mentor/ME-16_tien-do-toan-khoa-hoc/ME-16_markers.json) và [`screen_annotated.png`](../../screen_stitch/04_mentor/ME-16_tien-do-toan-khoa-hoc/screen_annotated.png). Icon/decorative parts được tính cùng control/copy gần nhất; marker là duy nhất cho mỗi dòng dưới đây.

| ID | Tên / loại | Vị trí, mục đích và thuộc tính | Nguồn / điều kiện / trạng thái | Event |
|---:|---|---|---|---|
| 1 | Study2Work brand + LMS Mentor — anchor | Header trái; logo, tên và subtitle trong một link. Không có route thật (`href="#"`, `data-path="tong-quan"`). | Static HTML; visible desktop header; không có dynamic state. | EV-08 |
| 2 | Tổng quan — anchor/nav | Header; link `data-path="tong-quan"`, `href="#"`. | Placeholder; không xác định đích. | EV-08 |
| 3 | Khóa học phụ trách — anchor/nav hiện hành | Header; link `data-path="khoa-hoc-phu-trach"`, `aria-current="page"`. | Visual active style; không có route. | EV-08 |
| 4 | Chấm bài — anchor/nav | Header; link `data-path="cham-bai"`, `href="#"`. | Placeholder; không xác định đích. | EV-08 |
| 5 | Hộp thư hỗ trợ — anchor/nav | Header; link `data-path="hop-thu-ho-tro"`, `href="#"`. | Placeholder; không xác định đích. | EV-08 |
| 6 | Thông báo — anchor/nav | Header; link `data-path="thong-bao"`, `href="#"`. | Placeholder; không xác định đích. | EV-08 |
| 7 | Notification bell + unread dot — anchor | Header phải; thông báo icon và dot đỏ trong link `data-path="thong-bao"`, `href="#"`. | Dot là static; unread count/state không có nguồn. | EV-08 |
| 8 | Mentor profile summary | Header phải; tên “TS. Vũ Thành Đạt”, role “Mentor / Giảng viên”, avatar icon. Không có anchor/action. | Static prototype profile; không suy ra user API hoặc menu. | — |
| 9 | Breadcrumb “Khóa học phụ trách” — anchor | Hàng breadcrumb; link `data-path="khoa-hoc-phu-trach"`, `href="#"`; icon sách là decorative. | Placeholder. | EV-08 |
| 10 | Breadcrumb “Chi tiết khóa học” — anchor | Hàng breadcrumb; `href="#"`, không có `data-path`. | Placeholder; course ID/destination không có. | EV-08 |
| 11 | Current breadcrumb “Tiến độ học tập chung” | Hàng breadcrumb cuối, text `aria-current="page"`, không phải link. | Static current label. | — |
| 12 | Mã lớp badge | Góc phải breadcrumb; static `CS-2025-FE02`, chấm xanh. | Không có field class code trong #65; không dùng làm course ID. | — |
| 13 | Hero module label | Đầu card; icon + “Hệ thống Điều phối Đào tạo”. | Static copy, không có API field. | — |
| 14 | Page title | H1 “Tiến độ học tập toàn khóa học”. | Static heading. | — |
| 15 | Introductory copy | Mô tả completion, nhật ký nộp bài, chuyên cần và đồng bộ LMS cho từng học viên được phân công. | Static; các claims chưa có mapping/contract và không được #65 trả. | — |
| 16 | Tổng ghi danh metric | Hero phải; hiển thị `0 học viên`. | Static literal. #65 `items.length`/pagination total không được tự coi là enrollment metric đã duyệt. | — |
| 17 | Cập nhật metric | Hero phải; hiển thị “Vừa xong”. | Static; #65 không trả timestamp/freshness. | — |
| 18 | Course selector label | Toolbar trái, label “Khóa học phụ trách”. | Static label gắn `for="course-select"`. | EV-02 |
| 19 | Course selector — select | Toolbar trái; default `cs-frontend-2025`; options `fs-backend-nodejs`, `ai-ml-pipeline`; labels FE-Pro, BE-Adv, AI-Eng. No selected course ID mapping; không có handler. | Static HTML; displayed slugs không tương thích int64 #65/#46. Enabled-looking control nhưng không wired. | EV-02 |
| 20 | Completion label | Toolbar giữa, label “Mức độ hoàn thành”. | Static; không mô tả status taxonomy hoặc threshold. | EV-03 |
| 21 | “Tất cả” — segmented button | Toolbar giữa; selected visual default; `type=button`, không có ID/handler/`aria-pressed`. | Static selection styling; no state update. | EV-03 |
| 22 | “Đúng tiến độ” — segmented button | Toolbar giữa; `type=button`, no ID/handler. | Criteria/threshold chưa có và field không có trong #65. | EV-03 |
| 23 | “Cần nhắc nhở” — segmented button | Toolbar giữa; `type=button`, no ID/handler. | Reminder criteria/field chưa có; không suy từ percent. | EV-03 |
| 24 | Search label | Toolbar phải, “Tìm kiếm học viên”. | Static label gắn `for="student-search-input"`. | EV-04 |
| 25 | Student search input | Toolbar phải; type text; placeholder “Nhập họ tên, mã số sinh viên hoặc email...”; không required/max length/handler được khai báo. | Không có value mặc định; #65 không có email/query parameters. Search semantics và privacy chưa chốt. | EV-04 |
| 26 | Progress table title | Đầu panel; group icon + “Bảng tổng hợp học viên & Tiến trình”. | Chỉ title bar; prototype không render column headers/rows/table semantics. | — |
| 27 | Sync status badge | Panel phải; cloud icon + “Hệ thống đồng bộ trực tiếp”. | Static claim; không có sync service/status field. | — |
| 28 | Empty-state illustration | Trung tâm panel; vòng tiến độ, document/magnifier illustration. | SVG decorative (`aria-hidden=true`); static zero/empty illustration, không có data. | — |
| 29 | Hourglass status badge | Chồng góc dưới phải illustration. | Static icon; không xác định trạng thái queue/aggregation. | — |
| 30 | Empty-state heading | “Chưa có dữ liệu tiến độ học viên”. | Static copy. UI không phân biệt empty roster với progress aggregation pending. | — |
| 31 | Empty-state description | Copy nói chưa có enrollment hoặc dữ liệu đang tổng hợp; bảng hiện khi có activity. | Static; #65 empty response chỉ báo `items=[]`, không phân biệt các nguyên nhân này. | — |
| 32 | Refresh progress — button | Empty-state action; text “Làm mới dữ liệu tiến độ”; icon `#refresh-icon`; `type=button`. | Current handler spinner + disabled 1000 ms, không request/update/toast. | EV-05 |
| 33 | ME-18 analytics — anchor/button | Primary action “Xem phân tích khóa học (ME-18)”; `data-path="phan-tich-khoa-hoc-me18"`, `href="#"`. | Placeholder; course ID/destination/AC sequencing chưa chốt. | EV-07 |
| 34 | Cohort diagnostic copy | “Kiểm tra đợt tuyển sinh mới nhất”. | Static text + info icon. No cohort data/source or event. | — |
| 35 | LMS guide — anchor | “Xem sổ tay hướng dẫn đồng bộ LMS”, `href="#"`. | Placeholder; destination chưa có. | EV-08 |
| 36 | Standards/sync status statement | Banner icon + “Dữ liệu tuân thủ chuẩn mã hóa tiến trình học tập SCORM/xAPI và WCAG 2.1 AA.” | Static claim; chưa có evidence mapping/compliance audit. Không trình bày như verified. | — |
| 37 | Auto-refresh cadence statement | “Chu kỳ tự động làm mới: Mỗi 15 phút”. | Static; no `setInterval`, timer, network call or polling. | EV-09 |
| 38 | Footer brand icon | Small Study2Work logo mark. | Static decoration, non-interactive. | — |
| 39 | Footer copyright/standard copy | “© 2025 Study2Work LMS. Chuẩn kiểm định WCAG 2.1 AA. Cổng điều phối Đào tạo & Mentor.” | Static; 2025 and WCAG copy not runtime validation. | — |
| 40 | Footer “Quy chế Giảng viên” — anchor | Footer link `href="#"`. | Placeholder; route/document chưa xác định. | EV-08 |
| 41 | Footer “Tiêu chuẩn đánh giá” — anchor | Footer link `href="#"`. | Placeholder; route/document chưa xác định. | EV-08 |
| 42 | Footer “Hỗ trợ kỹ thuật” — anchor | Footer link `href="#"`. | Placeholder; route/contact chưa xác định. | EV-08 |

## 4. Conditional UI & state variations
- States theo inventory: loading/empty/ready/denied
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/04_mentor/ME-16_tien-do-toan-khoa-hoc/ME-16.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
