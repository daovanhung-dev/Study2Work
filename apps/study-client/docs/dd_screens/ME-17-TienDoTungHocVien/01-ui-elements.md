# ME-17 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [ME-17_markers.json](../../screen_stitch/04_mentor/ME-17_tien-do-tung-hoc-vien/ME-17_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `ME-17-EL-001` | `not supplied in marker JSON` | Study2Work brand and LMS Mentor label |
| #2 | `ME-17-EL-002` | `not supplied in marker JSON` | Tổng quan navigation |
| #3 | `ME-17-EL-003` | `not supplied in marker JSON` | Khóa học phụ trách navigation hiện hành |
| #4 | `ME-17-EL-004` | `not supplied in marker JSON` | Chấm bài navigation |
| #5 | `ME-17-EL-005` | `not supplied in marker JSON` | Hộp thư hỗ trợ navigation |
| #6 | `ME-17-EL-006` | `not supplied in marker JSON` | Thông báo navigation |
| #7 | `ME-17-EL-007` | `not supplied in marker JSON` | Notification bell and unread indicator |
| #8 | `ME-17-EL-008` | `not supplied in marker JSON` | Mentor name, role and avatar profile |
| #9 | `ME-17-EL-009` | `not supplied in marker JSON` | Breadcrumb link: Tiến độ lớp học |
| #10 | `ME-17-EL-010` | `not supplied in marker JSON` | Current breadcrumb: Hồ sơ tiến độ cá nhân học viên |
| #11 | `ME-17-EL-011` | `not supplied in marker JSON` | Hệ thống giám sát trực tiếp eyebrow |
| #12 | `ME-17-EL-012` | `not supplied in marker JSON` | Chi tiết lộ trình và tiến độ học viên page title |
| #13 | `ME-17-EL-013` | `not supplied in marker JSON` | Làm mới kết nối button |
| #14 | `ME-17-EL-014` | `not supplied in marker JSON` | Student profile icon and sync heading |
| #15 | `ME-17-EL-015` | `not supplied in marker JSON` | Mã học viên label and value |
| #16 | `ME-17-EL-016` | `not supplied in marker JSON` | Đã xác nhận ghi danh badge |
| #17 | `ME-17-EL-017` | `not supplied in marker JSON` | Khóa học đăng ký title |
| #18 | `ME-17-EL-018` | `not supplied in marker JSON` | Mức độ hoàn thành percent and progress bar |
| #19 | `ME-17-EL-019` | `not supplied in marker JSON` | Lần gửi dữ liệu cuối metric |
| #20 | `ME-17-EL-020` | `not supplied in marker JSON` | Chỉ số giám sát panel heading and tune icon |
| #21 | `ME-17-EL-021` | `not supplied in marker JSON` | Bài nộp dự án metric row |
| #22 | `ME-17-EL-022` | `not supplied in marker JSON` | Kiểm tra định kỳ metric row |
| #23 | `ME-17-EL-023` | `not supplied in marker JSON` | Thời lượng tự học metric row |
| #24 | `ME-17-EL-024` | `not supplied in marker JSON` | Monitoring data activation note |
| #25 | `ME-17-EL-025` | `not supplied in marker JSON` | Dòng thời gian học tập (Learning Timeline) heading |
| #26 | `ME-17-EL-026` | `not supplied in marker JSON` | Giai đoạn: Khởi tạo chương trình label |
| #27 | `ME-17-EL-027` | `not supplied in marker JSON` | Empty timeline illustration |
| #28 | `ME-17-EL-028` | `not supplied in marker JSON` | Lock badge on empty timeline illustration |
| #29 | `ME-17-EL-029` | `not supplied in marker JSON` | Chưa có lịch sử học tập được đồng bộ heading |
| #30 | `ME-17-EL-030` | `not supplied in marker JSON` | Empty timeline explanation |
| #31 | `ME-17-EL-031` | `not supplied in marker JSON` | Quay lại tiến độ toàn khóa button |
| #32 | `ME-17-EL-032` | `not supplied in marker JSON` | Bài giảng & Video explanatory tile |
| #33 | `ME-17-EL-033` | `not supplied in marker JSON` | Nhận xét của Mentor explanatory tile |
| #34 | `ME-17-EL-034` | `not supplied in marker JSON` | Cột mốc Đồ án explanatory tile |
| #35 | `ME-17-EL-035` | `not supplied in marker JSON` | Study2Work footer mark |
| #36 | `ME-17-EL-036` | `not supplied in marker JSON` | Footer copyright and WCAG copy |
| #37 | `ME-17-EL-037` | `not supplied in marker JSON` | Quy chế Giảng viên footer link |
| #38 | `ME-17-EL-038` | `not supplied in marker JSON` | Tiêu chuẩn đánh giá footer link |
| #39 | `ME-17-EL-039` | `not supplied in marker JSON` | Hỗ trợ kỹ thuật footer link |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Đặc tả từng element

