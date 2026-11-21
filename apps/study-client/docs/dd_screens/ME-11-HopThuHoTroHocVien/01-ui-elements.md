# ME-11 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [ME-11_markers.json](../../screen_stitch/04_mentor/ME-11_hop-thu-ho-tro-hoc-vien/ME-11_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `ME-11-EL-001` | `ME11-EL-01` | Study2Work Mentor brand/logo link |
| #2 | `ME-11-EL-002` | `ME11-EL-02` | Header navigation: Tổng quan |
| #3 | `ME-11-EL-003` | `ME11-EL-03` | Header navigation: Khóa học phụ trách |
| #4 | `ME-11-EL-004` | `ME11-EL-04` | Header navigation: Chấm bài |
| #5 | `ME-11-EL-005` | `ME11-EL-05` | Active navigation: Hộp thư hỗ trợ |
| #6 | `ME-11-EL-006` | `ME11-EL-06` | Header navigation: Thông báo |
| #7 | `ME-11-EL-007` | `ME11-EL-07` | Notification bell and unread dot |
| #8 | `ME-11-EL-008` | `ME11-EL-08` | Mentor sample name, role and avatar |
| #9 | `ME-11-EL-009` | `ME11-EL-09` | Support eyebrow/icon |
| #10 | `ME-11-EL-010` | `ME11-EL-10` | Page title |
| #11 | `ME-11-EL-011` | `ME11-EL-11` | Page description |
| #12 | `ME-11-EL-012` | `ME11-EL-12` | SLA <4 giờ badge |
| #13 | `ME-11-EL-013` | `ME11-EL-13` | “Vừa cập nhật tức thì” badge |
| #14 | `ME-11-EL-014` | `ME11-EL-14` | Filter panel/surface |
| #15 | `ME-11-EL-015` | `ME11-EL-15` | “Tất cả” tab and sample count |
| #16 | `ME-11-EL-016` | `ME11-EL-16` | “Đang mở” tab and sample count |
| #17 | `ME-11-EL-017` | `ME11-EL-17` | “Đã giải quyết” tab and sample count |
| #18 | `ME-11-EL-018` | `ME11-EL-18` | Course filter label |
| #19 | `ME-11-EL-019` | `ME11-EL-19` | Course filter select |
| #20 | `ME-11-EL-020` | `ME11-EL-20` | Empty-state panel |
| #21 | `ME-11-EL-021` | `ME11-EL-21` | Empty-state mail illustration |
| #22 | `ME-11-EL-022` | `ME11-EL-22` | Empty-state heading |
| #23 | `ME-11-EL-023` | `ME11-EL-23` | Empty-state explanatory copy |
| #24 | `ME-11-EL-024` | `ME11-EL-24` | “Làm mới hộp thư” button |
| #25 | `ME-11-EL-025` | `ME11-EL-25` | Automatic notification/realtime claim |
| #26 | `ME-11-EL-026` | `ME11-EL-26` | SLA information card |
| #27 | `ME-11-EL-027` | `ME11-EL-27` | Standard-answer information card |
| #28 | `ME-11-EL-028` | `ME11-EL-28` | Direct meeting information card |
| #29 | `ME-11-EL-029` | `ME11-EL-29` | Footer logo |
| #30 | `ME-11-EL-030` | `ME11-EL-30` | Footer copyright/WCAG copy |
| #31 | `ME-11-EL-031` | `ME11-EL-31` | Footer link: Quy chế Giảng viên |
| #32 | `ME-11-EL-032` | `ME11-EL-32` | Footer link: Tiêu chuẩn đánh giá |
| #33 | `ME-11-EL-033` | `ME11-EL-33` | Footer link: Hỗ trợ kỹ thuật |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Đặc tả chi tiết element

Marker `#1–#33` trong [ảnh đánh số](../../screen_stitch/04_mentor/ME-11_hop-thu-ho-tro-hoc-vien/screen_annotated.png) khớp `number` và `id` ở [JSON map](../../screen_stitch/04_mentor/ME-11_hop-thu-ho-tro-hoc-vien/ME-11_markers.json) và SVG overlay. Tất cả coordinates dùng ảnh nguồn 1600×1425; ảnh chú thích 3200×2850. Các giá trị hiển thị ở mockup là source content, không phải dữ liệu API/runtime.

