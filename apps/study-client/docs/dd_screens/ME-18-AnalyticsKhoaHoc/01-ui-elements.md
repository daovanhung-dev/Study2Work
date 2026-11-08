# ME-18 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [ME-18_markers.json](../../screen_stitch/04_mentor/ME-18_analytics-khoa-hoc/ME-18_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `ME-18-EL-001` | `not supplied in marker JSON` | Study2Work brand and LMS Mentor label |
| #2 | `ME-18-EL-002` | `not supplied in marker JSON` | Tổng quan navigation |
| #3 | `ME-18-EL-003` | `not supplied in marker JSON` | Khóa học phụ trách navigation hiện hành |
| #4 | `ME-18-EL-004` | `not supplied in marker JSON` | Chấm bài navigation |
| #5 | `ME-18-EL-005` | `not supplied in marker JSON` | Hộp thư hỗ trợ navigation |
| #6 | `ME-18-EL-006` | `not supplied in marker JSON` | Thông báo navigation |
| #7 | `ME-18-EL-007` | `not supplied in marker JSON` | Notification bell and unread indicator |
| #8 | `ME-18-EL-008` | `not supplied in marker JSON` | Mentor name, role and avatar profile |
| #9 | `ME-18-EL-009` | `not supplied in marker JSON` | Breadcrumb link: Khóa học phụ trách |
| #10 | `ME-18-EL-010` | `not supplied in marker JSON` | Breadcrumb course title and code: Kỹ thuật Lập trình Hệ thống Cao cấp (CS-402) |
| #11 | `ME-18-EL-011` | `not supplied in marker JSON` | Current breadcrumb: Báo cáo & Phân tích chuyên sâu |
| #12 | `ME-18-EL-012` | `not supplied in marker JSON` | Học kỳ II • 2024-2025 semester badge |
| #13 | `ME-18-EL-013` | `not supplied in marker JSON` | Chờ đồng bộ dữ liệu course status |
| #14 | `ME-18-EL-014` | `not supplied in marker JSON` | Phân tích và thống kê hiệu quả khóa học page title |
| #15 | `ME-18-EL-015` | `not supplied in marker JSON` | Analytics explanatory subtitle |
| #16 | `ME-18-EL-016` | `not supplied in marker JSON` | Khung thời gian phân tích label |
| #17 | `ME-18-EL-017` | `not supplied in marker JSON` | Disabled timeframe selector, options and lock icon |
| #18 | `ME-18-EL-018` | `not supplied in marker JSON` | Tác vụ báo cáo label |
| #19 | `ME-18-EL-019` | `not supplied in marker JSON` | Disabled Xuất dữ liệu (.CSV) button |
| #20 | `ME-18-EL-020` | `not supplied in marker JSON` | Tỷ lệ hoàn thành KPI card |
| #21 | `ME-18-EL-021` | `not supplied in marker JSON` | Thời lượng trung bình KPI card |
| #22 | `ME-18-EL-022` | `not supplied in marker JSON` | Tương tác thảo luận KPI card |
| #23 | `ME-18-EL-023` | `not supplied in marker JSON` | Empty analytics illustration |
| #24 | `ME-18-EL-024` | `not supplied in marker JSON` | Trạng thái phân tích: Chưa kích hoạt badge |
| #25 | `ME-18-EL-025` | `not supplied in marker JSON` | Chưa có số liệu phân tích thống kê heading |
| #26 | `ME-18-EL-026` | `not supplied in marker JSON` | Analytics empty-state explanation |
| #27 | `ME-18-EL-027` | `not supplied in marker JSON` | Quay lại tiến độ toàn khóa (ME-16) anchor |
| #28 | `ME-18-EL-028` | `not supplied in marker JSON` | Kiểm tra đồng bộ lại button |
| #29 | `ME-18-EL-029` | `not supplied in marker JSON` | WCAG 2.1 AA Compliant badge |
| #30 | `ME-18-EL-030` | `not supplied in marker JSON` | Schema v2.4 Analytical Ready badge |
| #31 | `ME-18-EL-031` | `not supplied in marker JSON` | Study2Work footer mark |
| #32 | `ME-18-EL-032` | `not supplied in marker JSON` | Footer copyright and standards copy |
| #33 | `ME-18-EL-033` | `not supplied in marker JSON` | Quy chế Giảng viên footer link |
| #34 | `ME-18-EL-034` | `not supplied in marker JSON` | Tiêu chuẩn đánh giá footer link |
| #35 | `ME-18-EL-035` | `not supplied in marker JSON` | Hỗ trợ kỹ thuật footer link |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Đặc tả từng element