Tọa độ marker là pixel center trên ảnh gốc 1280×1266. Marker JSON/SVG và ảnh chú thích nằm tại [ME-17_markers.json](../../screen_stitch/04_mentor/ME-17_tien-do-tung-hoc-vien/ME-17_markers.json), [ME-17_markers.svg](../../screen_stitch/04_mentor/ME-17_tien-do-tung-hoc-vien/ME-17_markers.svg), [screen_annotated.png](../../screen_stitch/04_mentor/ME-17_tien-do-tung-hoc-vien/screen_annotated.png). Mỗi hàng dưới đây khớp đúng một marker; phần tử tĩnh không có input validation. Không suy ra responsive/hover behavior ngoài class/style có trong HTML mẫu.

| ID | Tên / loại | Vị trí, thuộc tính, mục đích | Nguồn, điều kiện, trạng thái | Event |
|---:|---|---|---|---|
| 1 | Study2Work brand and LMS Mentor label — anchor/brand | Header trái; logo, tên và subtitle. HTML href="#" và data-path=tong-quan. | Static; visible theo shell mẫu; không có route thật. Focus ring có trong HTML class. | EV-04 |
| 2 | Tổng quan navigation — anchor | Header; nav anchor href="#" và data-path=tong-quan. | Placeholder; không có URL đích. Hover/focus class trong HTML, không có route state. | EV-04 |
| 3 | Khóa học phụ trách — anchor/nav hiện hành | Header; href="#" và data-path=khoa-hoc-phu-trach; aria-current=page, active styling. | Static active state của prototype, không xác nhận route hiện tại. | EV-04 |
| 4 | Chấm bài navigation — anchor | Header; href="#" và data-path=cham-bai. | Placeholder, không có route/API. | EV-04 |
| 5 | Hộp thư hỗ trợ navigation — anchor | Header; href="#" và data-path=hop-thu-ho-tro. | Placeholder, không có route/API. | EV-04 |
| 6 | Thông báo navigation — anchor | Header; href="#" và data-path=thong-bao. | Placeholder, không có route/API. | EV-04 |
| 7 | Notification bell and unread indicator — anchor | Header phải; icon notification + dot đỏ; href="#" và data-path=thong-bao. | Dot đỏ tĩnh; không có unread count/state source. | EV-04 |
| 8 | Mentor name, role and avatar profile — profile summary | Header phải; tên “TS. Vũ Thành Đạt”, role “MENTOR / GIẢNG VIÊN”, icon avatar. | Static; không phải profile API result; không phải link/button và không có event. | — |
| 9 | Breadcrumb link: Tiến độ lớp học — anchor | Trên trang; icon + text breadcrumb, href="#". | Placeholder; có thể gợi ý course progress nhưng destination/course ID chưa được nối. | EV-04 |
| 10 | Current breadcrumb: Hồ sơ tiến độ cá nhân học viên — text/current breadcrumb | Breadcrumb cuối; aria-current=page, không có href. | Static current label; không có event. | — |
| 11 | Hệ thống giám sát trực tiếp eyebrow — label | Trên H1, chấm xanh và copy giám sát trực tiếp. | Static marketing/status copy; không chứng minh realtime stream/poll. | — |
| 12 | Chi tiết lộ trình và tiến độ học viên page title — heading/H1 | Page heading; không có input hoặc action. | Static text; visible. | — |
| 13 | Làm mới kết nối — button | Hero phải; type=button, id=refreshSyncBtn, icon sync id=syncIcon. | Enabled ngoài thời gian handler; không có validation/API state. Current handler disable/rotate 600 ms rồi restore. | EV-02 |
| 14 | Student profile icon and sync heading — profile/status card | Card trái; person icon và “Đang đồng bộ hồ sơ…”. | Static prototype copy; không bind #67 loading/student response. | — |
| 15 | Mã học viên label and value — identifier text | Dưới heading profile; label “Mã học viên”, literal “Chưa nạp”. | Không có student-code field trong #67. Không đổi student.id thành mã học viên khi chưa có mapping. | — |
| 16 | Đã xác nhận ghi danh — badge | Badge xanh trên card profile. | Static claim; #67 kiểm ACTIVE enrollment nhưng response local không trả enrollment status. | — |
| 17 | Khóa học đăng ký title — text | Tóm tắt course; literal “Chuyên đề Đào tạo Thực chiến”. | #67 chỉ trả course_id, không trả course title. Không dùng course_id để dựng title. | — |
| 18 | Mức độ hoàn thành percent and progress bar — metric/progress bar | Khối giữa; literal 0% và thanh progress. | Candidate mapping từ summary.progress_percent chỉ sau khi contract được duyệt; giá trị screenshot không phải runtime default. Không có range validation ở UI trong prototype. | — |
| 19 | Lần gửi dữ liệu cuối — metric/freshness | Khối phải của course summary; label và “Chưa ghi nhận”. | #67 chỉ có timestamps per lesson; không có last-sync/send timestamp hoặc freshness SLA. | — |
| 20 | Chỉ số giám sát panel heading and tune icon — card heading | Heading panel phải; tune icon là decorative. | Static title; không có settings action. | — |
| 21 | Bài nộp dự án metric row — metric row | Panel phải; label, icon và literal “-- / --”. | #67 không trả assignment submission counts. Không hiển thị từ lessons hoặc #65/#66. | — |
| 22 | Kiểm tra định kỳ metric row — metric row | Panel phải; label, icon và literal “-- / --”. | #67 không trả quiz/assessment counts. Không suy ra từ lesson progress. | — |
| 23 | Thời lượng tự học metric row — metric row | Panel phải; label, icon và literal “0 giờ”. | #67 không trả study-hour duration. Literal 0 không phải measured zero. | — |
| 24 | Monitoring data activation note — informational note | Dưới metric rows; copy nói dữ liệu thống kê sẽ kích hoạt sau buổi học đầu tiên. | Static business claim; không có field, event trigger hoặc rule trong #67. | — |
| 25 | Dòng thời gian học tập (Learning Timeline) heading — card heading | Trên card timeline; icon chart decorative. | Static title. #67 trả per-lesson state snapshot, không trả event history. | — |
| 26 | Giai đoạn: Khởi tạo chương trình — status label | Góc phải heading timeline, dot xám + phase copy. | Static; không có curriculum-phase/status field trong #67. | — |
| 27 | Empty timeline illustration — illustration | Vùng giữa timeline; document/check illustration. | Decorative; không phải API empty result indicator. | — |
| 28 | Lock badge on empty timeline illustration — icon/badge | Badge khóa nhỏ cạnh illustration. | Decorative; không chứng minh authorization denial hay locked course state. | — |
| 29 | Chưa có lịch sử học tập được đồng bộ — empty-state heading | Trung tâm empty panel. | Static empty state; không suy ra từ lessons=[] vì điều kiện đó có thể là course không có PUBLISHED lesson. | — |
| 30 | Empty timeline explanation — text | Mô tả hoạt động hoàn thành và bài nộp/bài kiểm tra sẽ xuất hiện theo mốc thời gian. | Static promise. #67 không cung cấp event chronology, assignment/quiz activity hoặc sync pipeline. | — |
| 31 | Quay lại tiến độ toàn khóa — anchor/button | Primary action trong empty panel; HTML href="#". | Inventory gợi ý ME-16, nhưng course_id carrier/destination route chưa wire. Không có API call. | EV-03 |
| 32 | Bài giảng & Video explanatory tile — information card | Tile trái; icon sách và copy “Tự động đánh dấu hoàn thành…” | Static policy claim; #67 đọc trạng thái hiện có, không đánh dấu completion hay cung cấp playback. | — |
| 33 | Nhận xét của Mentor explanatory tile — information card | Tile giữa; icon/comment và copy về hỗ trợ theo mốc bài tập. | Static; #67 không trả mentor comments hoặc assignment milestones. | — |
| 34 | Cột mốc Đồ án explanatory tile — information card | Tile phải; flag và copy theo chuẩn chương trình nghề nghiệp. | Static; #67 không trả project milestone/rubric. | — |
| 35 | Study2Work footer mark — brand mark | Footer trái; school icon trong khối xanh, không interactive. | Static decoration. | — |
| 36 | Footer copyright and WCAG copy — footer text | Copyright 2025, WCAG 2.1 AA và portal copy. | Static; accessibility conformance chưa được kiểm thử/xác nhận trong phiên. | — |
| 37 | Quy chế Giảng viên — footer anchor | Footer phải; href="#". | Placeholder; không có destination. | EV-04 |
| 38 | Tiêu chuẩn đánh giá — footer anchor | Footer phải; href="#". | Placeholder; không có destination. | EV-04 |
| 39 | Hỗ trợ kỹ thuật — footer anchor | Footer phải; href="#". | Placeholder; không có destination. | EV-04 |

## 4. Conditional UI & state variations
- States theo inventory: loading/ready/denied/not-found
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/04_mentor/ME-17_tien-do-tung-hoc-vien/ME-17.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