| # / Element ID | Tên, loại, vị trí, thuộc tính và dữ liệu | Hiển thị / trạng thái / validation | Event |
|---|---|---|---|
| 1 / ME11-EL-01 | Brand/logo link Study2Work Mentor ở header trái; `data-path="tong-quan"`, `href="#"`. | Luôn hiện trong desktop mockup; destination chưa wire; no input. | E06 |
| 2 / ME11-EL-02 | Nav link “Tổng quan”; anchor `href="#"`. | Static header item; no route/current-session source. | E06 |
| 3 / ME11-EL-03 | Nav link “Khóa học phụ trách”; anchor `href="#"`. | Không mang `course_id`; đích và history chưa xác nhận. | E06 |
| 4 / ME11-EL-04 | Nav link “Chấm bài”; anchor `href="#"`. | Không có `aria-current` trong prototype này; destination chưa wire. | E06 |
| 5 / ME11-EL-05 | Nav “Hộp thư hỗ trợ” đang selected; `aria-current="page"`; anchor `href="#"`. | Mục hiện hành theo mockup; không có route runtime. | E06 |
| 6 / ME11-EL-06 | Nav link “Thông báo”; anchor `href="#"`. | Chỉ là link mẫu; unread target chưa xác nhận. | E06 |
| 7 / ME11-EL-07 | Notification bell link và dot đỏ unread; anchor `data-path="thong-bao"`, `href="#"`. | Dot không gắn API/state; không kết luận có unread notification. | E06 |
| 8 / ME11-EL-08 | Tên/role/avatar Mentor mẫu (“TS. Vũ Thành Đạt”, “MENTOR / GIẢNG VIÊN”). | Static; không lấy từ token hoặc #04/profile. PII-like sample không dùng làm current user data. | — |
| 9 / ME11-EL-09 | Eyebrow/icon `support_agent`, text “Cổng giải đáp & Đồng hành 1-on-1”. | Static label; “1-on-1” là copy, không phải scheduling integration. | — |
| 10 / ME11-EL-10 | H1 “Hộp thư hỗ trợ và giải đáp thắc mắc học viên”. | Heading tĩnh; page title không có validation. | — |
| 11 / ME11-EL-11 | Page description về quản lý/phản hồi học thuật hoặc kỹ thuật. | Static copy; không tạo SLA/policy/API behavior. | — |
| 12 / ME11-EL-12 | SLA badge “SLA phản hồi: < 4 giờ”. | Static claim, không có deadline/timestamp trong #58. Owner cần xác minh trước product promise. | — |
| 13 / ME11-EL-13 | “Vừa cập nhật tức thì” badge/clock text (`lastUpdatedTime`). | Initial HTML string; refresh timer chỉ đổi text. Không phải server freshness, polling hoặc realtime evidence. | E04 (prototype only) |
| 14 / ME11-EL-14 | Filter bar surface bao quanh tabs và course select. | Layout container; không có independent data/submit event. | E02/E03 |
| 15 / ME11-EL-15 | Tab “Tất cả” và badge số `0`; `role=tab`, `aria-selected=true`, `id=tab-all`. | Số 0 hardcoded trong HTML; không phải count response. Click chỉ đổi selected styles/ARIA. | E02 |
| 16 / ME11-EL-16 | Tab “Đang mở” và badge số `0`; `role=tab`, `aria-selected=false`, `id=tab-open`. | Không có mapping sang 1 hay nhiều status hiện tại; counter sample. | E02 |
| 17 / ME11-EL-17 | Tab “Đã giải quyết” và badge số `0`; `role=tab`, `aria-selected=false`, `id=tab-resolved`. | DDL fallback có `RESOLVED`, nhưng count/refresh behavior không có trong source. | E02 |
| 18 / ME11-EL-18 | Label “Khóa học:” liên kết `for="course-filter"`. | Label hiển thị trong desktop; CSS ẩn dưới breakpoint nhỏ (`hidden sm:inline-block`). | E03 |
| 19 / ME11-EL-19 | Course `<select id="course-filter">`; default `all`; các option slug mẫu. | `all`, `fe-adv`, `be-node`, `fullstack-capstone` không tương thích trực tiếp với `course_id:int64`; select không có change handler. Required/empty policy chưa chốt. | E03 |
| 20 / ME11-EL-20 | Empty-state content panel, container có `min-h-[520px]`, centered. | Prototype chỉ vẽ empty state; loading/ready/error panels không có. Visibility phải phụ thuộc #58 result trong implementation tương lai. | E01 |
| 21 / ME11-EL-21 | Mail illustration SVG với check badge. | Decorative (`aria-hidden=true`); không mang request status. | — |
| 22 / ME11-EL-22 | Empty-state heading “Không có yêu cầu hỗ trợ nào đang chờ xử lý”. | Static empty copy; chỉ hiển thị khi response `data=[]` theo future mapping đã duyệt. | E01 |
| 23 / ME11-EL-23 | Empty-state explanatory text về chưa có câu hỏi/yêu cầu. | Static copy; claim “gửi trực tiếp về đây” chưa có Student producer/route evidence. | E01 |
| 24 / ME11-EL-24 | Button “Làm mới hộp thư”; `type=button`. | Current handler disable/spinner ~650 ms rồi cập nhật clock; không gọi API, không có retry/error output. | E04 |
| 25 / ME11-EL-25 | Shield icon và claim auto-notification tức thời khi có tin nhắn. | Static claim; HTML không có WebSocket/SSE/polling/notification listener, #58 là GET list. | — |
| 26 / ME11-EL-26 | Info card “Thời hạn cam kết SLA” với copy ưu tiên 4 giờ làm việc. | Static guidance; #58 không trả priority, due time, business calendar hoặc SLA status. | — |
| 27 / ME11-EL-27 | Info card “Kho giải đáp chuẩn” và canned answer guidance. | Static claim; không có template/canned-answer API hoặc action trong HTML. | — |
| 28 / ME11-EL-28 | Info card “Hẹn gặp trực tiếp 1:1”/Google Meet guidance. | Static claim; không có meeting provider, link creation hoặc meeting field. | — |
| 29 / ME11-EL-29 | Footer logo icon. | Static; no event. | — |
| 30 / ME11-EL-30 | Copyright/ownership/WCAG text. | Static “© 2025” and “WCAG 2.1 AA” copy; không xác nhận ownership/compliance audit. | — |
| 31 / ME11-EL-31 | Footer link “Quy chế Giảng viên”; `href="#"`. | Destination/document chưa biết. | E06 |
| 32 / ME11-EL-32 | Footer link “Tiêu chuẩn đánh giá”; `href="#"`. | Destination chưa biết; không phải rubric contract. | E06 |
| 33 / ME11-EL-33 | Footer link “Hỗ trợ kỹ thuật”; `href="#"`. | Destination/contact channel chưa biết; không gắn với Google Meet claim. | E06 |

## 4. Conditional UI & state variations
- States theo inventory: loading/empty/ready/error
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/04_mentor/ME-11_hop-thu-ho-tro-hoc-vien/ME-11.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