Tọa độ marker tính từ góc trên-trái ảnh gốc 1600×1380. Đối chiếu [ME-18_markers.json](../../screen_stitch/04_mentor/ME-18_analytics-khoa-hoc/ME-18_markers.json), [ME-18_markers.svg](../../screen_stitch/04_mentor/ME-18_analytics-khoa-hoc/ME-18_markers.svg), [screen_annotated.png](../../screen_stitch/04_mentor/ME-18_analytics-khoa-hoc/screen_annotated.png). Một card metric là một element gồm icon, label, value và caption; icon trang trí được nhóm với component. Phần tử tĩnh không có input validation.

| ID | Tên / loại | Vị trí, thuộc tính, mục đích | Nguồn, visibility/state, validation | Event |
|---:|---|---|---|---|
| 1 | Study2Work brand and LMS Mentor label — anchor/brand | Header trái; logo, tên và LMS Mentor subtitle. HTML href="#" và data-path=tong-quan. | Static shell; visible; HTML có focus ring nhưng chưa có route. | EV-06 |
| 2 | Tổng quan navigation — anchor | Header; nav anchor href="#" và data-path=tong-quan. | Placeholder; không có URL đích. | EV-06 |
| 3 | Khóa học phụ trách navigation hiện hành — anchor/nav | Header; href="#" và data-path=khoa-hoc-phu-trach; aria-current=page, active style. | Active visual state chỉ là prototype; không xác nhận router. | EV-06 |
| 4 | Chấm bài navigation — anchor | Header; href="#" và data-path=cham-bai. | Placeholder; không có route/API. | EV-06 |
| 5 | Hộp thư hỗ trợ navigation — anchor | Header; href="#" và data-path=hop-thu-ho-tro. | Placeholder; không có route/API. | EV-06 |
| 6 | Thông báo navigation — anchor | Header; href="#" và data-path=thong-bao. | Placeholder; không có route/API. | EV-06 |
| 7 | Notification bell and unread indicator — anchor | Header phải; icon bell và dot đỏ; href="#" và data-path=thong-bao. | Dot/count tĩnh; không có unread source. | EV-06 |
| 8 | Mentor name, role and avatar profile — profile summary | Header phải; TS. Vũ Thành Đạt, Mentor/Giảng viên và avatar icon. | Static text/icon; không phải profile response, không phải link/action. | — |
| 9 | Breadcrumb link: Khóa học phụ trách — anchor | Breadcrumb đầu; icon sách + text; href="#". | Placeholder; không mang course_id. | EV-06 |
| 10 | Breadcrumb course title and code: Kỹ thuật Lập trình Hệ thống Cao cấp (CS-402) — anchor | Breadcrumb giữa; course name và mã CS-402; href="#". | Static; #66 response chỉ có aggregate fields, không trả title/code. | EV-06 |
| 11 | Current breadcrumb: Báo cáo & Phân tích chuyên sâu — text/current breadcrumb | Breadcrumb cuối, không href. | Static current-page text. | — |
| 12 | Học kỳ II • 2024-2025 semester badge — badge | Hero trên; hiển thị term. | Literal; #66 không trả semester/term. | — |
| 13 | Chờ đồng bộ dữ liệu course status — status label | Cạnh term badge; dot xám và status copy. | Static sync claim; không có sync state trong #66. | — |
| 14 | Phân tích và thống kê hiệu quả khóa học — heading/H1 | Hero H1; tiêu đề trang. | Static heading. | — |
| 15 | Analytics explanatory subtitle — text | Dưới H1; mô tả hiệu suất, engagement và retention từ dữ liệu chuẩn hóa LMS. | Static product claim; API #66 không trả retention hoặc standardized-event status. | — |
| 16 | Khung thời gian phân tích label — label | Cột phải trên control. | Static text; không có event. | — |
| 17 | Disabled timeframe selector, options and lock icon — select/disabled | Select id=timeframe-select; current text 7 ngày gần đây; options 30 ngày gần đây và Toàn khóa học cũng ghi chưa có dữ liệu; disabled, có lock. | Không nhận Change khi disabled; API không có query params. Option values/period boundary/timezone chưa có contract. | — (disabled; EV-02 records no action) |
| 18 | Tác vụ báo cáo label — label | Trên export action. | Static label. | — |
| 19 | Disabled Xuất dữ liệu (.CSV) button — button/disabled export | Type button, disabled, aria-disabled=true. | Không thể kích hoạt từ prototype; không có endpoint/job/file. | — (disabled; EV-03 records no action) |
| 20 | Tỷ lệ hoàn thành KPI card — card/metric | Card trái gồm icon, label, literal “——” và “Chờ pipeline ETL tổng hợp”. | Static; #66 không trả completion rate hay ETL state. | — |
| 21 | Thời lượng trung bình KPI card — card/metric | Card giữa gồm icon, label, literal “——” và “Đang thu thập telemetry”. | Static; #66 không trả duration/telemetry state. | — |
| 22 | Tương tác thảo luận KPI card — card/metric | Card phải gồm icon, label, literal “——” và “Chưa có bài nộp/thảo luận”. | Static; #66 không trả discussion/submission counts. | — |
| 23 | Empty analytics illustration — illustration | Trung tâm panel; decorative chart/person icon. | Không phải chart data hoặc API no-data proof. | — |
| 24 | Trạng thái phân tích: Chưa kích hoạt badge — badge/status | Trên empty heading; text status phân tích. | Static; #66 không có pipeline activation field. | — |
| 25 | Chưa có số liệu phân tích thống kê heading — heading/empty state | Empty panel trung tâm. | Static copy; không bind local 0/0/null hay catalog page. | — |
| 26 | Analytics empty-state explanation — text | Copy nói completion/time distribution/discussion frequency đang chờ server analytics; charts bật khi đủ dữ liệu thực. | Static promise; không có threshold, event pipeline, readiness flag hoặc loaded chart design trong source. | — |
| 27 | Quay lại tiến độ toàn khóa (ME-16) anchor — anchor/navigation | Primary action; data-path=tien-do-toan-khoa, href="#". | Expected link to ME-16; route/course_id carrier chưa wire. | EV-05 |
| 28 | Kiểm tra đồng bộ lại button — button | Type button, inline onclick; ban đầu enabled-looking. | JS chỉ thay innerHTML/timers, không disable/fetch/persist. Repeated click có thể chồng timer. | EV-04 |
| 29 | WCAG 2.1 AA Compliant badge — claim/status | Badge ở cuối panel, icon verified_user + copy. | Static claim; no accessibility audit evidence. | — |
| 30 | Schema v2.4 Analytical Ready badge — claim/status | Cạnh badge WCAG, database icon + schema version/readiness copy. | Static; version/readiness không có API/config source. | — |
| 31 | Study2Work footer mark — brand mark | Footer trái; school icon. | Decorative, không interactive. | — |
| 32 | Footer copyright and standards copy — footer text | Copyright 2025, WCAG 2.1 AA và portal copy. | Static text; compliance claim chưa được xác minh. | — |
| 33 | Quy chế Giảng viên footer link — anchor | Footer phải; href="#". | Placeholder; không có destination. | EV-06 |
| 34 | Tiêu chuẩn đánh giá footer link — anchor | Footer phải; href="#". | Placeholder; không có destination. | EV-06 |
| 35 | Hỗ trợ kỹ thuật footer link — anchor | Footer phải; href="#". | Placeholder; không có destination. | EV-06 |

## 4. Conditional UI & state variations
- States theo inventory: loading/no-data/ready/error
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/04_mentor/ME-18_analytics-khoa-hoc/ME-18.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
